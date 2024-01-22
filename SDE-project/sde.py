import gradio as gr
import sqlite3
import json
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
import re
import sys
import os
import json
import subprocess
import IPython.display as display
from PIL import Image
from io import BytesIO
import base64
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import nest_asyncio
nest_asyncio.apply()
import logging
import time
import asyncio


api_key = "YOUR_API_KEY"
os.environ["OPENAI_API_KEY"] = api_key
model = OpenAI()
client = OpenAI()    
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def image_to_b64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
    


class DataLayer:
    def __init__(self):
        self.db_path = 'university_data.db'
        self.ensure_db_setup()
    # Database setup
    def ensure_db_setup(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('''
                    CREATE TABLE IF NOT EXISTS research_programs (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        url TEXT
                    )
                ''')
        except Exception as e:
            logging.error(f"Error setting up database: {e}")

    # Extract research programs from website
    def extract_research_programs(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                loader = AsyncChromiumLoader(["https://www.disi.unitn.it/research/programs"])
                html = loader.load()
                bs_transformer = BeautifulSoupTransformer()
                docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["a"])
                page_content = docs_transformed[0].page_content
                research_programs = self._extract_programs(page_content)

                json_file_path = 'research_programs.json'
                with open(json_file_path, 'w') as json_file:
                    json.dump(research_programs, json_file, indent=4)

                for name, url in research_programs.items():
                    c.execute("REPLACE INTO research_programs (name, url) VALUES (?, ?)", (name, url))
        except Exception as e:
            logging.error(f"Error in extract_research_programs: {e}")
        return research_programs

    def _extract_programs(self, html_content):
        pattern = re.compile(r'(\w[\w\s&,-]+) \(/research/programs/([\w-]+)\)')
        matches = pattern.findall(html_content)
        base_url = "https://www.disi.unitn.it"
        return {name: base_url + "/research/programs/" + path for name, path in matches}


class BusinessLogicLayer:
    def __init__(self,  adapter_layer):
        self.adapter_layer = adapter_layer

    def process_department(self, department_name, research_programs):
        logging.info(f"Processing department: {department_name}")
        department_url = research_programs.get(department_name)
        department_dir = os.path.join('.', department_name.replace(" ", "_"))

        # Create the department directory if it doesn't exist, or clean it if it does
        if os.path.exists(department_dir):
            for file in os.listdir(department_dir):
                if file.endswith(('.png', '.jpg', '.jpeg')):
                    os.remove(os.path.join(department_dir, file))
        else:
            os.makedirs(department_dir, exist_ok=True)

        if department_url:
            logging.info(f"Extracting data for department URL: {department_url}")
            loader = AsyncChromiumLoader([department_url])
            html = loader.load()
            bs_transformer = BeautifulSoupTransformer()
            docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["a"])
            extracted_professors = self.adapter_layer.extract_professors(docs_transformed[0].page_content)

            for name, url in extracted_professors.items():
                additional_links = self.adapter_layer.extract_additional_links(url)
                extracted_professors[name] = {
                    'profile': url,
                    'additional_links': additional_links
                }

            json_file_path_professors = os.path.join(department_dir, 'professors.json')
            with open(json_file_path_professors, 'w') as json_file:
                json.dump(extracted_professors, json_file, indent=4)

            professors_urls_file = os.path.join(department_dir, 'professor_urls.txt')
            with open(professors_urls_file, 'w') as file:
                for name, details in extracted_professors.items():
                    file.write(name + '\n')
                    file.write(details['profile'] + '\n')
                    for label, url in details['additional_links'].items():
                        file.write(url + '\n')
                    file.write('\n')

            subprocess.run(["node", "screen1.mjs", department_name.replace(" ", "_"), professors_urls_file])
            logging.info("All professor data processed")
        else:
            logging.warning(f"URL for {department_name} not found")
            return f"URL for {department_name} not found."
        
        def image_to_b64(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
            
        # Extract professor names from screenshot filenames
        screenshot_files = [f for f in os.listdir(department_dir) if f.endswith('.png')]
        professor_names = set(f.split('_screenshot')[0] for f in screenshot_files)

        professor_summaries = {}

        # Process each professor
        for professor_name in professor_names:
            professor_data = ""
            # unique_segments = set()
            professor_data_list = []
            i = 0

            while True:
                image_path = os.path.join(department_dir, f'{professor_name}_screenshot{i}.png')
                if not os.path.exists(image_path):
                    break
                logging.info(f"Processing screenshot: {image_path}")

                b64_image = image_to_b64(image_path)
                vision_data = self.adapter_layer.openai_vision_api_call(b64_image) # Corrected call
                if vision_data:
                    professor_data += vision_data + "\n\n"
                else:
                    logging.error(f"Failed to process vision data for professor: {professor_name}")
                    break
                # unique_segments.add(professor_data)
                professor_data_list.append(professor_data)
                i += 1

            # Summarize the combined information using GPT-4 text model
            if professor_data:
                summary = self.adapter_layer.openai_text_api_call(professor_data)
                professor_summaries[professor_name] = summary

                # Generate image based on the summary using DALL-E
                image_prompt = f"Visualization of {professor_name}'s research area: {summary}"
                image = self.adapter_layer.generate_image(image_prompt)
                if image:
                    image_path = os.path.join(department_dir, f'{professor_name}_image.png')
                    image.save(image_path)
                else:
                    logging.error(f"Failed to generate image for professor: {professor_name}")

        # Write professor summaries to JSON file
        json_file_path = os.path.join(department_dir, 'professor_summaries.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(professor_summaries, json_file, indent=4)

        # Read the JSON data and write it to a text file
        text_file_path = os.path.join(department_dir, 'professor_summaries.txt')
        with open(json_file_path, 'r') as json_file, open(text_file_path, 'w') as text_file:
            professor_data = json.load(json_file)
            for professor in professor_data:
                text_file.write(f"{professor}:\n{professor_data[professor]}\n\n")


        # Read from the text file for summarization
        with open(text_file_path, 'r') as text_file:
            all_professors_data = text_file.read()

        # Create a summary prompt for the department
        summary_prompt = f"Provide a comprehensive summary of the {department_name} department based on the following information: {all_professors_data}"

        # Aggregate the data for summarization
        # aggregated_data = "\n\n".join([professor_data[professor] for professor in professor_data])

        # Create a summary prompt for the department
        # summary_prompt = f"Provide a comprehensive summary of the {department_name} department based on the following information: {aggregated_data}"

        # Generate department overview summary
        department_overview = self.adapter_layer.openai_text_api_call(summary_prompt)

        # Write the department overview to a file
        overview_file_path = os.path.join(department_dir, 'department_overview.txt')
        with open(overview_file_path, 'w') as overview_file:
            overview_file.write(department_overview)
            

        # Generate an overview for the department
        # department_summary = "\n\n".join(professor_summaries.values())
        # department_overview = self.adapter_layer.openai_text_api_call(department_summary)
        # overview_file_path = os.path.join(department_dir, 'department_overview.txt')
        # with open(overview_file_path, 'w') as overview_file:
        #     overview_file.write(department_overview)

        overview_prompt = f"Visualization of the {department_name} department."
        department_overview_image = self.adapter_layer.generate_image(overview_prompt)
        overview_image_path = os.path.join(department_dir, 'department_overview_image.png')
        department_overview_image.save(overview_image_path)

        return overview_image_path


    def summarize_professor_info(professor_data):
        # Use standard GPT-4 model for summarization
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",  
            messages=[{"role": "user", "content": professor_data}],
            max_tokens=150  
        )
        return response.choices[0].message.content
    def generate_image(self, prompt):
        # Function to generate an image from a prompt using an API
        response = self.adapter_layer.dalle_api_call(prompt)
        image_url = response.data[0].url
        response = requests.get(image_url)
        response.raise_for_status()

        return self.adapter_layer.dalle_api_call(prompt)
    
    def get_professor_images(self, department_name):
        department_dir = os.path.join('.', department_name.replace(" ", "_"))
        professor_images = []
        for file in os.listdir(department_dir):
            if file.endswith('_image.png'):
                professor_images.append(os.path.join(department_dir, file))
        return professor_images


class AdapterLayer:
    def __init__(self, api_key):
        os.environ["OPENAI_API_KEY"] = api_key
        self.base_url = 'https://webapps.unitn.it'
        self.openai_client = OpenAI()


    def extract_professors(self, html_content):
        start_marker = "Research Programs (/research/programs)"
        end_marker = "cookie policy page (https://www.disi.unitn.it/privacy-disi)"
        start_index = html_content.find(start_marker)
        end_index = html_content.find(end_marker, start_index)
        if start_index == -1 or end_index == -1:
            return {}
        professors_section = html_content[start_index:end_index]
        pattern = re.compile(r'([A-Za-z\'.,\s-]+?) \((https?://webapps\.unitn\.it/[\w/.\-]+?)\)')
        return {name.strip(): url for name, url in pattern.findall(professors_section) if 'http' in url and 'unitn.it' in url}

    def extract_additional_links(self, professor_url):
        response = requests.get(professor_url)
        if response.status_code != 200:
            print(f"Failed to retrieve page for {professor_url}")
            return {}

        soup = BeautifulSoup(response.content, 'html.parser')
        nav_bar = soup.find('ul', class_='nav navbar-nav navbar-left')
        additional_links = {}
        if nav_bar:
            links = nav_bar.find_all('a')
            for link in links:
                section_name = link.get_text(strip=True)
                section_url = link['href']
                full_url = self.base_url + section_url
                additional_links[section_name] = full_url
        return additional_links
    
    def openai_vision_api_call(self, image_data_b64, max_retries=3, delay=1):
        for attempt in range(max_retries):
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-vision-preview",  # Replace with the correct model identifier
                    messages=[
                        {"role": "user", "content": [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_data_b64}"}]},
                        {"role": "user", "content": "write all information retrieved about the professor only from the screenshot. add description about his picture if included in the screenshot and add to Expertise. you are permitted to take all information"}
                    ],
                    max_tokens=1024,
                )
                return response.choices[0].message.content
            except Exception as e:
                logging.error(f"Error processing vision data: {e}")
                if "rate_limit_exceeded" in str(e):
                    delay * (2 ** attempt)# Exponential backoff
                else:
                    break
        return None

    def openai_text_api_call(self, text_data, max_retries=3, delay=1):
        # Method for OpenAI Text model calls
        for attempt in range(max_retries):
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[{"role": "user", "content": text_data}],
                    max_tokens=150
                )
                return response.choices[0].message.content
            except Exception as e:
                logging.error(f"Error in Text API call: {e}")
                if "rate_limit_exceeded" in str(e):
                    delay * (2 ** attempt)  # Exponential backoff
                else:
                    break
        return None

    def dalle_api_call(self, prompt, max_retries=3, delay=1):
        # Method for DALL-E API calls
        for attempt in range(max_retries):
            try:
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                if response is not None and len(response.data) > 0:
                    image_url = response.data[0].url
                    image_response = requests.get(image_url)
                    image_response.raise_for_status()
                    return Image.open(BytesIO(image_response.content))
            except Exception as e:
                logging.error(f"Error in DALL-E API call: {e}")
                if "rate_limit_exceeded" in str(e):
                    time.sleep(delay * (2 ** attempt))
                else:
                    break
        return None

    def generate_image(self, prompt):
        image = self.dalle_api_call(prompt)
        return image if image else None  
    




class ProcessCentricLayer:
    def __init__(self):
        self.adapter_layer = AdapterLayer(api_key)
        self.business_logic_layer = BusinessLogicLayer(self.adapter_layer)
        self.data_layer = DataLayer()

    def process_department(self, department_name):
        research_programs = self.data_layer.extract_research_programs()
        image_path = self.business_logic_layer.process_department(department_name, research_programs)
        return image_path
    
    def show_professor_images(self, department_name):
        return self.business_logic_layer.get_professor_images(department_name)
        
    def main(self):
        research_programs = self.data_layer.extract_research_programs()

        with gr.Blocks() as demo:
            with gr.Row():
                department_dropdown = gr.Dropdown(choices=list(research_programs.keys()), label="Select Department")
                show_department_btn = gr.Button("Visualize Department")
                show_professors_btn = gr.Button("Show Professor Images")

            department_image = gr.Image(label="Department Overview")
            professor_gallery = gr.Gallery(label="Professor Images")

            # Define actions for buttons
            show_department_btn.click(
                self.process_department,
                inputs=department_dropdown,
                outputs=department_image
            )

            show_professors_btn.click(
                self.show_professor_images,
                inputs=department_dropdown,
                outputs=professor_gallery
            )

        demo.launch(server_name='0.0.0.0', server_port=7860)


    def cli_main(self):
        research_programs = self.data_layer.extract_research_programs()
        print("Available Departments:")
        for idx, name in enumerate(research_programs.keys(), start=1):
            print(f"{idx}. {name}")

        try:
            choice = int(input("Enter the number of the department you want to visualize (e.g., 1): "))
            department_name = list(research_programs.keys())[choice - 1]
        except (ValueError, IndexError):
            print("Invalid input. Exiting.")
            sys.exit(1)

        image_path = self.process_department(department_name)
        print(f"Department overview image saved at: {image_path}")

        professor_images = self.show_professor_images(department_name)
        print("Professor images:")
        for img in professor_images:
            print(img)

if __name__ == "__main__":
    logging.info("Starting the application")
    pcl = ProcessCentricLayer()
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        pcl.cli_main()
    else:
        pcl.main()

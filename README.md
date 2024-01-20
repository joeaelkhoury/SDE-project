# Project Title: SDE Project: Scraping and visualizing university research groups

## Overview
This project involves Docker, Puppeteer, Playwright, Gradio, SQLite, and integration with OpenAI's GPT-4 and DALL-E models. It's designed to capture and process data from university websites, particularly focusing on research programs and faculty information, and then uses AI to summarize and visualize this data.

## Features
- Dockerized Python and Node.js environment.
- Web scraping using Puppeteer.
- Automated browser actions with Playwright.
- Data extraction and transformation.
- Integration with OpenAI's GPT-4 and DALL-E for text summarization and image generation.
- SQLite database for storing extracted data.
- Gradio interface for easy visualization and interaction, which plays also the server side.
- Auth0 integration for secure user authentication.


## Prerequisites
- Docker
- Node.js (Installed in the Docker container)
- Python 3.11.6 (Used in the Docker container)
- An OpenAI API key (set in the Dockerfile and code)
- Auth0 account for authentication setup

## Installation

### Step 1: Clone the Repository
```docker
Clone this repository to your local machine:
git clone https://github.com/joeaelkhoury/SDE-project
```
### Step 2: Building the Docker Container
Navigate to the project directory and build the Docker container:
```docker
cd C:\Users\x\ [your project directory]
docker build -t sde .
```
### Step 3: Run the Container
Run the Docker container for the file without Auth0:
```docker
docker run -it -p 7860:7860 sde
```
while for the file with Auth0
```docker
docker run -it -p 5000:5000 -p 7860:7860 sde
```
## Usage

### Running the Script
- Once the Docker container is up, the Python script `sde.py` will execute automatically.
- The script will scrape data, interact with OpenAI's API, and use Gradio for visualization.

### Accessing the Interface
- Access to the interface at
```html
  http://127.0.0.1:5000/login
```
### Using Gradio Interface
- Access the Gradio interface at
```html
  http://localhost:7860 
```
- Select a department from the dropdown and click on the buttons to visualize department overviews or professor images.

### Command Line Interface (CLI) Mode
- To run the application in CLI mode, use:
```cmd
python sde.py --cli
```
- Follow the prompts to interact with the application via the command line.

## Code Structure

- `Dockerfile`: This file is used to define the Docker container where the application will run. It specifies the base image, environment setup, dependencies to be installed, and the commands to run the application.

- `sde.py`: The main Python script of the application. It contains the core logic for web scraping, data processing, interaction with OpenAI's API, and Gradio interface setup for visualization.

- `requirements.txt`: Lists all the Python dependencies required for the project. This file is used by pip to automatically install all the necessary Python packages.

- `screen1.mjs`: A Node.js module script that handles specific tasks like screenshot taking and browsing in a JavaScript/Node.js environment. It is used in conjunction with the Python script since its functions are better handled in Node.js.
- auth.py: Python script for handling Auth0 authentication.

Each of these files plays a critical role in the setup, execution, and functionality of your application.


# Component Overview and Implementation

# DataLayer: Handles database operations and scrapes research program data.
```python
class DataLayer:
    def __init__(self):
        self.db_path = 'university_data.db'

    def ensure_db_setup(self):
        # Database setup code here

    def extract_research_programs(self):
        # Web scraping code here
```

# BusinessLogicLayer: Processes department information, extracts professor details, and generates visual summaries.

```python
class BusinessLogicLayer:
    def __init__(self, adapter_layer):
        self.adapter_layer = adapter_layer

    def process_department(self, department_name, research_programs):
        # Department processing code here

    def summarize_professor_info(professor_data):
        # Professor info summarization code here
```

# AdapterLayer: Handles OpenAI API interactions and manages web scraping tasks.
```python
class AdapterLayer:
    def __init__(self, api_key):
        # Initialization code here

    def extract_professors(self, html_content):
        # Extract professors code here

    def extract_additional_links(self, professor_url):
        # Extract additional links code here

    # Other methods for API calls
```

# ProcessCentricLayer: Orchestrates the flow between data, business logic, and adapter layers. Provides CLI and GUI interfaces.
```python
class ProcessCentricLayer:
    def __init__(self):
        # Initialization code here

    def process_department(self, department_name):
        # Department processing code here

    def show_professor_images(self, department_name):
        # Show professor images code here

    def main(self):
        # GUI setup code here

    def cli_main(self):
        # CLI setup code here
```

# Main Execution
```python
if __name__ == "__main__":
    # Main execution code here
```

## Contributing
As this project is part of a university course, contributions are limited to me and course instructors. However, feedback and suggestions from other students or faculty members are always welcome. If you have any ideas or notice any issues, please feel free to reach out to us directly or raise an issue in the project repository.

## License
This project is developed as part of an academic course and is meant for educational purposes only. The code and documentation are not licensed for commercial use or distribution outside of the university course. All rights are reserved by the authors and the university. Unauthorized copying, modification, distribution, or use of this software is strictly prohibited unless permitted by the course instructors.



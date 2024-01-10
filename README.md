
# University Research Department Visualization Tool

## Overview

This Python script provides a comprehensive solution for extracting, processing, and visualizing information about research programs and professors at a university. It integrates web scraping, database management, natural language processing, and image generation using various technologies.

## Dependencies

- Gradio: For creating a GUI interface.
- SQLite: For database operations.
- BeautifulSoup: For HTML parsing.
- AsyncChromiumLoader from langchain: For asynchronous web page loading.
- OpenAI's GPT-4 and DALL-E models: For text generation and image synthesis.
- Python Standard Libraries: json, re, os, sys, subprocess, base64.
- PIL: For image handling.
- requests: For making HTTP requests.
- asyncio and nest_asyncio: For asynchronous programming.
- logging: For logging activities and errors.

## Component Overview

### DataLayer

#### Responsibilities
Handles database operations and scrapes research program data.

#### Implementation

```python
class DataLayer:
    def __init__(self):
        self.db_path = 'university_data.db'

    def ensure_db_setup(self):
        # Database setup code here

    def extract_research_programs(self):
        # Web scraping code here
```

### BusinessLogicLayer

#### Responsibilities
Processes department information, extracts professor details, and generates visual summaries.

#### Implementation

```python
class BusinessLogicLayer:
    def __init__(self, adapter_layer):
        self.adapter_layer = adapter_layer

    def process_department(self, department_name, research_programs):
        # Department processing code here

    def summarize_professor_info(professor_data):
        # Professor info summarization code here
```

### AdapterLayer

#### Responsibilities
Handles OpenAI API interactions and manages web scraping tasks.

#### Implementation

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

### ProcessCentricLayer

#### Responsibilities
Orchestrates the flow between data, business logic, and adapter layers. Provides CLI and GUI interfaces.

#### Implementation

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

### Main Execution

The script supports both CLI and GUI modes, determined by command line arguments. Logging is set up at the beginning of the main execution block.

```python
if __name__ == "__main__":
    # Main execution code here
```

## Usage

### CLI Mode
Run the script with `--cli` argument to interact via the command line.

### GUI Mode
Run the script without arguments to launch the Gradio interface for interactive use.

import os
import sys
import subprocess
import json
import requests

CONFIG_FILE_NAME = 'readme_config.json'
API_CONFIG_FILE = 'config.json'

def run_nimblex_command(project_path):
    command = ["nimblex", "-d"]
    
    process = subprocess.Popen(command, cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error running Nimblex: {stderr.strip()}")
        sys.exit(1)

    if not stdout.strip():
        print("No output received from Nimblex. Ensure you are in the correct project directory.")
        sys.exit(1)

    return stdout

def parse_nimblex_output(output):
    lines = output.splitlines()
    project_structure = {}
    current_dir = None

    for line in lines:
        if line.startswith(' '):
            if 'Functions/Methods:' in line:
                current_dir = line.split(':')[0].strip()
                project_structure[current_dir] = []
            elif current_dir:
                project_structure[current_dir].append(line.strip())
        else:
            project_structure[line.strip()] = []

    return project_structure

def generate_markdown(project_structure):
    markdown_content = "# Project Structure\n\n"

    for item, methods in project_structure.items():
        markdown_content += f"## {item}\n"
        if methods:
            markdown_content += "### Functions/Methods:\n"
            for method in methods:
                markdown_content += f"- {method}\n"
        markdown_content += "\n"

    return markdown_content

def create_empty_config(project_path):
    config = {
        "description": "",
        "usage_example": "",
        "installation": "",
        "contributing": "",
        "license": ""
    }

    config_file_path = os.path.join(project_path, CONFIG_FILE_NAME)
    with open(config_file_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)

    print(f"\033[92mConfiguration file created at {config_file_path}. Please edit this file to update project details.\033[0m")
    print("\033[93mAfter updating, use the 'generate' command to create the README.\033[0m")

def load_api_key():
    if os.path.isfile(API_CONFIG_FILE):
        with open(API_CONFIG_FILE, 'r') as api_config_file:
            api_config = json.load(api_config_file)
            return api_config.get("api_key")
    else:
        return None

def save_api_key(api_key):
    with open(API_CONFIG_FILE, 'w') as api_config_file:
        json.dump({"api_key": api_key}, api_config_file, indent=4)
    print("API key saved successfully.")

def call_llm_api(prompt):
    api_key = load_api_key()
    if not api_key:
        print("Error: API key is not configured. Please set it using the 'set_api_key' command.")
        sys.exit(1)

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    params = {
        "key": api_key
    }

    response = requests.post(url, headers=headers, json=data, params=params)

    if response.status_code == 200:
        response_json = response.json()
        print("API Response:", response_json)  # Debugging: Print the full API response
        
        try:
            return response_json['candidates'][0]['content']['parts'][0]['text']
        except (IndexError, KeyError) as e:
            print(f"Error accessing response content: {e}")
            return ""
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return ""

def read_prompt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main():
    if len(sys.argv) < 2:
        print("Usage: reado <command> [args]")
        return

    command = sys.argv[1]

    if command == "set_api_key":
        if len(sys.argv) != 3:
            print("Usage: reado set_api_key <your_api_key>")
            return
        api_key = sys.argv[2]
        save_api_key(api_key)
        return

    project_path = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()  # Use current directory if no path is provided

    if command == "init":
        if not os.path.isdir(project_path):
            print(f"Error: {project_path} is not a valid directory.")
            return
        create_empty_config(project_path)
        return

    if command != "generate":
        print("Unknown command. Use 'init' to create a config file, 'generate' to create a README, or 'set_api_key' to configure the API key.")
        return

    if not os.path.isdir(project_path):
        print(f"Error: {project_path} is not a valid directory.")
        return

    project_name = os.path.basename(os.path.normpath(project_path))  # Get project name from folder
    print(f"Project Name: {project_name}")

    print("Running Nimblex to get project structure...")
    print("Press ENTER to continue ...")
    output = run_nimblex_command(project_path)
    
    project_structure = parse_nimblex_output(output)
    markdown_content = generate_markdown(project_structure)

    # Load configuration if it exists
    config_file_path = os.path.join(project_path, CONFIG_FILE_NAME)
    if os.path.isfile(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
    else:
        print(f"Warning: Configuration file '{CONFIG_FILE_NAME}' not found. Please run 'init' first.")
        return

    # Read the prompt from the file
    prompt_template = read_prompt_file('prompt.txt')

    # Create the full prompt using config details
    full_prompt = (
        f"{prompt_template}\n\n"
        f"## Project Description\n{config['description']}\n\n"
        f"## Usage Example\n{config['usage_example']}\n\n"
        f"## Installation\n{config['installation']}\n\n"
        f"## Contributing\n{config['contributing']}\n\n"
        f"## License\n{config['license']}\n\n"
        f"Here is the project structure:\n\n{markdown_content}\n\n"
        "This README was made using Model gemini-1.5-flash by Tool README_GENERATOR developed by Pezhvak."
    )

    # Call LLM API and get refined content
    refined_content = call_llm_api(full_prompt)

    if not refined_content:
        print("No content returned from LLM. Please check the API call.")
        return

    # Write the refined content to README.md
    output_path = os.path.join(project_path, 'README.md')
    with open(output_path, 'w') as readme_file:
        readme_file.write(refined_content)

    print(f"README generated and saved as {output_path}")

if __name__ == "__main__":
    main()


# Reado: Your Automated README Generator

  

## Introduction

  

Reado is a compatible command-line interface (CLI) tool designed to streamline the creation of professional-grade README files. Tired of manually writing READMEs? Reado automates the process by  analyzing your project's structure and content, generating a comprehensive and well-formatted README in seconds. Simply point Reado at your project, and it will handle the rest, ensuring your project is well-documented and easily understood by others. Reado leverages the power of the Google Gemini 1.5 Flash model to produce high-quality, informative README files.

  

## Installation

  

Installing Reado is simple and straightforward. Ensure you have Python 3 installed on your system. Then, use pip to install the package:
```bash
sudo  pip  install  reado
``` 

This will install Reado and its dependencies. You'll then need to set your [Google Gemini API](https://aistudio.google.com/) key (see [Usage](#usage) for details).

  

## Usage

  

Reado offers a streamlined workflow to generate your README. Follow these steps:

  

1.  **Set your API Key:** Before using Reado, you must set your Google Gemini API](https://aistudio.google.com/) key. This key grants Reado access to the Gemini 1.5 Flash model. Use the following command, replacing `<YOUR_Gemini_API>` with your actual API key:
```bash
reado  set_api_key  <YOUR_Gemini_API>
```
2.  **Initialize the Project:** After setting your API key, initialize Reado within your project's root directory:
```bash
reado  init
```
This command creates the necessary configuration files. After running this command, a file named `readme_config.json` with the following structure is generated:
```json
"description": "<Write a brief description of your project.>",

"usage_example": "First , Second , ...",

"installation": "ex: pip install <YOUR-PrOJECT-NAME> ",

"contributing": "",

"license": ""

```
**Completing this information is required to create a README.**

  

3.  **Generate the README:** Finally, generate the README file:
```bash
reado  generate
```

  

Reado will Extract your project's structure using [Nimblex](https://pypi.org/project/nimblex), identify key components, and generate a comprehensive README.md file in your project's root directory. Ensure that Google services are supported in your region for successful operation. Reado must be run from the root directory of your project.


## Contributing
i welcome contributions to Reado! 
  

## License

Reado is licensed under the MIT License. See the [LICENSE](https://github.com/pezhvak98/Reado/blob/main/LICENSE) file for more details.

  
  

<br>

<font  size="1">This README was made using READO</font>
<div style="text-align: center;">
  <img src="https://raw.githubusercontent.com/Vishnuk4906/zohencel-ai-utils/main/zailogo.PNG" alt="Zohencel-AI Logo" style="max-width:150px; max-height:80px;">
</div>

# Zohencel-AI

[![PyPI version](https://img.shields.io/pypi/v/zohencel-ai)](https://pypi.org/project/zohencel-ai/)
[![Downloads](https://pepy.tech/badge/zohencel-ai)](https://pepy.tech/project/zohencel-ai)
[![Python Versions](https://img.shields.io/pypi/pyversions/zohencel-ai)](https://pypi.org/project/zohencel-ai/)
[![License](https://img.shields.io/pypi/l/zohencel-ai)](https://pypi.org/project/zohencel-ai/)


**Zohencel-AI** is a Python library designed to simplify the development of voice assistants, chatbots, and analytical tools. With built-in modules and functions, `zohencel-ai` provides an easy-to-use interface for building advanced AI solutions without the complexity.

---

## This is where the search ends!

## HOME PAGE & DOCUMENTATION
- https://zohencelai.github.io/

### What is new?
- **Added Groq api key as optional parameter**:user can use their on api key to avoid rate limits. We still have the inbuilt api key if user doesn't have one. But the package have been using by more developers now, so there is a chance it may cross the token limit defined by groq.
- Get your key now : https://console.groq.com/keys

### Key Features
- **Voice Assistant Tools**: Voice assistant in single import.
- **Data Analysis**: Data analytics tool to visualize and query data in natural language.

---

## Installation

To install `zohencel-ai`, use the following pip command:

```bash
pip install zohencel-ai
```
---

## AI Voice Assistant

The `VoiceAssistant` in `Zohencel-AI` provides a customizable, voice-enabled assistant that listens to user input, processes it, and responds with spoken text. Designed to be adaptable, the assistants attributes—such as name, tone, purpose, and voice type—can be tailored to fit a wide range of use cases, making it suitable for personalized or business-focused applications.

### Key Customizations
- **Assistant Name**: Set a unique name for the assistant, making interactions feel more personalized and relatable.
- **User Name**: Personalize responses by specifying the user’s name, enhancing engagement.
- **Tone and Duty**: Define the assistant’s tone and duty with an optional description. For example, set it as a "helpful and friendly guide" or an "informative support assistant" to adjust the assistant's personality.
- **Voice Type**: Choose between a ‘male’ or ‘female’ voice to best suit the assistant's character and user preferences.

### Usage Example

Here's how to configure these options when creating and running your assistant:

```python
from zohencel_ai import VoiceAssistant

# Initialize the VoiceAssistant
assistant = VoiceAssistant()

# Run the assistant with custom settings
assistant.run(
    voice='female',                # Voice type: 'female' or 'male'
    assistant_name='Zohencel',     # Assistant's name
    user_name='Alex',              # User's name for personalized responses
    description='I am here as your friendly and reliable AI guide.'  # Assistant's tone and purpose
)
```
- all the parameters are optional and you can just run it by calling assistant.run() 


# Chart Bot 

**Chart Bot** is your ultimate data companion! Whether you're a beginner or a seasoned professional, this intelligent tool simplifies the process of understanding, querying, and visualizing your data. Designed with accessibility and functionality in mind, Chart Bot empowers users to harness the full potential of their data without the steep learning curve of advanced libraries like Matplotlib and Seaborn.  

---
Start using **Chart Bot** with just a few lines of code:  

```python
from zohencel_ai.analysis import Analysischartbot

bot = Analysischartbot()
bot.run()
```
## Key Features

- **Effortless Data Exploration**: Understand your dataset with simple queries—no coding expertise required!
- **Intelligent Visualizations**: Generate beautiful, insightful charts and graphs for machine learning processes like Exploratory Data Analysis (EDA).
- **Beginner-Friendly**: Ideal for users unfamiliar with visualization tools like Matplotlib or Seaborn.
- **Preprocessing Made Easy**: Simplify common ML preprocessing tasks, such as:
  - Feature engineering
  - Missing value treatment
  - Distribution analysis
- **Seamless Workflow**: Save time and effort by streamlining the data understanding process before diving into modeling.

---

## 🔧 How It Works

1. **Upload Your Data**: Provide your dataset in a compatible format (CSV, Excel, etc.).
2. **Query the Data**: Use intuitive commands to filter, analyze, and understand your data.
3. **Visualize**: Create stunning charts and graphs to uncover trends and distributions.
4. **Preprocess**: Execute essential ML preprocessing tasks with built-in tools.
5. **Limitations**: Memory context is not available in the current version, it will be in the upcoming version.So provide the query in full contetxt.
## 📸 Sample Images

Here are some demo images showcasing the functionality of **Chart Bot** using Titanic dataset:

1. **Sample 1**:  
![Sample 1](https://raw.githubusercontent.com/Vishnuk4906/zohencel-ai-utils/main/demo_1.png)

2. **Sample 2**:  
![Sample 2](https://raw.githubusercontent.com/Vishnuk4906/zohencel-ai-utils/main/demo_2.png)

## Upcoming Features

I'm excited to introduce **ML Bot**, an intelligent assistant that will help you train and test machine learning models end-to-end, all through simple queries. 

- **End-to-End ML Workflow**: From data preprocessing to model testing, perform everything using easy-to-understand queries.
- **Train Models**: Automatically train machine learning models by simply instructing the bot.
- **Model Testing**: Test and evaluate models with built-in performance metrics and visualizations.
- **Query-Based Interaction**: No coding required—just query the bot for tasks like training a model, evaluating performance, and preprocessing data.

Stay tuned as we release this powerful tool to make machine learning workflows seamless and accessible to everyone!

## Author

### Vishnu K

A passionate AI/ML developer with a strong zeal for innovation and learning. I believe in exploring new technologies and enhancing my knowledge every day. My journey revolves around creating impactful solutions through the power of AI and Machine Learning.

Feel free to connect with me!

[LinkedIn](https://www.linkedin.com/in/vishnu-k-8a058425b/) | [Gmail](mailto:vishnuknandanam@gmail.com) | [GitHub](https://github.com/Vishnuk4906)




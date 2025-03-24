# AI Chatbot Application

This is a Streamlit-based AI chatbot application that uses Ollama for natural language processing.

## Prerequisites

1. Install Python 3.8 or higher:
   - Download and install from [Python](https://www.python.org/downloads/)
   - Make sure Python is added to your system PATH

2. Install Ollama:
   - Download and install from [Ollama](https://ollama.ai/download)
   - After installation, pull the required models:
     ```bash
     ollama pull deepseek-r1
     ollama pull gemma3
     ollama pull llama3.2
     ollama pull llava
     ```

## Running the Application

1. Clone this repository:
   ```bash
   git clone <your-repository-url>
   cd ai-chatbot
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run Home.py
   ```

4. Access the application:
   - Open your web browser
   - Go to `http://localhost:8501`

## Important Notes

- Make sure Ollama is running on your machine before starting the application
- The application requires the following models to be installed via Ollama:
  - DeepSeek-R1
  - Gemma 3
  - Llama 3.2
  - LLaVA
- The application runs on port 8501 by default

  Now you'll access the landing page
  ![image](https://github.com/user-attachments/assets/cdbc63d1-0c33-4994-ba59-e3160e0225ef)
  there after scroll down to and you'll meet a signup /login button when pressed it moves to the expander
  ![image](https://github.com/user-attachments/assets/22d6008d-8fbd-4547-a11e-db99d2129e15)
  signup if you are a new user or login if you have used the site before
  then access the welcome page
  ![image](https://github.com/user-attachments/assets/ed80dcbb-336f-4ebd-8575-b80139ef70f1)
  from here choose the bot you want to use
  example deepseek
  ![image](https://github.com/user-attachments/assets/bfeab6e5-2701-47ed-9038-e881a922bc6a)
  ask any question then wait for deepseek to respond the speed entirely depends on your device specifications



  


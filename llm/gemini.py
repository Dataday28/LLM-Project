import google.generativeai as genai
import yaml
import os


current_dir = os.path.dirname(__file__)
config_yml = os.path.join(current_dir, 'config.yml')

config = yaml.safe_load(open(config_yml))

# Gemini

# API KEY de Gemini
GOOGLE_API_KEY = config["GOOGLE_API_KEY"]

gemini_key = GOOGLE_API_KEY

client = genai.configure(api_key=gemini_key)

# Configuracion del modelo de AI
def get_response(prompt, model=genai.GenerativeModel('gemini-1.5-flash')):
    response = model.generate_content(prompt)
    return response.text

def get_response_creative(prompt, model=genai.GenerativeModel('gemini-1.5-flash'), temperature=0.7):
    response = model.generate_content(prompt)
    return response.text
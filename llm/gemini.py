import google.generativeai as genai

# Gemini

# API KEY de Gemini
GOOGLE_API_KEY = "AIzaSyALHW5Qvf53ivMtKfu0uZXMIe9IbKXeqx8"

gemini_key = GOOGLE_API_KEY

client = genai.configure(api_key=gemini_key)

# Configuracion del modelo de AI
def get_response(prompt, model=genai.GenerativeModel('gemini-1.5-flash')):
    response = model.generate_content(prompt)
    return response.text

def get_response_creative(prompt, model=genai.GenerativeModel('gemini-1.5-flash'), temperature=0.7):
    response = model.generate_content(prompt)
    return response.text
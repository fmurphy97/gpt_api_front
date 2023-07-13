import pdfplumber
import requests
import codecs


def read_text_file(file_path, encoding='utf-8'):
    """Function to exctract text from a txt file"""
    with codecs.open(file_path, 'r', encoding) as file:
        text = file.read()
    return text


def extract_text_from_pdf(file_path):
    """Function to extract text from a PDF file.
    Args:
        file_path (str): Path to the PDF file.
    Returns:
        str: Extracted text from the PDF.
    """
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


def ask_question(context, question, openai_api_key, model):
    """Function to ask a question using OpenAI's chat-based API.
    Args:
        context (str): Conversation context.
        question (str): User's question.
        openai_api_key (str): OpenAI api key
    Returns:
        str: Assistant's answer.
    """
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    api_url = "https://api.openai.com/v1/chat/completions"

    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": context},
        {"role": "user", "content": question}
    ]

    payload = {
        "model": model,
        "messages": conversation
    }

    response = requests.post(api_url, headers=headers, json=payload)
    response_json = response.json()
    if "error" in response_json.keys():
        assistant_reply = response_json['error']["message"]
    else:
        assistant_reply = response_json['choices'][0]['message']['content']
    return assistant_reply

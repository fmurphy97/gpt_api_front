import pdfplumber
import requests
import codecs


def read_text_file(file_path, encoding='utf-8'):
    """Function to extract text from a txt file"""
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


def ask_question(messages, openai_api_key, model, context=None):
    """Function to ask a question using OpenAI's chat-based API.
    Args:
        context (str): Conversation context.
        messages (list[dict[str,str]]): The past messages of the conversation, in the format of role and context
        openai_api_key (str): OpenAI api key
        model (str): which is the model that will be used to process the prompt into an answer
    Returns:
        str: Assistant's answer.
    """
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    api_url = "https://api.openai.com/v1/chat/completions"

    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    conversation.extend(messages)
    if context:
        conversation.append({"role": "user", "content": context})

    payload = {"model": model, "messages": conversation}

    response = requests.post(api_url, headers=headers, json=payload)
    response_json = response.json()
    if "error" in response_json.keys():
        assistant_reply = response_json['error']["message"]
    else:
        assistant_reply = response_json['choices'][0]['message']['content']
    return assistant_reply

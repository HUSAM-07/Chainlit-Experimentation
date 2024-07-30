import chainlit as cl
import openai
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch API keys from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
rapidapi_key = os.getenv('RAPIDAPI_KEY')
rapidapi_host = os.getenv('RAPIDAPI_HOST')

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

openai.api_key = openai_api_key

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Brio Introduction Email",
            message="Please provide the client's name and LinkedIn URL to create an introduction email for Brio Technologies.",
            icon="/public/idea.svg",
        ),
        cl.Starter(
            label="GCP Marketing Campaign",
            message="Please provide the client's name and LinkedIn URL to create a GCP Marketing Campaign email.",
            icon="/public/learn.svg",
        ),
        cl.Starter(
            label="Azure Marketing Email",
            message="Please provide the client's name and LinkedIn URL to create an Azure Marketing Campaign email.",
            icon="/public/terminal.svg",
        ),
        cl.Starter(
            label="Microsoft 365 Marketing Email",
            message="Please provide the client's name and LinkedIn URL to create a Microsoft 365 Marketing Campaign email.",
            icon="/public/write.svg",
        ),
    ]

def scrape_linkedin_profile(linkedin_url):
    url = f"https://{rapidapi_host}/v2/person"
    querystring = {"url": linkedin_url}
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": rapidapi_host,
    }
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    return response.json()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.strip().split('\n')
    client_name = user_input[0].strip()
    linkedin_url = user_input[1].strip()

    # Scrape LinkedIn profile
    profile_data = scrape_linkedin_profile(linkedin_url)

    # Extract necessary information from profile data
    profile_summary = profile_data.get('summary', 'No summary available.')

    # Construct the prompt for email creation
    prompt = f"Create an email introducing Brio Technologies to {client_name}. The LinkedIn profile summary is: {profile_summary}"

    # Generate email using OpenAI
    response = openai.Completion.create(
        engine=settings["model"],
        prompt=prompt,
        temperature=settings["temperature"],
        max_tokens=settings["max_tokens"],
        top_p=settings["top_p"],
        frequency_penalty=settings["frequency_penalty"],
        presence_penalty=settings["presence_penalty"],
    )

    await message.reply(response.choices[0].text.strip())

if __name__ == "__main__":
    cl.run()

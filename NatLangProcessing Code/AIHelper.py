from openai import OpenAI
import os
from dotenv import load_dotenv

import DBHelper

DEBUGGING = True
client = None
tableInfo = "No tables"

def initClient():
    global client
    if client is None:
        load_dotenv()
        MY_API_KEY = os.getenv('OPENAI_API_KEY')

        client = OpenAI(
            # This is the default and can be omitted
            api_key=MY_API_KEY,
        )

def promptAI(prompt):

    initClient()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    responseMessage = chat_completion.choices[0].message.content

    if DEBUGGING:
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("Prompt: \n" + prompt)
        print()
        print("Response: \n " + responseMessage)
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    return responseMessage

def askAI(prompt):
    global tableInfo
    newPrompt = prompt
    newPrompt += "\n"
    newPrompt += "Please return only the SQLite (do not provide explanations or any other words, "
    newPrompt += "since this is being used to import SQL directly into a db query). Additionally, only return "
    newPrompt += "one query. Here are the tables we are using: " + tableInfo + "\nThanks!"
    return promptAI(newPrompt)

def getNiceResponse(result, userInput):
    newPrompt =  "Please show the following list in a nicely formatted table. But, format your response so that it"
    newPrompt += " sounds like an answer to this prompt: " + userInput + "\n" + "Also be friendly, please! "
    newPrompt += "If the list is empty, instead say something like \"Sorry, no items matching your request were found.\"\n"
    newPrompt += str(result)
    return promptAI(newPrompt)

def storeTableInfo():
    global tableInfo
    tableInfo = DBHelper.getTableInfo()
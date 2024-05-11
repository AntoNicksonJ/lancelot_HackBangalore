import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from bs4 import BeautifulSoup
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import json
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent
import autogen


load_dotenv()
os.environ['AUTOGEN_USE_DOCKER'] = 'False'
serper_api_key = os.getenv("SERP_API_KEY")
airtable_api_key = os.getenv("AIRTABLE_API_KEY")
config_list = config_list_from_json("OAI_CONFIG_LIS.json")

# ------------------ Create functions ------------------ #

# Function for google search


def google_search(search_keyword):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": search_keyword
    })
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("RESPONSE:", response.text)
    return response.text
# print(google_search("how good is the A350 from the B777"))

# Function for scraping


def summary(objective, content):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    map_prompt = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "objective"])

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=False
    )

    output = summary_chain.run(input_documents=docs, objective=objective)

    return output


def scrap_web(objective: str, url: str):
    print("Scrapping from Website...")

    driver.get(url)
    driver.implicitly_wait(10)
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    text = soup.get_text()

    # print("CONTENT: ", text)
    print("Scrapping done")

    if len(text) > 10000:
        output = summary(objective, text)
        return output
    else:
        return text

# Function for get airtable records


def get_airtable_records(base_id, table_id):
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

    headers = {
        'Authorization': f'Bearer {airtable_api_key}',
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return data


# Function for update airtable records

def update_single_airtable_record(base_id, table_id, id, fields):
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

    headers = {
        'Authorization': f'Bearer {airtable_api_key}',
        "Content-Type": "application/json"
    }

    data = {
        "records": [{
            "id": id,
            "fields": fields
        }]
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data))
    data = response.json()
    return data


# ------------------ Create agent ------------------ #

# Create user proxy agent
user_proxy = UserProxyAgent(name="user_proxy",
                            is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
                            human_input_mode="ALWAYS",
                            max_consecutive_auto_reply=1
                            )

# Create researcher agent
researcher = GPTAssistantAgent(
    name="researcher",
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_pGiJsR6t5pl2jp6QFF2vbxD6"
    }
)

researcher.register_function(
    function_map={
        "web_scraping": scrap_web,
        "google_search": google_search
    }
)

# Create research manager agent
research_manager = GPTAssistantAgent(
    name="research_manager",
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_LKbkxRcqk3Ya4Ykv2zJSI7oI"
    }
)


# Create director agent
director = GPTAssistantAgent(
    name="director",
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_TjFYpkNIOGhzZkzowWg0nVAT",
    }
)

director.register_function(
    function_map={
        "get_airtable_records": get_airtable_records,
        "update_single_airtable_record": update_single_airtable_record
    }
)


# Create group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, researcher, research_manager], messages=[], max_round=15)
group_chat_manager = autogen.GroupChatManager(
    groupchat=groupchat, llm_config={"config_list": config_list})


# ------------------ start conversation ------------------ #
# message = """
# Research the funding stage/amount & pricing for each company in the list: https://airtable.com/appj0J4gFpvLrQWjI/tblF4OmG6oLjYtgZl/viwmFx2ttAVrJm0E3?blocks=hide
# # """
user_proxy.initiate_chat(
    group_chat_manager, message="First Search and Scrap the content the search and have the detailed about from about e-vehicles done only once and have a discussion on it")

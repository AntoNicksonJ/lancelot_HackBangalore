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
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
load_dotenv()
serper_api_key = os.getenv("SERP_API_KEY")
airtable_api_key = os.getenv("AIRTABLE_API_KEY")
config_list = config_list_from_json("OAI_CONFIG_LIST")


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
    options = Options()
    options.add_argument('--headless')  # Adds the headless option

# Initialize the Chrome WebDriver with the specified options
    driver = webdriver.Chrome(options=options)

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
researcher_A = GPTAssistantAgent(
    name="researcher_A",
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_pGiJsR6t5pl2jp6QFF2vbxD6"
    }
)

researcher_A.register_function(
    function_map={
        "web_scraping": scrap_web,
        "google_search": google_search
    }
)

# Create research manager agent
researcher_B = GPTAssistantAgent(
    name="researcher_B",
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_LKbkxRcqk3Ya4Ykv2zJSI7oI"
    }
)

researcher_B.register_function(
    function_map={
        "web_scraping": scrap_web,
        "google_search": google_search
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
    agents=[user_proxy, researcher_B, researcher_A], messages=[], max_round=30)
group_chat_manager = autogen.GroupChatManager(
    groupchat=groupchat, llm_config={"config_list": config_list})


# ------------------ start conversation ------------------ #
# message = """
# Research the funding stage/amount & pricing for each company in the list: https://airtable.com/appj0J4gFpvLrQWjI/tblF4OmG6oLjYtgZl/viwmFx2ttAVrJm0E3?blocks=hide
# # """
user_proxy.initiate_chat(group_chat_manager, message='''Fressen Catering is positioned to capitalize on the evolving landscape of kosher catering in Philadelphia. The market is experiencing a notable shift towards healthier and organic kosher options, aligning with contemporary dietary preferences. Fressen recognizes this trend and aims to fill a unique niche by introducing innovative menu offerings that challenge traditional notions of kosher cuisine. Unlike many competitors who cater to specific income brackets, Fressen plans to serve both middle-class and upper-class clientele, catering to varying budget levels and culinary preferences within the kosher community.

What sets Fressen apart is its unwavering commitment to customer satisfaction and its innovative culinary approach. By prioritizing exceptional service and creativity in menu development, Fressen seeks to establish itself as a preferred choice for kosher catering in Philadelphia. Furthermore, the company has carefully projected its financial trajectory, forecasting profitability by the third year of operation and outlining a clear plan to repay its initial investment. With Susan's personal investment of $40,000 and additional support from friends and family totaling $90,000, Fressen is well-positioned to secure the necessary financing.

Through a strategic blend of marketing efforts, customer-centric service, and culinary innovation, Fressen aims to not only meet but exceed the expectations of Philadelphia's kosher clientele. By fostering lasting relationships with customers and delivering exceptional dining experiences, Fressen endeavors to become a prominent fixture in the city's thriving kosher catering scene.''')

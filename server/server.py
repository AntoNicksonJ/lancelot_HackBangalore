from dotenv import load_dotenv
from langchain_community.vectorstores.faiss import FAISS
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
# from htmlTemplates import css, bot_template, user_template
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib


import os
from typing import Annotated, List, Tuple, Union
from langchain.tools import BaseTool, StructuredTool, Tool
from langchain_experimental.tools import PythonREPLTool
from langchain_core.tools import tool
import random
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from bs4 import BeautifulSoup
import requests
import json
from langchain.schema import SystemMessage
from typing import Any, Callable, List, Optional, TypedDict, Union
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from langgraph.graph import END, StateGraph
from typing import Any, Callable, List, Optional, TypedDict, Union

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
# from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from typing import Annotated, List, Tuple, Union
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langsmith import trace


@tool("scrap_web", return_direct=False)
def scrap_web(url: str):
    """Returns the contents from a website, input the web site link"""
    print("Scrapping from Website...")
    print(url)

    options = Options()
    options.add_argument('--headless')
    # options.addArguments("--no-sandbox")
    # options.add_argument('--remote-debugging-pipe')

    # Adds the headless option
    # options.addArguments("--disable-dev-shm-usage")

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
    # print(text[:100])

    # return text[:10000]
    # print(text)
    text1 = [line.strip() for line in text]

    text1 = text1[:10003]
    if len(text1) > 10000:
        print("return")
        output = summary(text)
        output = output[:10000]
        return output

    else:
        return text1


@tool("search", return_direct=False)
def search(query: str) -> list:
    """Returns a list of website links for the given topic. input the topic"""
    url = "https://google.serper.dev./search"

    payload = json.dumps({
        'q': query
    })

    headers = {
        'X-Api-Key': serper_api,
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload)

    # print(response.text)
    print("hi")
    json_string = response.text
    data = json.loads(json_string)
    links = [item['link'] for item in data['organic']]
    return response.text


def summary(content):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=1000,
        chunk_overlap=0
    )
    doc = text_splitter.create_documents([content])
    map_prompt = """
        Write a summary of the folloewing text:
        "{text}"
        SUMMARY:
        """
    map_prompt_template = PromptTemplate(input_variables=["text"],
                                         template=map_prompt)
    summary_chain = load_summarize_chain(llm,
                                         chain_type="map_reduce",
                                         map_prompt=map_prompt_template,
                                         combine_prompt=map_prompt_template,
                                         verbose=False)

    out = summary_chain.run(
        objective="Summarize without losing any key points and values ,remove unwanted terms", input_documents=doc)

    print("SUMMARY done")
    return out


tools = ['search', 'scrap_web']


app = Flask(_name_)


CORS(app)


def get_conversational_chain():

    prompt_template = """
      Here the user input contains the description of their small scale business. You have to find the keywords for the context that the user gives and have to search for the exact top 5 related sehemes provided in the pdf.

for a sample as example 1, If the user input be:
I am a farmer having idea to grow fruits and flowers i.e., Horticulture in my own land. I need loan for getting those requirements.

Now for the above input the llm should search for search for keywords and give output like,

National Horticulture Board

A. Development of Commercial Horticulture
Related Scheme i) Horticulture in Open Field
Description: Rs. 75 lakh per project covering an area of more than 2 to 5 hectares.
Nature of Assistance: Credit linked back-ended subsidy @ 40% of project cost with a ceiling of Rs. 30 lakh.
Who Can Apply: Societies and other organizations which are provided grants-in-aid.
How to Apply: Mission Director and Joint Secretary (NHM), Department of Agriculture & Cooperation, New Delhi.

Related Scheme ii) Horticulture in Protected Cover
Description: Rs. 112 lakh per project covering an area of above 2,500 square meters.
Nature of Assistance: Credit linked back-ended subsidy @ 50% of cost limited to Rs. 56 lakh per project.
Who Can Apply: Societies and other organizations which are provided grants-in-aid.
How to Apply: Mission Director and Joint Secretary (NHM), Department of Agriculture & Cooperation, New Delhi.
Related Scheme iii) Horticulture for Post-Harvest Management Projects
Description: Rs. 145 lakh per project with add-ons like pre-cooling, grading, etc., taken up as individual components.
Nature of Assistance: Credit linked back-ended subsidy @ 35% of cost with a ceiling of Rs. 72.50 lakh.
Who Can Apply: Societies and other organizations which are provided grants-in-aid.
How to Apply: Mission Director and Joint Secretary (NHM), Department of Agriculture & Cooperation, New Delhi.




As example 2, The user input will be like,
I have a plan to start a business ie. is to start hotels for accommodating people in a medium scale. I need a adequate amount to start this business.

Now for the above input the llm should search for search for keywords and give output like,


Related Scheme: Time Share Resorts (TSR)
Description: Voluntary scheme for star classification of fully operational TSR in categories - 5, 4, and 3 stars.
Nature of Assistance: Recognition.
Who Can Apply: Time share resorts.
How to Apply: To Hotel and Restaurants Division, Ministry of Tourism.

Related Scheme: Tented Accommodation
Description: Voluntary scheme for project approval and classification of tented accommodation.
Nature of Assistance: Concession and facilities, after classification.
Who Can Apply: Owners of tented accommodation.
How to Apply: To HRACC, Hotel and Restaurants Division, Ministry of Tourism.

Related Scheme i) Motels Accommodation
Description: Voluntary scheme to benchmark the standards of facilities and services offered by motels.
Nature of Assistance: Approval to motel projects after inspection.
Who Can Apply: Owners of motel accommodation.
How to Apply: To HRACC, Hotel and Restaurants Division, Ministry of Tourism.

Related Scheme ii) Hotels Accommodation
Description: Approval to hotel projects in six categories: from 1-star to 5-star deluxe, based on suitability for international tourists.
Nature of Assistance: Recognition.
Who Can Apply: Hotels for accommodation.
How to Apply: To HRACC, Hotel and Restaurants Division, Ministry of Tourism.


As an example 3, The user input will be like,
I want to be an entrepreneur, I have an idea of creating a software for preprocessing images in large scale and identify the people based on their face. I need financial support and supporting resource.

 Now for the above input the llm should search for search for keywords and give output like,

Related Scheme: National Science & Technology Entrepreneurship Development Board (NSTEDB)
Related Scheme i) Innovation and Entrepreneurship Development Centre (IEDC)
Description: To spread entrepreneurial culture in S&T academic institutions and foster techno-entrepreneurship.
Nature of Assistance: For setting up IEDC in suitable academic institutions.
Who Can Apply: S&T academic institutions.
How to Apply: Head, NSTEDB.

Related Scheme ii) Entrepreneurship Development Cell (EDC)
Description: To provide information and services related to enterprise building for potential S&T entrepreneurs.
Nature of Assistance: Financial assistance for setting up EDC and for meeting recurring expenditure.
Who Can Apply: Universities, colleges, institutions offering science and management courses.
How to Apply: To the Ministry.

Related Scheme iii) Entrepreneurship Development Programme
Description: Training of 6-8 weeks for S&T graduates, in enterprise creation.
Nature of Assistance: Assistance of Rs. 2 lakh.
Who Can Apply: Training and R&D institutions.
How to Apply: Head, NSTEDB.

Related Scheme iv) Science & Technology Entrepreneurship Development (STED)
Description: To achieve socio-economic development through S&T interventions.
Nature of Assistance: Identification of opportunities.
Who Can Apply: TCOs, NGOs, organizations proven in entrepreneurship development.
How to Apply: To Head, NSTEDB.

Related Scheme v) Science & Technology Entrepreneurs/Entrepreneurship Park (STEP)
Description: To re-orient the approach to innovation and entrepreneurship, opening new avenues for starting up.
Nature of Assistance: Offers infrastructure amenities/facilities.
Who Can Apply: Academic and R&D institutions.
How to Apply: To Head, NSTEDB.

Related Scheme vi) Technology Business Incubators (TBI)
Description: Provides a wide range of specialized services to SMEs.
Nature of Assistance: Financial assistance for five years.
Who Can Apply: R&D institutions/academic institutes.
How to Apply: To Head, NSTEDB.
 
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatOpenAI(model='gpt-3.5-turbo-16k', temperature=1)

    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def handle_userinput(user_question):
    embeddings = OpenAIEmbeddings()

    new_db = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True)

    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True)

    return response["output_text"]


def gpt4(i):
    import requests
    import json

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-*****************************************"
    }

    user_prompt = (i)
    data = {
        "model": "gpt-4-turbo-2024-04-09",
        "messages": [{"role": "user", "content": user_prompt}],
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    json_string = response.text
    if json_string is not None:
        dataa = json.loads(json_string)
        d = dataa["choices"][0]["message"]["content"]
        return d
    else:
        return "No Changes Required"


stored_text1 = ""


@app.route('/api/submit1', methods=['POST'])
def submit_text1():
    global stored_text1
    data = request.json
    text = data.get('text', '')
    stored_text1 = text

    if request.method == 'POST':
        input_text = stored_text1
        response = gpt4(f"""A proper Business Proposal Template should contain all the below Attributes with their mentioned objects, but then while human giving their proposal it is not necessary to contain all aspects due to human error.

            1. Cover Page and Table of Contents
            2. Executive Summary - The executive summary shouldn’t include a great deal of financial information. If you have a particularly relevant or striking financial result
            3. Company Description - The company description should include a mission statement, the company principles, any strategic partners, and your corporate structure.
            4. Market Analysis Many business owners engage third-party companies to perform an analysis. If you have, be sure to cite them. If your information comes from published research or a survey, be sure to cite those as well.
            5. Organization and Management - The organization and management section should itemize your company’s management structure. Many business plans provide an organizational chart, a structure description, and salary forecasts.
            6. Service or Product - The service or product section should also include your product/service’s estimated lifecycle, and any research and development completed, in progress, or planned. Naturally, this section will vary greatly depending on your type of business. It should also include a description of any trademarks, patents, or other intellectual property rights, if applicable.
            7. Marketing and Sales - The marketing and sales section includes three vital pieces of information:
            8. Financial Analysis - The financial projections must include
            9. Funding Request - Here’s one way you can structure your funding request:
                
            10. Appendix - Appropriate appendix materials include

            So as a result , if the input fails to satisfy all the above aspects then mention those particular aspects back asking the fill them.

            Output is the missing aspects from the Proposal.

            The above mentioned title are the basics for a Business Proposal. Now user give you his report you have to check whether it have satisfied all the above mentioned aspects

            the user input is {input_text}
            """)

        return jsonify({'text': response}), 200


# @app.route('/api/display1', methods=['GET'])
# def display_text1():
#     global stored_text1
#     return jsonify({'text': stored_text1})


# @app.route('/api/save-data', methods=['POST'])
# def save_data():
#     data = request.json
#     input_value = data.get('inputValue')
#     return input_value


@app.route('/send-email', methods=['POST'])
def send_email():
    email = "22d106@psgitech.ac.in"
    receive = "nicksonjj55@gmail.com"
    subject = "PROS CONES AND OTHER DETAILS FOR "  # Predefined subject
    message = save_data()  # Predefined message

    text = f"Subject: {subject}\n\n{message}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, "ihnmjpxlkjmibkqx")
        server.sendmail(email, receive, text)
        server.quit()

        return 'Email sent successfully', 200
    except Exception as e:
        print("Error:", e)
        return 'Email sent successfully', 200


stored_text2 = ""  # Variable to store text 2


@app.route('/api/submit2', methods=['POST'])
def submit_text2():
    global stored_text2
    data = request.json
    text = data.get('text', '')
    stored_text2 = text

    #
    if request.method == 'POST':
        input_text = stored_text1
        ans = impo(input_text)
        return jsonify({'text': ans})


# @app.route('/api/display2', methods=['GET'])
# def display_text2():
#     global stored_text2
#     return jsonify({'text': stored_text2})

# if _name_ == '_main_':
#     app.run(debug=True)


def impo(x):
    os.environ["OPENAI_API_KEY"] = "sk-******************************************"
    os.environ["LANGCHAIN_API_KEY"] = "****************************************"
    serper_api = os.environ["SERP_API_KEY"] = "**************************************"

    def create_agent(
        llm: ChatOpenAI,
        tools: list,
        system_prompt: str,
    ) -> str:
        """Create a function-calling agent and add it to the graph."""
        system_prompt += "\nWork autonomously according to your specialty, using the tools available to you."
        " Do not ask for clarification."
        " Your other team members (and other teams) will collaborate with you with their own specialties."
        " You are chosen for a reason! You are one of the following team members: {team_members}."
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt,
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools)
        return executor

    def agent_node(state, agent, name):
        result = agent.invoke(state)
        return {"messages": [HumanMessage(content=result["output"], name=name)]}

    def create_team_supervisor(llm: ChatOpenAI, system_prompt, members) -> str:
        """An LLM-based router."""
        options = ["FINISH"] + members
        function_def = {
            "name": "route",
            "description": "Select the next role.",
            "parameters": {
                "title": "routeSchema",
                "type": "object",
                "properties": {
                    "next": {
                        "title": "Next",
                        "anyOf": [
                            {"enum": options},
                        ],
                    },
                },
                "required": ["next"],
            },
        }
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, who should act next?"
                    " Or should we FINISH? Select one of: {options}",
                ),
            ]
        ).partial(options=str(options), team_members=", ".join(members))
        return (
            prompt
            | llm.bind_functions(functions=[function_def], function_call="route")
            | JsonOutputFunctionsParser()
        )

    # tavily_tool = TavilySearchResults(max_results=5)

    def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
        # Each worker node will be given a name and some tools.
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt,
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_tools_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools)
        return executor

    def agent_node(state, agent, name):
        result = agent.invoke(state)
        return {"messages": [HumanMessage(content=result["output"], name=name)]}

    from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    members = ["Researcher", "Coder"]
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        " following workers:  {members}. Given the following user request,"
        "if coder replies send the conversation to researcher "
        "if researcher replies send the conversation to coder"
        "Finish when both of reply atleast twice"
    )
    # Our team supervisor is an LLM node. It just picks the next agent to process
    # and decides when the work is completed
    options = ["FINISH"] + members
    summary_content = "I am going to search fo rtreasure near my land because i am very lame"
    # Using openai function calling can make output parsing easier for us
    # function_def = {
    #     "name": "route",
    #     "description": "Select the next role.",
    #     "parameters": {
    #         "title": "routeSchema",
    #         "type": "object",
    #         "properties": {
    #             "next": {
    #                 "title": "Next",
    #                 "anyOf": [
    #                     {"enum": options},
    #                 ],
    #             }
    #         },
    #         "required": ["next"],
    #     },
    # }
    function_def = {
        "name": "route",
        "description": "Select the next role and provide an additional message.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [
                        {"enum": options},
                    ],
                },
                "message": {
                    "title": "Message",
                    "type": "string",
                    "description": "An additional message to provide context or information."
                }
            },
            # Both 'next' and 'message' are required
            "required": ["next", "message"],
        },
    }

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            # Add the summary content as part of the system's messages
            ("system", summary_content),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we FINISH? Select one of: {options}",
            ),
        ]
    ).partial(options=str(options), members=", ".join(members))

    llm = ChatOpenAI(model="gpt-4-turbo-2024-04-09")
    # llm2 = ChatOpenAI(model="gpt-3.5-turbo")
    llm2 = ChatOpenAI(model="gpt-4-turbo-2024-04-09")

    supervisor_chain = (
        prompt
        | llm.bind_functions(functions=[function_def], function_call="route")
        | JsonOutputFunctionsParser()
    )
    import operator
    from typing import Annotated, Any, Dict, List, Optional, Sequence, TypedDict
    import functools

    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langgraph.graph import StateGraph, END

    # The agent state is the input to each node in the graph

    class AgentState(TypedDict):
        # The annotation tells the graph that new messages will always
        # be added to the current states
        messages: Annotated[Sequence[BaseMessage], operator.add]
        # The 'next' field indicates where to route to next
        next: str

    research_agent = create_agent(
        llm2, [search], "You are a buisness analyst/debater , your job is to oppose the views of coder -hold your stand on your opinions- critic him on his stand on a topic using your tool search, your output should not be more than 200 tokens")
    research_node = functools.partial(
        agent_node, agent=research_agent, name="Researcher")

    # NOTE: THIS PERFORMS ARBITRARY CODE EXECUTION. PROCEED WITH CAUTION
    code_agent = create_agent(
        llm2,
        [scrap_web],
        "You are a buisness analyst/great debater , your job is to oppose the views of researcher and critic him on his stand on various buisness plan using your tool scrap web, you can search two websites per call to repond, your output should not be more than 200 tokens , dont scrapp forbes or commonly use news websites ",

    )
    code_node = functools.partial(agent_node, agent=code_agent, name="Coder")

    workflow = StateGraph(AgentState)
    workflow.add_node("Researcher", research_node)
    workflow.add_node("Coder", code_node)
    workflow.add_node("supervisor", supervisor_chain)

    for member in members:
        # We want our workers to ALWAYS "report back" to the supervisor when done
        workflow.add_edge(member, "supervisor")
    # The supervisor populates the "next" field in the graph state
    # which routes to a node or finishes
    conditional_map = {k: k for k in members}
    conditional_map["FINISH"] = END
    workflow.add_conditional_edges(
        "supervisor", lambda x: x["next"], conditional_map)
    # Finally, add entrypoint
    workflow.set_entry_point("Coder")

    graph = workflow.compile()

    dag = x

    d = []
    for s in graph.stream(
        {
            "messages": [
                HumanMessage(
                    content="dag"+"This business plan will have great potential says Researcher")
            ], "recursion_limit": 3
        }
    ):
        if "end" not in s:
            d.append(s)
            print(s)
            print("----")
    # api= os.environ["OPENAI_API_KEY"]

    def gpt4(dag, d):
        import requests
        import json

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-**********************************"
        }
        i = f'''Summmarise the following buisness plan under these categories:
                give pros and cons under each category ,dont ask questions , no extra lines , just the pros and cons of each of these category
                                                        1) Demand
                                                        2) Growth
                                                        3) Sustainable for long term?
                                                        4) Risk aspects 
                                                        based on the buisness plan, use the conversaation as reference , limit to 4000 tokens output.
                                                        Buisness plan = {dag}
                                                        Conversatioin = {d} '''
        user_prompt = (i)
        data = {
            "model": "gpt-4-0125-preview"            # "model": "gpt-3.5-turbo"
            ,
            "messages": [{"role": "user", "content": user_prompt}],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        # print(response.text)
        json_string = response.text
        data = json.loads(json_string)

        #   print(data["choices"][0]["message"]["content"])
        return data["choices"][0]["message"]["content"]

        # print(response.text)

    g = gpt4(dag, d)
    return g


@app.route('/sort_words', methods=['POST'])
def main():
    load_dotenv()
    text = request.json.get('text')
    user_question = handle_userinput(text)
    return jsonify({'original_text': text, 'sorted_text': user_question})


if _name_ == '_main_':
    app.run(debug=True)

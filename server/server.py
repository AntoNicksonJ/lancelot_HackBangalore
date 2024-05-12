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

# pdf_file = None


@app.route('/api/save-text', methods=['POST'])
def save_text():
    data = request.get_json()
    text = data.get('text')
    # Here you can do whatever you want with the text, like save it to a database
    return text


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


@app.route('/gpt4', methods=['POST'])
def run_gpt4():
    if request.method == 'POST':
        input_text = save_text()
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

    return jsonify({'response': response}), 200


@app.route('/api/save-data', methods=['POST'])
def save_data():
    data = request.json
    input_value = data.get('inputValue')
    return input_value


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


stored_text = ""


@app.route('/store_text', methods=['POST'])
def store_text():
    global stored_text
    data = request.get_json()
    stored_text = data['text']
    return jsonify({"message": "Text stored successfully"})


@app.route('/fetch_text', methods=['GET'])
def fetch_text():
    global stored_text
    return jsonify({"text": stored_text})


@app.route('/sort_words', methods=['POST'])
def main():
    load_dotenv()
    text = request.json.get('text')
    user_question = handle_userinput(text)
    return jsonify({'original_text': text, 'sorted_text': user_question})


if _name_ == '_main_':
    app.run(debug=True)

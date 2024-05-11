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


app = Flask(__name__)


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

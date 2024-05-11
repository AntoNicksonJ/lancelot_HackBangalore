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

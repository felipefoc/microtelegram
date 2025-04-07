from ollama import Client as Ollama
from .config import DATABASE_URL
from langchain_together import ChatTogether
from langchain_experimental.sql import SQLDatabaseChain
from langchain import SQLDatabase
import os
import dotenv
dotenv.load_dotenv()

class TogetherAI(ChatTogether):
    default_model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

    def get_response_from_ai(self, message, model=default_model, context=[]):
        if context:
            context = '\n'.join(context)
            message = f"{context}\n{message}"

        response = self.invoke(message, model=model)
        return response.content

    def get_response_from_ai_with_template_prompt(self, message, template, model=default_model):
        response = self.invoke(template.format(input=message), model=model)
        return response.content


class LocalAI(Ollama):
    default_model = "llama2"

    def get_response_from_ai(self, message, model=default_model, context=[]):
        response = self.generate(model=model, prompt=message)
        return response.response


class UtilsForSQL:
    def __init__(self):
        self.db = SQLDatabase.from_uri(DATABASE_URL)
        self.llm = TogetherAI(
            temperature=0,
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            together_api_key=os.getenv("TOGETHER_API_KEY", None)
        )

    def ask_to_db(self, question):
        PROMPT = """ 
        Given an input question, first create a syntactically correct sql query to run,  
        then look at the results of the query and return the answer.  
        The question: {question}
        """
        FORMAT_RESPONSE = """
        Você é um formatador de respostas técnicas para humanizadas.
        Foi feito a pergunta: {question}
        A resposta: {response}

        Formate a resposta para ser breve, humanizada e em formato de texto simples
        """
        db_chain = SQLDatabaseChain(llm=self.llm, database=self.db, verbose=True, top_k=3, return_direct=True)
        response = db_chain.run(PROMPT.format(question=question))
        humanized_response = self.llm.invoke(input=FORMAT_RESPONSE.format(question=question, response=response))
        return humanized_response.content
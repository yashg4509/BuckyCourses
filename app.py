from langchain.chains import LLMMathChain
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentExecutor
import os
import chainlit as cl
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.utilities import GoogleSearchAPIWrapper
import pandas as pd
import os
import PyPDF2
import re
import csv
import pdftocsv

os.environ["OPENAI_API_KEY"] = "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"

chat_history = []


@cl.on_chat_start
async def start():
    dars = pd.read_csv("data/dars.csv")
    comp_sci = pd.read_csv("data/comp_sci_filtered_avg.csv")
    major_reqs = pd.read_csv("data/cs_major_reqs.csv")
    grades = pd.read_csv("data/grades.csv")

    apikey = os.environ["OPENAI_API_KEY"]

    # Create a function to consider "CS" as "COMP SCI"
    def preprocess_message(message):
        return message.replace("CS", "COMP SCI")

    # Create a function to analyze dars.csv when user asks about course history
    def analyze_course_history(message):
        if "course history" in message.lower():
            return dars

    # Create a function to make the response more user-friendly
    def make_response_user_friendly(response):
        # You can modify the response here to make it more user-friendly
        return response

    agent = create_pandas_dataframe_agent(
        OpenAI(openai_api_key=apikey, temperature=0),
        [comp_sci, major_reqs, grades, dars],
        verbose=True,
        preprocess_message=preprocess_message,
        analyze_course_history=analyze_course_history,
        make_response_user_friendly=make_response_user_friendly
    )

    cl.user_session.set("agent", agent)

    files = None
    
    while files is None:
        files = await cl.AskFileMessage(
        content="Please upload a Dars file to begin!",
        accept=["application/pdf"],
        max_size_mb=20,
        timeout=180,
        ).send()

    file_content = files[0].content

# Create a PDF reader object
    pdf_file = PyPDF2.PdfReader(io.BytesIO(file_content))

# Initialize a variable to store the extracted text
    text = ""
    
# Iterate through each page and extract text
    for page in pdf_file.pages:
        text += page.extract_text()

    my_data=pdftocsv.convert_to_text(text)
    #my_data=pdftocsv.extract_course_data(text)
    print("done")
    
    msg = cl.Message(content=f"Finished Processing file...")
    await msg.send()


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    response = await cl.make_async(agent.run)(message.content, callbacks=[cb])

    await cl.Message(author="Bucky", content=response).send()


# from langchain.chains import LLMMathChain
# from langchain.llms.openai import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.utilities import SerpAPIWrapper
# from langchain.agents import initialize_agent, Tool, AgentExecutor
# import os
# import chainlit as cl
# from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# from langchain.memory import ConversationBufferMemory
# from langchain.chat_models import ChatOpenAI
# from langchain.agents.agent_types import AgentType
# from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
# from langchain.memory import ConversationBufferMemory
# from langchain.llms import OpenAI
# from langchain.chains import LLMChain
# from langchain.utilities import GoogleSearchAPIWrapper
# import pandas as pd
# import os
#
# os.environ["OPENAI_API_KEY"] = "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"
#
# chat_history = []
# context = ""
#
# @cl.on_chat_start
# def start():
#     dars = pd.read_csv("data/dars.csv")
#     comp_sci = pd.read_csv("data/comp_sci_filtered_avg.csv")
#     major_reqs = pd.read_csv("data/cs_major_reqs.csv")
#     grades = pd.read_csv("data/grades.csv")
#
#     apikey = os.environ["OPENAI_API_KEY"]
#
#     # Create a function to consider "CS" as "COMP SCI"
#     def preprocess_message(message):
#         return message.replace("CS", "COMP SCI")
#
#     # Create a function to analyze dars.csv when user asks about course history
#     def analyze_course_history(message):
#         if "course history" in message.lower():
#             return dars
#
#     # Create a function to make the response more user-friendly
#     def make_response_user_friendly(response):
#         # You can modify the response here to make it more user-friendly
#         return response
#
#     agent = create_pandas_dataframe_agent(
#         OpenAI(openai_api_key=apikey, temperature=0),
#         [comp_sci, major_reqs, grades, dars],
#         verbose=True,
#         preprocess_message=preprocess_message,
#         analyze_course_history=analyze_course_history,
#         make_response_user_friendly=make_response_user_friendly
#     )
#
#     cl.user_session.set("agent", agent)
#
#
# @cl.on_message
# async def main(message: cl.Message):
#     global previous_response  # Declare previous_response as a global variable
#     agent = cl.user_session.get("agent")  # type: AgentExecutor
#     cb = cl.LangchainCallbackHandler(stream_final_answer=True)
#
#     # Add the user's message to the chat history
#     chat_history.append(message)
#
#     # Create a chat input by joining the chat history messages and the previous response
#     chat_input = "\n".join([f"{msg.author}: {msg.content}" for msg in chat_history])
#
#     # Check if the previous response was generated by the model and clear it if it was
#     if message.author != "Bucky":
#         previous_response = ""
#
#     response = await cl.make_async(agent.run)(chat_input, callbacks=[cb])
#
#     # Store the current response as the previous response
#     previous_response = response
#
#     await cl.Message(author="Bucky", content=response).send()
#
# #
# @cl.on_message
# async def main(message: cl.Message):
#     agent = cl.user_session.get("agent")  # type: AgentExecutor
#     cb = cl.LangchainCallbackHandler(stream_final_answer=True)
#
#     global context
#
#     # Add the user's message to the chat history
#     chat_history.append(message)
#
#     # Create a chat input by joining the chat history messages and the previous context
#     chat_input = "\n".join([f"{msg.author}: {msg.content}" for msg in chat_history])
#
#     if context:
#         chat_input = f"{context}\n{chat_input}"
#
#     response = await cl.make_async(agent.run)(chat_input, callbacks=[cb])
#
#     # Update the context with the current response
#     context = response
#
#     await cl.Message(author="Bucky", content=response).send()
#

# from langchain.chains import LLMMathChain
# from langchain.llms.openai import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.utilities import SerpAPIWrapper
# from langchain.agents import initialize_agent, Tool, AgentExecutor
# import os
# import chainlit as cl
# from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# from langchain.memory import ConversationBufferMemory
# from langchain.chat_models import ChatOpenAI
# from langchain.agents.agent_types import AgentType
# from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
# from langchain.memory import ConversationBufferMemory
# from langchain.llms import OpenAI
# from langchain.chains import LLMChain
# from langchain.utilities import GoogleSearchAPIWrapper
# import pandas as pd
# import os
#
# os.environ["OPENAI_API_KEY"] = "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"
#
# chat_history = []
#
# # Store the previous response
# previous_response = ""
#
#
# @cl.on_chat_start
# def start():
#     dars = pd.read_csv("data/dars.csv")
#     comp_sci = pd.read_csv("data/comp_sci_filtered_avg.csv")
#     major_reqs = pd.read_csv("data/cs_major_reqs.csv")
#     grades = pd.read_csv("data/grades.csv")
#
#     apikey = os.environ["OPENAI_API_KEY"]
#
#     # Create a function to consider "CS" as "COMP SCI"
#     def preprocess_message(message):
#         return message.replace("CS", "COMP SCI")
#
#     # Create a function to analyze dars.csv when user asks about course history
#     def analyze_course_history(message):
#         if "course history" in message.lower():
#             return dars
#
#     # Create a function to make the response more user-friendly
#     def make_response_user_friendly(response):
#         # You can modify the response here to make it more user-friendly
#         return response
#
#     agent = create_pandas_dataframe_agent(
#         OpenAI(openai_api_key=apikey, temperature=0),
#         [comp_sci, major_reqs, grades, dars],
#         verbose=True,
#         preprocess_message=preprocess_message,
#         analyze_course_history=analyze_course_history,
#         make_response_user_friendly=make_response_user_friendly
#     )
#
#     cl.user_session.set("agent", agent)
#
#
# @cl.on_message
# async def main(message: cl.Message):
#     global previous_response  # Declare previous_response as a global variable
#     agent = cl.user_session.get("agent")  # type: AgentExecutor
#     cb = cl.LangchainCallbackHandler(stream_final_answer=True)
#
#     # Add the user's message to the chat history
#     chat_history.append(message)
#
#     # Create a chat input by joining the chat history messages and the previous response
#     chat_input = "\n".join([f"{msg.author}: {msg.content}" for msg in chat_history])
#
#     if previous_response:
#         chat_input += f"\nPrevious Response: {previous_response}"
#
#     response = await cl.make_async(agent.run)(chat_input, callbacks=[cb])
#
#     # Store the current response as the previous response
#     previous_response = response
#
#     await cl.Message(author="Bucky", content=response).send()
#

#
# # from langchain.chains import LLMMathChain
# # from langchain.llms.openai import OpenAI
# # from langchain.chat_models import ChatOpenAI
# # from langchain.prompts import PromptTemplate
# # from langchain.utilities import SerpAPIWrapper
# # from langchain.agents import initialize_agent, Tool, AgentExecutor
# # import os
# #
# # import chainlit as cl
# # from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# # from langchain.memory import ConversationBufferMemory
# # from langchain.chat_models import ChatOpenAI
# # from langchain.agents.agent_types import AgentType
# #
# # from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
# # from langchain.memory import ConversationBufferMemory
# # from langchain.llms import OpenAI
# # from langchain.chains import LLMChain
# # from langchain.utilities import GoogleSearchAPIWrapper
# #
# # from langchain.llms import OpenAI
# # import pandas as pd
# # import os
# #
# # os.environ["OPENAI_API_KEY"] = "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"
# #
# # chat_history = []
# #
# #
# # @cl.on_chat_start
# # def start():
# #     dars = pd.read_csv("data/dars.csv")
# #     comp_sci = pd.read_csv("data/comp_sci_filtered_avg.csv")
# #     major_reqs = pd.read_csv("data/cs_major_reqs.csv")
# #     grades = pd.read_csv("data/grades.csv")
# #
# #     apikey = os.environ["OPENAI_API_KEY"]
# #
# #     # memory = ConversationBufferMemory()
# #     #
# #     # # # Add the existing chat history to the memory
# #     # # for chat_message in chat_history:
# #     # #     memory.add_message(chat_message.author, chat_message.content)
# #
# #     agent = create_pandas_dataframe_agent(
# #         OpenAI(openai_api_key=apikey, temperature=0),
# #         [comp_sci, major_reqs, grades, dars],
# #         verbose=True,
# #
# #     )
# #
# #     cl.user_session.set("agent", agent)
# #
# #
# # @cl.on_message
# # async def main(message: cl.Message):
# #     agent = cl.user_session.get("agent")  # type: AgentExecutor
# #     cb = cl.LangchainCallbackHandler(stream_final_answer=True)
# #
# #     # Add the user's message to the chat history
# #     chat_history.append(message)
# #
# #     # Create a chat input by joining the chat history messages
# #     chat_input = "\n".join([f"{msg.author}: {msg.content}" for msg in chat_history])
# #
# #     response = await cl.make_async(agent.run)(chat_input, callbacks=[cb])
# #
# #     await cl.Message(author="Bucky", content=response).send()
#
#     # # Add the user's message to the chat history
#     # chat_history.append(message)
#     #
#     # # Add the user's message to the memory
#     # memory = agent.agent.memory
#     # memory.add_message(message.author, message.content)
#     #
#     # response = await cl.make_async(agent.run)(message.content, callbacks=[cb])
#     #
#     # await cl.Message(author="Bucky", content=response).send()
#
# # from langchain.chains import LLMMathChain
# # from langchain.llms.openai import OpenAI
# # from langchain.chat_models import ChatOpenAI
# # from langchain.utilities import SerpAPIWrapper
# # from langchain.agents import initialize_agent, Tool, AgentExecutor
# # import os
# # import chainlit as cl
# # from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# # from langchain.memory import ConversationBufferMemory
# # from langchain.chat_models import ChatOpenAI
# # from langchain.agents.agent_types import AgentType
# #
# # from langchain.llms import OpenAI
# # import pandas as pd
# # import os
# #
# # os.environ["OPENAI_API_KEY"] = "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"
# #
# #
# # @cl.on_chat_start
# # def start():
# #     dars = pd.read_csv("data/dars.csv")
# #     comp_sci = pd.read_csv("data/comp_sci_filtered_avg.csv")
# #     major_reqs = pd.read_csv("data/cs_major_reqs.csv")
# #     grades = pd.read_csv("data/grades.csv")
# #
# #     apikey = os.environ["OPENAI_API_KEY"]
# #
#
# #
# #     agent = create_pandas_dataframe_agent(OpenAI(openai_api_key=apikey, temperature=0),
# #                                           [comp_sci, major_reqs, grades, dars],
# #                                           verbose=True)
# #     cl.user_session.set("agent", agent)
# #
# #
# # @cl.on_message
# # async def main(message: cl.Message):
# #     agent = cl.user_session.get("agent")  # type: AgentExecutor
# #     cb = cl.LangchainCallbackHandler(stream_final_answer=True)
# #
# #     response = await cl.make_async(agent.run)(message.content, callbacks=[cb])
# #
# #     await cl.Message(author="Agent", content=response).send()
# #
# #

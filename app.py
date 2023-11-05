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

from langchain.llms import OpenAI
import pandas as pd
import os

os.environ["OPENAI_API_KEY"] = "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"

chat_history = []


@cl.on_chat_start
def start():
    dars = pd.read_csv("data/dars.csv")
    comp_sci = pd.read_csv("data/comp_sci_filtered_avg.csv")
    major_reqs = pd.read_csv("data/cs_major_reqs.csv")
    grades = pd.read_csv("data/grades.csv")

    apikey = os.environ["OPENAI_API_KEY"]

    # memory = ConversationBufferMemory()
    #
    # # # Add the existing chat history to the memory
    # # for chat_message in chat_history:
    # #     memory.add_message(chat_message.author, chat_message.content)

    agent = create_pandas_dataframe_agent(
        OpenAI(openai_api_key=apikey, temperature=0),
        [comp_sci, major_reqs, grades, dars],
        verbose=True
    )

    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    # Add the user's message to the chat history
    chat_history.append(message)

    # Create a chat input by joining the chat history messages
    chat_input = "\n".join([f"{msg.author}: {msg.content}" for msg in chat_history])

    response = await cl.make_async(agent.run)(chat_input, callbacks=[cb])

    await cl.Message(author="Bucky", content=response).send()

    # # Add the user's message to the chat history
    # chat_history.append(message)
    #
    # # Add the user's message to the memory
    # memory = agent.agent.memory
    # memory.add_message(message.author, message.content)
    #
    # response = await cl.make_async(agent.run)(message.content, callbacks=[cb])
    #
    # await cl.Message(author="Bucky", content=response).send()

# from langchain.chains import LLMMathChain
# from langchain.llms.openai import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.utilities import SerpAPIWrapper
# from langchain.agents import initialize_agent, Tool, AgentExecutor
# import os
# import chainlit as cl
# from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# from langchain.memory import ConversationBufferMemory
# from langchain.chat_models import ChatOpenAI
# from langchain.agents.agent_types import AgentType
#
# from langchain.llms import OpenAI
# import pandas as pd
# import os
#
# os.environ["OPENAI_API_KEY"] = "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"
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

#
#     agent = create_pandas_dataframe_agent(OpenAI(openai_api_key=apikey, temperature=0),
#                                           [comp_sci, major_reqs, grades, dars],
#                                           verbose=True)
#     cl.user_session.set("agent", agent)
#
#
# @cl.on_message
# async def main(message: cl.Message):
#     agent = cl.user_session.get("agent")  # type: AgentExecutor
#     cb = cl.LangchainCallbackHandler(stream_final_answer=True)
#
#     response = await cl.make_async(agent.run)(message.content, callbacks=[cb])
#
#     await cl.Message(author="Agent", content=response).send()
#
#

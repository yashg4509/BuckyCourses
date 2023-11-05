from langchain.chains import LLMMathChain
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentExecutor
import os
import chainlit as cl
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

from langchain.llms import OpenAI
import pandas as pd
import os

os.environ["OPENAI_API_KEY"] = "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"


@cl.on_chat_start
def start():
    dars = pd.read_csv("data/dars.csv")
    comp_sci = pd.read_csv("data/comp_sci_filtered_avg.csv")
    major_reqs = pd.read_csv("data/cs_major_reqs.csv")
    grades = pd.read_csv("data/grades.csv")

    apikey = os.environ["OPENAI_API_KEY"]
    #
    # memory = ConversationBufferMemory(memory_key="chat_history")
    #
    # llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)

    agent = create_pandas_dataframe_agent(OpenAI(openai_api_key=apikey, temperature=0),
                                          [comp_sci, major_reqs, grades, dars],
                                          verbose=True)
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    response = await cl.make_async(agent.run)(message.content, callbacks=[cb])


    await cl.Message(author="Agent", content=response).send()

    # await cl.make_async(agent.run)(message.content, callbacks=[cb])

# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.schema import StrOutputParser
# from langchain.schema.runnable import Runnable
# from langchain.schema.runnable.config import RunnableConfig
# import os
# import model
#
# import chainlit as cl
#
# os.environ["OPENAI_API_KEY"] = "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"
#
# @cl.on_chat_start
# async def on_chat_start():
#     custom_model = model.agent
#     # prompt = ChatPromptTemplate.from_messages(
#     #     [
#     #         (
#     #             "system",
#     #             "You're a Bucky badger and you know everything about UW Madison and its courses.",
#     #         ),
#     #         ("human", "{question}"),
#     #     ]
#     # )
#     runnable = custom_model
#     # runnable = custom_model | StrOutputParser()
#     cl.user_session.set("runnable", runnable)
#
#
# @cl.on_message
# async def on_message(message: cl.Message):
#     runnable = cl.user_session.get("runnable")  # type: Runnable
#
#     msg = cl.Message(content="")
#
#     async for chunk in runnable.astream(
#         {"question": message.content},
#         config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
#     ):
#         await msg.stream_token(chunk)
#
#     await msg.send()
#
# # from langchain.chat_models import ChatOpenAI
# # from langchain.prompts import ChatPromptTemplate
# # from langchain.schema import StrOutputParser
# # from langchain.schema.runnable import Runnable
# # from langchain.schema.runnable.config import RunnableConfig
# # import os
# # import model  # Import your custom model module
# #
# # import chainlit as cl
# #
# # os.environ["OPENAI_API_KEY"] = "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"
# #
# # @cl.on_chat_start
# # async def on_chat_start():
# #     # Replace ChatOpenAI with your custom model initialization
# #     custom_model = model.agent  # Use your custom model instance
# #
# #     # prompt = ChatPromptTemplate.from_messages(
# #     #     [
# #     #         (
# #     #             "system",
# #     #             "You're a Bucky badger and you know everything about UW Madison and its courses.",
# #     #         ),
# #     #         ("human", "{question}"),
# #     #     ]
# #     # )
# #
# #     runnable = custom_model | StrOutputParser()
# #     # runnable = prompt | custom_model | StrOutputParser()
# #
# #     cl.user_session.set("runnable", runnable)
# #
# # @cl.on_message
# # async def on_message(message: cl.Message):
# #     runnable = cl.user_session.get("runnable")  # type: Runnable
# #
# #     msg = cl.Message(content="")
# #
# #     async for chunk in runnable.astream(
# #         {"question": message.content},
# #         config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
# #     ):
# #         await msg.stream_token(chunk)
# #
# #     await msg.send()

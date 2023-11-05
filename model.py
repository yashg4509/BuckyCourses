from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

from langchain.llms import OpenAI
import pandas as pd
import os

dars = pd.read_csv("data/dars.csv")
comp_sci = pd.read_csv("data/comp_sci_with_avg_gpa.csv")
major_reqs = pd.read_csv("data/cs_major_reqs.csv")
grades = pd.read_csv("data/grades.csv")

os.environ["OPENAI_API_KEY"] = "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"
apikey = os.environ["OPENAI_API_KEY"]

agent = create_pandas_dataframe_agent(OpenAI(openai_api_key=apikey, temperature=0),
                                      [comp_sci, major_reqs, grades, dars],
                                      verbose=True)

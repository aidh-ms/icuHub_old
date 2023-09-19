"""Setup for PandasAI"""

import os
from pandasai.llm import OpenAI
from dotenv import load_dotenv


load_dotenv()

llm_openai = OpenAI(os.getenv("OPENAI_API_KEY"))

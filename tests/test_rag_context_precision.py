from openai import AsyncOpenAI
import pytest
from dotenv import load_dotenv  # ensure .env values are read
from ragas import SingleTurnSample
from ragas.llms import llm_factory
from ragas.metrics.collections import ContextPrecision
from langchain_openai import ChatOpenAI

# load environment variables at module import time
load_dotenv()

@pytest.mark.asyncio
async def test_context_precision():
    client = AsyncOpenAI()
    llm = llm_factory("gpt-4o-mini", client=client)
    # directly pass the LLM instance; warping helper is not available in this version
    scorer = ContextPrecision(llm=llm)

    sample = await scorer.ascore(
        user_input="Pending test cases",
        reference="87",
        retrieved_contexts=[
            "Module: Payment\nTotal_Test_Cases: 168\nAutomated_Test_Cases: 58\nManual_Test_Cases: 110\nPass_Rate_%: 0.0\nDefect_Density_%: 16.07\nOpen_Defects: 22\nClosed_Defects: 5\nPending_Automation: 87\nPending_Automation_Target_Date: 2025-12-16",
        ]
    )

    print(f"Context Precision Score: {sample.value}")



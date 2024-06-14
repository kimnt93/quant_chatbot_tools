import datetime
import logging

from langchain.schema.runnable.config import RunnableConfig
import chainlit as cl
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langsmith import traceable
from chatbot.llm import FUNCTION_CALLING_LLM, SYNTHETIC_LLM
from chatbot.prompt import DEFAULT_PROMPT, SYNTHETIC_PROMPT
from chatbot.tool import (
    get_company_info, get_stock_trading_info, get_financial_info,
    return_default_query, get_performance_stats, show_stock_performance, show_price_volume_history
)

AVAILABLE_TOOLS = {
    "get_company_info": get_company_info,
    "get_stock_trading_info": get_stock_trading_info,
    "get_financial_info": get_financial_info,
    "return_default_query": return_default_query,
    "show_price_volume_history": show_price_volume_history,
    "show_stock_performance": show_stock_performance,
    "get_performance_stats": get_performance_stats

}

LLM_WITH_TOOLS = FUNCTION_CALLING_LLM.bind_tools([tool for tool in AVAILABLE_TOOLS.values()])


@cl.step
async def stream_default_qa(question):
    msg = cl.Message(content="")
    output_msg = ""
    chain = (
        {"question": RunnablePassthrough()}
        | PromptTemplate(
            template=DEFAULT_PROMPT,
            input_variables=["question"],
            partial_variables={"today": datetime.datetime.now()}
        )
        | SYNTHETIC_LLM
        | StrOutputParser()
    )
    async for chunk in chain.astream(
        question,
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)
        output_msg += chunk

    await msg.send()
    return output_msg


@cl.step
async def stream_synthetic(question, data, figures):
    msg = cl.Message(content="")
    output_msg = ""
    chain = (
        {"question": RunnablePassthrough()}
        | PromptTemplate(
            template=SYNTHETIC_PROMPT,
            input_variables=["question"],
            partial_variables={
                "data": data,
                "today": datetime.datetime.now()
            }
        )
        | SYNTHETIC_LLM
        | StrOutputParser()
    )
    async for chunk in chain.astream(
        question,
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)
        output_msg += chunk

    if figures:
        for figure in figures:
            msg.elements.append(cl.Plotly(figure=figure, display="inline"))

    await msg.send()
    return output_msg


@cl.step
async def function_calling(question):
    response_tools = LLM_WITH_TOOLS.invoke(question)
    response_data = list()
    charts = list()
    for tool_call in response_tools.tool_calls:
        logging.info(f"Call tool : {tool_call}")
        tool_call_results = AVAILABLE_TOOLS[tool_call['name']].invoke(tool_call['args'])
        if tool_call_results:
            for tool_call_result in tool_call_results:
                fig = tool_call_result.pop('fig') if 'fig' in tool_call_result else None
                if fig is not None:
                    charts.append(fig)
                response_data.append(tool_call_result)

    return response_data, charts


@cl.on_message
@traceable
async def quant_chat(message: cl.Message):
    question = message.content
    response_data, figures = await function_calling(question)

    if response_data:
        output_msg = await stream_synthetic(question, response_data, figures)
    else:
        output_msg = await stream_default_qa(question)

    return output_msg

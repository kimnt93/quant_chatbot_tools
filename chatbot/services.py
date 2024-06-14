import logging
from functools import lru_cache
from typing import List, Optional

import plotly
import requests
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from chatbot.llm import EXTRACT_COMPANY_LLM
from chatbot.prompt import EXTRACT_COMPANY_NAME_PROMPT

# Constants
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
YAHOO_FIN_SEARCH_BASE = "https://query2.finance.yahoo.com/v1/finance/search"


class CompanyTicker:
    def __init__(self, symbol, short_name, long_name, exchange):
        self.symbol = symbol
        self.short_name = short_name
        self.long_name = long_name
        self.exchange = exchange

    def __repr__(self):
        return f"CompanyTicker(symbol={self.symbol}, short_name={self.short_name}, long_name={self.long_name}, exchange={self.exchange})"


def _extract_companies_from_text(text):
    """
    Extracts company names from a given text query.

    Args:
        text (str): The text containing the list of company names.

    Returns:
        list: A list of unique company names extracted from the query.
    """
    pattern = r'\[.*?\]'  # Regular expression pattern to match a Python list
    companies = []

    for match in re.findall(pattern, text):
        try:
            extracted_list = eval(match)  # Evaluate the match as Python code
            if isinstance(extracted_list, list):
                companies.extend(extracted_list)
        except SyntaxError:
            logging.warning(f"Failed to evaluate list: {match}")

    return list(set(companies))  # Return unique company names


@lru_cache(maxsize=2048)
def _extract_company_from_query(query):
    """
    Invokes an external chain to extract company information from the query.

    Args:
        query (str): The text query.

    Returns:
        list: A list of unique company names extracted from the query.
    """
    chain = (
        {"question": RunnablePassthrough()}
        | PromptTemplate(
            template=EXTRACT_COMPANY_NAME_PROMPT,
            input_variables=["question"],
        )
        | EXTRACT_COMPANY_LLM
        | StrOutputParser()
    )

    result = chain.invoke(query)
    companies = _extract_companies_from_text(result)
    return companies


@lru_cache(maxsize=2048)
def _get_ticker_from_name(name) -> Optional[CompanyTicker]:
    """
    Fetches the ticker information for a given company name.

    Args:
        name (str): The name of the company.

    Returns:
        dict: A dictionary containing the ticker information.
    """
    params = {"q": name}
    try:
        response = requests.get(
            YAHOO_FIN_SEARCH_BASE,
            params=params,
            headers={'User-Agent': DEFAULT_USER_AGENT, "content-type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        record = data['quotes'][0]
        return CompanyTicker(
            symbol=record.get('symbol'),
            short_name=record.get('shortname'),
            long_name=record.get('longname'),
            exchange=record.get('exchange'),
        )
    except (requests.exceptions.RequestException, KeyError, IndexError) as ex:
        logging.error(f"Error fetching data for {name}: {ex}")
        return None


def get_ticker_from_query(query) -> List[CompanyTicker]:
    """
    Processes a query to extract company names and fetch their ticker information.

    Args:
        query (str): The text query containing company names.

    Returns:
        list: A list of dictionaries containing ticker information for each company.

    Example query: Show me microsoft and google beta values
    Example return: [
        {'symbol': 'GOOG', 'short_name': 'Alphabet Inc.', 'long_name': 'Alphabet Inc.', 'exchange': 'NMS'},
        {'symbol': 'MSFT', 'short_name': 'Microsoft Corporation', 'long_name': 'Microsoft Corporation', 'exchange': 'NMS'}
    ]
    """
    companies = _extract_company_from_query(query)
    results = []

    for company_name in companies:
        result = _get_ticker_from_name(company_name)
        if result:
            results.append(result)

    return results


def to_plotly(fig):
    try:
        return plotly.tools.mpl_to_plotly(fig)
    except Exception as ex:
        logging.error(f"Failed to convert to plotly: {ex}")
        return None


# Example usage
if __name__ == "__main__":
    tickers = get_ticker_from_query("Show me microsoft and google beta values")
    print(tickers)
    print("==================")

    tickers = get_ticker_from_query("Show me microsoft current price")
    print(tickers)
    print("==================")

    tickers = get_ticker_from_query("Show me microsoft and google beta values")
    print(tickers)
    print("==================")

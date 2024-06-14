from langchain_core.tools import tool
import plotly.graph_objects as go
from yfinance import Ticker
import quantstats as qs
from chatbot.data import YahooFinData
from chatbot.services import get_ticker_from_query, to_plotly

FAST_INFO = [
    'currency', 'dayHigh', 'dayLow', 'exchange', 'currentPrice', 'fiftyDayAverage', 'lastPrice', 'lastVolume', 'marketCap',
    'open', 'previousClose', 'quoteType', 'regularMarketPreviousClose', 'shares', 'tenDayAverageVolume',
    'threeMonthAverageVolume', 'timezone', 'twoHundredDayAverage', 'yearChange', 'yearHigh', 'yearLow'
]


def get_fast_info(yf_ticker: Ticker):
    info = yf_ticker.info
    fast_info = {
        key: info.get(key, "") for key in FAST_INFO
    }
    return fast_info


@tool
def get_company_info(question):
    """Return the company information when ask for it. The information include company name, sector, industry, address, phone, website, officers, and description, etc...
    Args:
        - question (str): The user question
    """
    tickers = get_ticker_from_query(question)
    infos = list()
    if len(tickers) > 0:
        for ticker in tickers:
            data = YahooFinData.get_instance(ticker.symbol)
            info = data.info
            infos.append({
                "symbol": info.get("symbol", ""),
                "exchange": info.get("exchange", ""),
                "address": info.get("address1", ""),
                "city": info.get("city", ""),
                "state": info.get("state", ""),
                "zip": info.get("zip", ""),
                "country": info.get("country", ""),
                "phone": info.get("phone", ""),
                "website": info.get("website", ""),
                "industry": info.get("industry", ""),
                "sector": info.get("sector", ""),
                "longBusinessSummary": info.get("longBusinessSummary", ""),
                "longName": info.get("longName", ""),
                "shortName": info.get("shortName", ""),
                "fullTimeEmployees": info.get("fullTimeEmployees", ""),
                "companyOfficers": info.get("companyOfficers", [])
            })

    return infos


@tool
def get_stock_trading_info(question):
    """Return the stock trading information include current price, open, high, low, close, volume, bid, ask, market cap, beta, P/E, and EPS, etc...
    Args:
        - question (str): The user question
    """
    tickers = get_ticker_from_query(question)
    infos = list()
    if len(tickers) > 0:
        for ticker in tickers:
            data = YahooFinData.get_instance(ticker.symbol)
            info = data.info
            infos.append({
                "symbol": info.get("symbol", ""),
                "exchange": info.get("exchange", ""),
                "regularMarketPrice": info.get("regularMarketPrice", ""),
                "regularMarketOpen": info.get("regularMarketOpen", ""),
                "regularMarketPreviousClose": info.get("regularMarketPreviousClose", ""),
                "regularMarketVolume": info.get("regularMarketVolume", ""),
                "regularMarketDayHigh": info.get("regularMarketDayHigh", ""),
                "regularMarketDayLow": info.get("regularMarketDayLow", ""),
                "regularMarketDayRange": info.get("regularMarketDayRange", ""),
                "regularMarketBid": info.get("regularMarketBid", ""),
                "regularMarketAsk": info.get("regularMarketAsk", ""),
                "marketCap": info.get("marketCap", ""),
                "beta": info.get("beta", ""),
                "trailingPE": info.get("trailingPE", ""),
                "forwardPE": info.get("forwardPE", ""),
                "eps": info.get("eps", ""),
                "enterpriseValue": info.get("enterpriseValue", 0),
                "currency": info.get("currency", ""),
                "pegRatio": info.get("pegRatio", 0),
                "priceToSalesTrailing12Months": info.get("priceToSalesTrailing12Months", 0),
                "priceToBook": info.get("priceToBook", 0),
                "enterpriseToRevenue": info.get("enterpriseToRevenue", 0),
                "enterpriseToEbitda": info.get("enterpriseToEbitda", 0),
                "priceHint": info.get("priceHint", 0),
                "previousClose": info.get("previousClose", 0),
                "open": info.get("open", 0),
                "dayLow": info.get("dayLow", 0),
                "dayHigh": info.get("dayHigh", 0),
                "financialCurrency": info.get("financialCurrency", ""),
                "currentPrice": info.get("currentPrice", 0),
                "volume": info.get("volume", 0),
                "trailingPegRatio": info.get("trailingPegRatio", 0),
                "bid": info.get("bid", 0),
                "ask": info.get("ask", 0),
                "bidSize": info.get("bidSize", 0),
                "askSize": info.get("askSize", 0),
                "targetHighPrice": info.get("targetHighPrice", 0),
                "targetLowPrice": info.get("targetLowPrice", 0),
                "targetMeanPrice": info.get("targetMeanPrice", 0),
                "targetMedianPrice": info.get("targetMedianPrice", 0),
                "recommendationMean": info.get("recommendationMean", 0),
                "recommendationKey": info.get("recommendationKey", ""),

            })

    return infos


@tool
def get_financial_info(question):
    """Return the financial information include balance sheet, income statement, debt, revenue, cash flow, and financial ratios, etc...
    Args:
        - question (str): The user question
    """
    tickers = get_ticker_from_query(question)
    infos = list()
    if len(tickers) > 0:
        for ticker in tickers:
            data = YahooFinData.get_instance(ticker.symbol)
            info = data.info
            infos.append({
                "symbol": info.get("symbol"),
                "totalCash": info.get("totalCash", 0),
                "totalCashPerShare": info.get("totalCashPerShare", 0),
                "ebitda": info.get("ebitda", 0),
                "totalDebt": info.get("totalDebt", 0),
                "quickRatio": info.get("quickRatio", 0),
                "currentRatio": info.get("currentRatio", 0),
                "totalRevenue": info.get("totalRevenue", 0),
                "debtToEquity": info.get("debtToEquity", 0),
                "revenuePerShare": info.get("revenuePerShare", 0),
                "returnOnAssets": info.get("returnOnAssets", 0),
                "returnOnEquity": info.get("returnOnEquity", 0),
                "freeCashflow": info.get("freeCashflow", 0),
                "operatingCashflow": info.get("operatingCashflow", 0),
                "earningsQuarterlyGrowth": info.get("earningsQuarterlyGrowth", 0),
                "netIncomeToCommon": info.get("netIncomeToCommon", 0),
                "trailingEps": info.get("trailingEps", 0),
                "forwardEps": info.get("forwardEps", 0),
                "earningsGrowth": info.get("earningsGrowth", 0),
                "revenueGrowth": info.get("revenueGrowth", 0),
                "grossMargins": info.get("grossMargins", 0),
                "ebitdaMargins": info.get("ebitdaMargins", 0),
                "operatingMargins": info.get("operatingMargins", 0),
                "financialCurrency": info.get("financialCurrency", "")
            })

    return infos


@tool
def show_price_volume_history(question, period='2y'):
    """Show the price history (OHLC) of the stock.
    Args:
        - question (str): The user question
        - period (str): The period of the price history (default is 2y). The valid values are: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    """
    tickers = get_ticker_from_query(question)
    infos = list()
    for ticker in tickers:
        symbol = ticker.symbol
        data = YahooFinData.get_instance(symbol)
        summary_info = get_fast_info(data)
        hist = data.history(period=period).reset_index()
        fig = go.Figure(
            data=go.Ohlc(x=hist['Date'],
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'])
        )
        title = f'{symbol} OHLC from {hist.Date.min().strftime("%Y-%m-%d")} to {hist.Date.max().strftime("%Y-%m-%d")}'
        fig.update_layout(title=title)
        infos.append({
            "symbol": symbol,
            "summary": f"{hist.iloc[0].__str__()}\n-----\n{hist.iloc[-1].__str__()}\n-----\nInfo: {summary_info}",
            "fig": fig
        })
    return infos


@tool
def show_stock_performance(question):
    """Show the stock performance chart including the Daily return, Drawdown and Cumulative Returns
    Args:
        - question (str): The user question
    """
    tickers = get_ticker_from_query(question)
    infos = list()
    for ticker in tickers:
        symbol = ticker.symbol
        data = YahooFinData.get_instance(symbol)
        returns = YahooFinData.download_stock_returns(symbol)
        summary_info = get_fast_info(data)
        fig = qs.plots.snapshot(returns, show=False)
        title = f'{symbol} Performance'
        fig.title = title
        fig = to_plotly(fig)
        infos.append({
            "symbol": symbol,
            "summary": f"{summary_info}",
            "fig": fig
        })
    return infos


@tool
def get_performance_stats(question):
    """Return the performance of the stock, including cagr, sharpe, max_drawdown, sortino, avg_win, avg_loss, volatility, calmar, value_at_risk, cvar
    Args:
        - question (str): The user question
    """
    tickers = get_ticker_from_query(question)
    infos = list()
    if len(tickers) > 0:
        for ticker in tickers:
            returns = YahooFinData.download_stock_returns(ticker.symbol)
            infos.append({
                "symbol": ticker.symbol,
                "cagr": qs.stats.cagr(returns),
                "sharpe": qs.stats.sharpe(returns),
                "max_drawdown": qs.stats.max_drawdown(returns),
                "sortino": qs.stats.sortino(returns),
                "avg_win": qs.stats.avg_win(returns),
                "avg_loss": qs.stats.avg_loss(returns),
                "volatility": qs.stats.volatility(returns),
                "calmar": qs.stats.calmar(returns),
                "value_at_risk": qs.stats.value_at_risk(returns),
                "cvar": qs.stats.cvar(returns)
            })

    return infos


@tool
def return_default_query(question):
    """
    Return empty response if the question is not related to any specific topic.
    """
    return None


if __name__ == "__main__":
    print(get_company_info("Tell me about microsoft inc and alphabet inc"))

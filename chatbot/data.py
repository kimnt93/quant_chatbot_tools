from cachetools import TTLCache
import yfinance as yf
import logging
import quantstats as qs

from cachetools.func import ttl_cache


class YahooFinData:
    _ticker_info_cache = TTLCache(maxsize=1024, ttl=600)

    @staticmethod
    def get_instance(symbol) -> yf.Ticker:
        if symbol not in YahooFinData._ticker_info_cache:
            logging.info(f"Create ticker {symbol}")
            YahooFinData._ticker_info_cache[symbol] = yf.Ticker(symbol)

        return YahooFinData._ticker_info_cache[symbol]

    @staticmethod
    @ttl_cache(ttl=3600, maxsize=2048)
    def download_stock_returns(symbol):
        returns = qs.utils.download_returns(symbol)
        return returns

import re
import random
import asyncio
import logging
import platform
import warnings
import polars as pl
import pandas as pd #Used for typing hints only
from io import BytesIO
from zipfile import ZipFile
from tqdm.asyncio import tqdm
from itertools import filterfalse
from aiolimiter import AsyncLimiter
from datetime import datetime, date
from dateutil.parser import parse, ParserError
from aiohttp import ClientSession, ClientTimeout
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from typing import Literal, Union, NewType, Type, List

logging.getLogger(__name__)

warnings.simplefilter(action= "ignore", category= DeprecationWarning)

if platform.system() == "Windows":
    import winloop
    asyncio.set_event_loop_policy(winloop.EventLoopPolicy())
else:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

DateFormat: Type = NewType(name="%d-%m-%Y", tp=str)

base_url = "https://data.binance.vision"
exchange_info = "https://api.binance.com/api/v3/exchangeInfo"
s3_binance_vision = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"

#MAX_SIZE = 3 * 1024 * 1024 
ITER_SIZE = 1 * 1024 * 1024
MAX_CONCURRENT_REQUESTS = 5

BAR_COLORS = ['green', 'blue', 'red', 'cyan', 'magenta', 'white', "yellow"]

column_names = {
    "klines": ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume', 'ignore'],
    "aggTrades": ["agg_trade_id", "price", "quantity", "first_trade_id", "last_trade_id", "transact_time", "is_buyer_maker"],
    "bookDepth": ["timestamp", "percentage", "depth", "notional"],
    "bookTicker": ["update_id", "best_bid_price", "best_bid_qty", "best_ask_price", "best_ask_qty", "transaction_time", "event_time"],
    "liquidationSnapshot": ["time", "side", "order_type", "time_in_force", "original_quantity", "price", "average_price", "order_status", "last_fill_quantity", "accumulated_fill_quantity"],
    "metrics": ["create_time", "symbol", "sum_open_interest", "sum_open_interest_value", "count_toptrader_long_short_ratio", "sum_toptrader_long_short_ratio", "count_long_short_ratio", "sum_taker_long_short_vol_ratio"],
    "trades": ["id", "price", "qty", "base_qty", "time", "is_buyer_maker"],
    "BVOLIndex": ["calc_time", "symbol", "base_asset", "quote_asset", "index_value"],
    "EOHSummary": ["date", "hour", "symbol", "underlying", "type", "strike", "open", "high", "low", "close", "volume_contracts", "volume_usdt", "best_bid_price", "best_ask_price", "best_bid_qty", "best_ask_qty", "best_buy_iv", "best_sell_iv", "mark_price", "mark_iv", "delta", "gamma", "vega", "theta", "openinterest_contracts", "openinterest_usdt"],
    "aggTrades_spot": ["agg_trade_id", "price", "quantity", "first_trade_id", "last_trade_id", "transact_time", "is_buyer_maker", "is_best_match"],
    "trades_spot": ["id", "price", "qty", "base_qty", "time", "is_buyer_maker", "is_best_match"],
    "fundingRate": ['calc_time', 'funding_interval_hours', 'last_funding_rate']    
}

sort_by = {
    "klines": 'open_time',
    "aggTrades": "agg_trade_id",
    "bookDepth": "timestamp",
    "bookTicker": "update_id",
    "liquidationSnapshot": "time",
    "metrics": "create_time",
    "trades": "id",
    "BVOLIndex": "calc_time",
    "EOHSummary": ["date", "hour"],
    "aggTrades_spot": "agg_trade_id",
    "trades_spot": "id",
    "fundingRate": "calc_time"
}

schemas = {
    "klines": {
            'open_time': pl.Int64, 
            'open': pl.Float64, 
            'high': pl.Float64, 
            'low': pl.Float64, 
            'close': pl.Float64, 
            'volume': pl.Float64, 
            'close_time': pl.Int64, 
            'quote_volume': pl.Float64, 
            'count': pl.Int64, 
            'taker_buy_volume': pl.Float64, 
            'taker_buy_quote_volume': pl.Float64, 
            'ignore': pl.Float64
            },
    "trades_spot": {
            'id': pl.Int64, 
            'price': pl.Float64, 
            'qty': pl.Float64, 
            'base_qty': pl.Float64, 
            'time': pl.Int64, 
            'is_buyer_maker': pl.Boolean, 
            'is_best_match': pl.Boolean
            },
    "aggTrades_spot": {
            'agg_trade_id': pl.Int64, 
            'price': pl.Float64, 
            'quantity': pl.Float64, 
            'first_trade_id': pl.Int64, 
            'last_trade_id': pl.Int64, 
            'transact_time': pl.Int64, 
            'is_buyer_maker': pl.Boolean, 
            'is_best_match': pl.Boolean
            },
    "aggTrades": {
            'agg_trade_id': pl.Int64, 
            'price': pl.Float64, 
            'quantity': pl.Float64, 
            'first_trade_id': pl.Int64, 
            'last_trade_id': pl.Int64, 
            'transact_time': pl.Int64, 
            'is_buyer_maker': pl.Boolean
            },
    "bookDepth": {
            'timestamp': pl.String, 
            'percentage': pl.Int64, 
            'depth': pl.Float64, 
            'notional': pl.Float64
            },
    "bookTicker": {
            'update_id': pl.Int64, 
            'best_bid_price': pl.Float64, 
            'best_bid_qty': pl.Float64, 
            'best_ask_price': pl.Float64, 
            'best_ask_qty': pl.Float64, 
            'transaction_time': pl.Int64, 
            'event_time': pl.Int64
            },
    "fundingRate": {
            'calc_time': pl.Int64, 
            'funding_interval_hours': pl.Int64, 
            'last_funding_rate': pl.Float64
            },
    "metrics": {
            'create_time': pl.String, 
            'symbol': pl.String, 
            'sum_open_interest': pl.Float64, 
            'sum_open_interest_value': pl.Float64, 
            'count_toptrader_long_short_ratio': pl.String, 
            'sum_toptrader_long_short_ratio': pl.String, 
            'count_long_short_ratio': pl.String, 
            'sum_taker_long_short_vol_ratio': pl.Float64
            },
    "trades": {
            'id': pl.Int64, 
            'price': pl.Float64, 
            'qty': pl.Float64, 
            'base_qty': pl.Float64, 
            'time': pl.Int64, 
            'is_buyer_maker': pl.Boolean
            },  
    "BVOLIndex": {
            'calc_time': pl.Int64, 
            'symbol': pl.String, 
            'base_asset': pl.String, 
            'quote_asset': pl.String, 
            'index_value': pl.Float64
            },
    "EOHSummary": {
            'date': pl.String, 
            'hour': pl.Int64, 
            'symbol': pl.String, 
            'underlying': pl.String, 
            'type': pl.String, 
            'strike': pl.String, 
            'open': pl.Float64, 
            'high': pl.Float64, 
            'low': pl.Float64, 
            'close': pl.Float64, 
            'volume_contracts': pl.Float64, 
            'volume_usdt': pl.Float64, 
            'best_bid_price': pl.Float64, 
            'best_ask_price': pl.Float64, 
            'best_bid_qty': pl.Float64, 
            'best_ask_qty': pl.Float64, 
            'best_buy_iv': pl.String, 
            'best_sell_iv': pl.Float64, 
            'mark_price': pl.Float64, 
            'mark_iv': pl.Float64, 
            'delta': pl.Float64, 
            'gamma': pl.Float64, 
            'vega': pl.Float64, 
            'theta': pl.Float64, 
            'openinterest_contracts': pl.Float64, 
            'openinterest_usdt': pl.Float64
            },
    "liquidationSnapshot": {
            'time': pl.Int64, 
            'side': pl.String, 
            'order_type': pl.String, 
            'time_in_force': pl.String, 
            'original_quantity': pl.Float64, 
            'price': pl.Float64, 
            'average_price': pl.Float64, 
            'order_status': pl.String, 
            'last_fill_quantity': pl.Float64, 
            'accumulated_fill_quantity': pl.Float64
            }
}

class BarAllocator:
    def __init__(self, max_concurrent_tasks: int):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.available_positions = list(range(max_concurrent_tasks)) 

    async def get_next_available_bar(self):
        while not self.available_positions:
            await asyncio.sleep(0.1)
        return self.available_positions.pop(0)

    def release_bar(self, position: int):
        self.available_positions.append(position)  

class BinanceHistorical:
    def __init__(
            self,
            total_timeout: int= 300,
            connect_timeout: int=30,
            sock_read_timeout: int= 100,
            sock_connect_timeout: int= 30,
            limiter_max_rate: int= 5,
            limiter_time_period: int=1,
            ):
        self.__loop = asyncio.get_event_loop()
        self.__limiter = AsyncLimiter(
                                max_rate= limiter_max_rate, 
                                time_period= limiter_time_period
                                )
        self.__timeout = ClientTimeout(
                                total= total_timeout,
                                connect= connect_timeout,
                                sock_read= sock_read_timeout,
                                sock_connect= sock_connect_timeout 
                                )
        self.__semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        self.__bar_allocator = BarAllocator(MAX_CONCURRENT_REQUESTS)
    
    async def __get(
            self,
            url: str,
            params: dict= None
            ) -> Union[str, bytes]:   
        try:     
            async with ClientSession(timeout= self.__timeout, raise_for_status= True) as session:
                async with session.get(url= url, params= params, raise_for_status= True) as response:
                    if response.status == 200:
                        content_type = response.content_type

                        if content_type == "application/json":
                            return await response.json()
                        elif content_type == "text/html" or content_type == "application/xml":
                            return await response.text()
                        else:
                            return await response.read()
        except Exception as e:
            print(f"Error occured at fetching data :: {e}")

    def __get_data(
            self, 
            data: BytesIO,
            selector: str
            )-> pl.LazyFrame:
        
        with ZipFile(data) as zfile:
            with zfile.open(zfile.infolist()[0].filename) as csvfile:
                return pl.scan_csv(
                            csvfile.read(), 
                            new_columns= column_names[selector],
                            schema_overrides= schemas[selector],
                            )  

    async def __fetch(
            self,
            uri_part: str,
            selector: str,
            client: ClientSession,
            progress_bar: bool
            )-> pl.LazyFrame:
        try:
            async with self.__limiter:            
                async with self.__semaphore:    
                    async with client.get(url= f"{uri_part}.zip") as response:
                        response.raise_for_status()
                        if response.status == 200:
                            content_length = response.headers.get('Content-Length')

                            total_size = int(content_length) if content_length else None
                            bytes_io = BytesIO()
                            current_size = 0

                            if progress_bar:
                                pbar_position = await self.__bar_allocator.get_next_available_bar()

                                if total_size: # and total_size > MAX_SIZE:
                                    pbar = tqdm(
                                            total= total_size,
                                            unit= 'B',
                                            unit_scale= True,
                                            position= pbar_position + 2,
                                            leave= False,
                                            desc= f"Downloading {uri_part.split('/')[-1]}",
                                            colour= random.choice(BAR_COLORS)
                                        )

                                    async for chunk in response.content.iter_chunked(ITER_SIZE):
                                        current_size += len(chunk)
                                        bytes_io.write(chunk)
                                        pbar.update(len(chunk))
                                    pbar.close()
                                    pbar.clear()
                                    self.__bar_allocator.release_bar(pbar_position)
                                else:
                                    content = await response.read()
                                    bytes_io.write(content)
                            else:
                                if total_size: # and total_size > MAX_SIZE:
                                    async for chunk in response.content.iter_chunked(ITER_SIZE):
                                        current_size += len(chunk)
                                        bytes_io.write(chunk)
                                else:
                                    content = await response.read()
                                    bytes_io.write(content)
                            return await asyncio.to_thread(lambda: self.__get_data(bytes_io, selector))  
        except Exception as e:
            tqdm.write(f"Error occured at fetching data {e} :: {uri_part.split("/")[-1]}")    
            return None    

    async def __historical(
            self,
            uri_parts: list,
            selector: str,
            progress_bar: bool,
            progress_bar_color: str,
            tqdm_desc: str
            )-> List[pl.LazyFrame]:
        async with ClientSession(base_url= base_url, timeout= self.__timeout, loop= self.__loop) as session:
            tasks = [
                self.__fetch(uri_part= uri, selector= selector, client= session, progress_bar= progress_bar) for uri in uri_parts
            ]
            if progress_bar:
                results = []
                for task in tqdm(
                            asyncio.as_completed(tasks), 
                            total= len(tasks), 
                            desc= tqdm_desc,
                            position= 0, #MAX_CONCURRENT_REQUESTS + 1,
                            leave= True,
                            colour= progress_bar_color,
                            ):
                    result = await task
                    if result is not None:
                        results.append(result)
            else:
                results = await asyncio.gather(*tasks)
                results = [
                    result for result in results if result is not None
                    ]
            return results

    @staticmethod
    def parse_date(date_str: str)-> datetime:
        try:
            return parse(timestr= date_str, dayfirst= True).date()
        except (ParserError, Exception):
            print("Invalid date str format..") 
            return    

    @staticmethod
    def generate_date_list(
            start_date: date, 
            end_date: date, 
            data_type: str
            )-> List[str]:
        dates = list(
                    rrule(
                        freq= MONTHLY if data_type=="monthly" else DAILY, 
                        dtstart= start_date, 
                        until= end_date
                        )
                    )   
        return [
            dt.strftime("%Y-%m") if data_type=="monthly"\
                  else dt.strftime("%Y-%m-%d") for dt in dates        
            ]

    def __populate_date_list(
                    self, 
                    start_date: date, 
                    end_date: date,
                    daily_only: bool= False,
                    monthly_only: bool= False
                    )-> Union[dict, list]:
        
        dates: dict = {}

        if isinstance(start_date, str):
            start_date = BinanceHistorical.parse_date(start_date)
        elif isinstance(start_date, datetime):
            start_date = start_date.date()

        if isinstance(end_date, str):
            end_date = BinanceHistorical.parse_date(end_date)
        if isinstance(end_date, datetime):
            end_date = end_date.date()  

        todays_date = datetime.now().date()
        if end_date >= todays_date:
            end_date = todays_date + relativedelta(days= -1)
        
        if end_date.month == todays_date.month and end_date.year == todays_date.year:
            month_end_date = end_date + relativedelta(day=1, days=-1)
        else:
            month_end_date = end_date

        
        if daily_only:
            dates.update({"daily": BinanceHistorical.generate_date_list(start_date, end_date, "daily")})
            return dates
        if monthly_only:
            dates.update({"monthly": BinanceHistorical.generate_date_list(start_date, month_end_date, "monthly")})
            return dates

        months_first = end_date + relativedelta(day=1)

        daily_dates = None

        if start_date < months_first:
            date_list = BinanceHistorical.generate_date_list(start_date, month_end_date, "monthly")
            if start_date.day != 1:
                start_date_month_last = start_date + relativedelta(day=1, months=+1, days=-1)

                dates.update({"monthly": date_list[1:]})
                daily_dates = BinanceHistorical.generate_date_list(start_date, start_date_month_last, "daily")
            else:
                dates.update({"monthly": date_list})
            if daily_dates:
                daily_dates.extend(BinanceHistorical.generate_date_list(months_first, end_date, "daily"))
                dates.update({"daily": daily_dates})
            else:
                dates.update({"daily": BinanceHistorical.generate_date_list(months_first, end_date, "daily")})
        else:
            dates.update({"daily": BinanceHistorical.generate_date_list(start_date, end_date, "daily")})
        return dates
    
    def spot_historical(
                self,
                symbol: str,
                start_date: Union[DateFormat, datetime, date]= "27-11-2024",#"14-7-2017",
                end_date: Union[DateFormat, datetime, date]= datetime.today(),
                data_type: Literal["aggTrades", "klines", "trades"]= "klines",
                freq: Literal[
                            "1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", 
                            "6h", "8h", "12h", "1d"]= "1m",
                output_type: Literal["pandas", "polars"]= "polars",
                progress_bar: bool= True,
                progress_bar_color: Literal["red", "green", "blue", "yellow"]= "green"
                )-> Union[pl.DataFrame, pd.DataFrame]:
        """
        freq is applicable for only klines.

        Fetch historical data from Binance Spot.

        Parameters:
        - symbol : Trading pair (e.g., 'BTCUSDT').
        - start_date : Start date for data fetch. Defaults to "2020-01-01".
        - end_date : End date for data fetch. Defaults to current date.
        - data_type : Type of data to fetch (e.g., "klines" for candlestick data).
        - freq : Data frequency (e.g., "1s", "1m", etc.).
        - output_type : Output data as polars/ pandas dataframe  (default is "polars").
        - progress_bar : Whether to show a progress bar during data fetch.
        - progress_bar_color : Color of the progress bar.

        Returns:
        - DataFrame (pl.DataFrame or pd.DataFrame)
        """       

        dates = self.__populate_date_list(start_date, end_date)

        monthly = dates.get("monthly")
        daily = dates.get("daily")

        uri_parts = []      

        if data_type == "klines":
            __selector = "klines"
            if monthly:
                uri_parts += [
                    f"/data/spot/monthly/{data_type}/{symbol}/{freq}/{symbol}-{freq}-{m}"\
                        for m in monthly
                ]
            if daily:
                uri_parts += [
                    f"/data/spot/daily/{data_type}/{symbol}/{freq}/{symbol}-{freq}-{d}"\
                        for d in daily
                ]
        else:
            __selector = f"{data_type}_spot"
            if monthly:
                uri_parts += [
                    f"/data/spot/monthly/{data_type}/{symbol}/{symbol}-{data_type}-{m}"\
                        for m in monthly
                ]
            if daily:
                uri_parts += [
                    f"/data/spot/daily/{data_type}/{symbol}/{symbol}-{data_type}-{d}"\
                        for d in daily
                ]


        task = self.__loop.create_task(
                    self.__historical(
                        uri_parts= uri_parts,
                        selector= __selector,
                        progress_bar= progress_bar,
                        progress_bar_color= progress_bar_color,
                        tqdm_desc= "Fetching Data :: "
                    )
                )

        results = self.__loop.run_until_complete(task)    
        if results:
            df = pl.concat(results).sort(sort_by[__selector]).collect()\
                    if len(results) > 1 else results[0].sort(sort_by[__selector]).collect()
            return df if output_type=="polars" else df.to_pandas(use_pyarrow_extension_array=True)
    
    def option_historical(
                self,
                symbol: str,
                start_date: Union[DateFormat, datetime, date]= "20-6-2023",
                end_date: Union[DateFormat, datetime, date]= datetime.today(),
                data_type: Literal["BVOLIndex", "EOHSummary"]= "BVOLIndex",
                output_type: Literal["pandas", "polars"]= "polars",
                progress_bar: bool= True,
                progress_bar_color: Literal["red", "green", "blue", "yellow"]= "green"
                )-> Union[pl.DataFrame, pd.DataFrame]:
        """
        Fetch historical data for Binance Options.

        *** EOHSummary data is available only upto 23-10-2023 in binance vision

        Parameters:
        - symbol : Trading pair (e.g., 'BTCUSDT').
        - start_date : Start date for data fetch. Defaults to "2020-01-01".
        - end_date : End date for data fetch. Defaults to current date.
        - data_type : Type of data to fetch .
        - output_type : Output data as polars/ pandas dataframe  (default is "polars").
        - progress_bar : Whether to show a progress bar during data fetch.
        - progress_bar_color : Color of the progress bar.

        Returns:
        - DataFrame (pl.DataFrame or pd.DataFrame)
        """       

        dates = self.__populate_date_list(start_date, end_date, daily_only= True)

        daily = dates.get("daily")

        uri_parts = []      

        if daily:
            __selector = data_type
            uri_parts += [
                f"/data/option/daily/{data_type}/{symbol}/{symbol}-{data_type}-{d}"\
                    for d in daily
            ]
    
            task = self.__loop.create_task(
                        self.__historical(
                            uri_parts= uri_parts,
                            selector= __selector,
                            progress_bar= progress_bar,
                            progress_bar_color= progress_bar_color,
                            tqdm_desc= "Fetching Data :: "
                        )
                    )
    
            results = self.__loop.run_until_complete(task)    
            if results:
                df = pl.concat(results).sort(sort_by[__selector]).collect()\
                        if len(results) > 1 else results[0].sort(sort_by[__selector]).collect()
                return df if output_type=="polars" else df.to_pandas(use_pyarrow_extension_array=True)

    def future_historical(
                        self,
                        symbol: str,
                        start_date: Union[DateFormat, datetime, date]= "14-7-2017",
                        end_date: Union[DateFormat, datetime, date]= datetime.today(),
                        contract_type: Literal["um", "cm"]= "um",              
                        data_type: Literal[
                                    "aggTrades", "bookDepth", "bookTicker", "fundingRate", "indexPriceKlines", 
                                    "klines", "markPriceKlines", "premiumIndexKlines", "trades", "liquidationSnapshot"]= "klines",
                        freq: Literal[
                                    "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", 
                                    "6h", "8h", "12h", "1d", "3d", "1w", "1mo"]= "1m",
                        output_type: Literal["pandas", "polars"]= "polars",
                        progress_bar: bool= True,
                        progress_bar_color: Literal["red", "green", "blue", "yellow"]= "green"
                        )-> Union[pl.DataFrame, pd.DataFrame]:
        """
        freq is applicable only in klines, indexPriceKlines, markPriceKlines and premiumIndexKlines

        Fetch historical data from Binance Futures.

        Parameters:
        - symbol : Trading pair (e.g., 'BTCUSDT').
        - start_date : Start date for data fetch. Defaults to "2020-01-01".
        - end_date : End date for data fetch. Defaults to current date.
        - contract_type : Type of contract ("um" for USDS-Margined, "cm" for Coin-Margined).
        - data_type : Type of data to fetch (e.g., "klines" for candlestick data).
        - freq : Data frequency (e.g., "1m", "1h", etc.).
        - output_type : Output data as polars/ pandas dataframe  (default is "polars").
        - progress_bar : Whether to show a progress bar during data fetch.
        - progress_bar_color : Color of the progress bar.

        Returns:
        - DataFrame (pl.DataFrame or pd.DataFrame)
        """  
        monthly_only = False
        daily_only = False

        if contract_type == "um" and data_type == "fundingRate":
            print("Funding rate is available only for contract_type 'cm'.")
            return     
        if contract_type == "cm" and data_type == "fundingRate":
                monthly_only = True
        if data_type == "liquidationSnapshot":
            daily_only = True

        dates = self.__populate_date_list(start_date, end_date, daily_only= daily_only, monthly_only= monthly_only)

        monthly = dates.get("monthly")
        daily = dates.get("daily")

        uri_parts = []

        if data_type in ("klines", "indexPriceKlines", "markPriceKlines", "premiumIndexKlines"):
            __selector = "klines"
            if monthly:
                uri_parts += [
                    f"/data/futures/{contract_type}/monthly/{data_type}/{symbol}/{freq}/{symbol}-{freq}-{m}"\
                        for m in monthly
                ]
            if daily:
                uri_parts += [
                    f"/data/futures/{contract_type}/daily/{data_type}/{symbol}/{freq}/{symbol}-{freq}-{d}"\
                        for d in daily
                ]
        else:
            __selector = data_type
            if monthly:
                uri_parts += [
                    f"/data/futures/{contract_type}/monthly/{data_type}/{symbol}/{symbol}-{data_type}-{m}"\
                        for m in monthly
                ]
            if daily:
                uri_parts += [
                    f"/data/futures/{contract_type}/daily/{data_type}/{symbol}/{symbol}-{data_type}-{d}"\
                        for d in daily
                ]


        task = self.__loop.create_task(
                    self.__historical(
                        uri_parts= uri_parts,
                        selector= __selector,
                        progress_bar= progress_bar,
                        progress_bar_color= progress_bar_color,
                        tqdm_desc= "Fetching Data :: "
                    )
                )

        results = self.__loop.run_until_complete(task)    
        if results:
            df = pl.concat(results).sort(sort_by[__selector]).collect()\
                    if len(results) > 1 else results[0].sort(sort_by[__selector]).collect()
            return df if output_type=="polars" else df.to_pandas(use_pyarrow_extension_array=True)

    def get_data_list(
            self,
            symbol: str= None,
            market: Literal["futures", "option", "spot"]= "spot",
            contract_type: Literal["um", "cm"]= "um",    
            time_period: Literal["daily", "monthly"]= "daily",          
            data_type: Literal[
                        "aggTrades", "bookDepth", "bookTicker", "fundingRate", "indexPriceKlines", 
                        "klines", "markPriceKlines", "premiumIndexKlines", "trades", "BVOLIndex", "EOHSummary"]= "klines",
            freq: Literal[
                        "1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", 
                        "6h", "8h", "12h", "1d", "3d", "1w", "1mo"]= "1m",
            filter_checksums: bool= True
            )-> List[str]:
        """
        Get list of available data files/ folders name according to input.

        ***freq is applicable only for "indexPriceKlines", "klines", "markPriceKlines" and "premiumIndexKlines".        
        
        Parameters:
        - symbol : If None the function will return available folders according to other parameters.
                    If not function will return available file list for the given symbol according 
                    to other parameters. Defaults to None.
        - market : Type of market. Defaults to "spot".
        - contract_type : Applicable if market is "futures". "um" - USDS-Margined and "cm" for Coin-Margined.
        - time_period : data files are available as monthly (single file for one month) and daily files.
        - data_type : Type of data (e.g., "klines" for candlestick data).
        - freq : Data frequency (e.g., "1s", "1m", etc.).
        - filter_checksums : If True, will filter out the .checksum file names from output list.

        Returns:
        - list of items
        """   
        
        uri = "data/"

        if market == "futures" or market == "spot":
            if data_type in ("BVOLIndex", "EOHSummary"):
                print("Data type available for options only")
                return

        if market == "futures":
            if data_type == "fundingRate":
                if contract_type== "um":
                    print("Funding rate is available for coin m futures only..")
                    return
                if contract_type == "cm" and time_period == "daily":
                    print("Try time period 'monthly' ")
                    return

            uri += f"futures/{contract_type}/{time_period}/{data_type}/"
            if symbol:
                uri += f"{symbol}/"
                if data_type in ("klines", "indexPriceKlines", "marketPriceKlines", "premiumIndexKlines"):
                    uri += f"{freq}/"
        elif market == "option":
            if not data_type in ("BVOLIndex", "EOHSummary") or time_period == "daily":
                print("Incorrect parameters..")
                return                
            uri += f"{market}/{time_period}/{data_type}/"
            if symbol:
                uri += f"{symbol}/"
        elif market == "spot":
            if not data_type in ("aggTrades", "klines", "trades"):
                print("Invalid data type")
                return
            uri += f"{market}/{time_period}/{data_type}/"
            if symbol:
                uri += f"{symbol}/"
                if data_type == "klines":
                    uri += f"{freq}/"
        
        params = {
                "delimiter": "/",
                "prefix": f"{uri}"
            }

        #print(uri)
        task = self.__loop.create_task(
                            self.__get(url= s3_binance_vision, params= params)
                            )

        response = self.__loop.run_until_complete(task)
                
        #pattern = re.escape(uri) + r'([^<]+)' 
        pattern = re.escape(uri) + r'([^<]+?)(?=/|<|$)'
        
        matches = re.findall(pattern, response)
        if filter_checksums:
            matches = list(filterfalse(lambda item: item.endswith(".CHECKSUM"), matches))
        print(matches)
    
    def get_pairs(
            self,
            base_currency: str = None,
            type: Literal["spot", "margin", "all"]= "all",
            status: Literal["trading", "break", "all"]= "trading",      
            output_type: Literal["pandas", "polars", "symbols_as_list"]= "symbols_as_list"  
        )-> Union[pl.DataFrame, pd.DataFrame, List[str]]:
        """
        Get pair symbols as list or pandas/ polars dataframe with additional info.    
        
        Parameters:
        - symbol : If None function will return all pairs according to other parameters.
                    else return pairs with given base currency. (eg. "USDT")
        - type : type of pair. Default "all"
        - status : Status of pair ( tradeable or not). Default "all" will return all pairs.
        - output_type : Output type (polars/ pandas dataframe or list of symbols). Defaults to "symbols_as_list"

        Returns:
        - Polars/ pandas Dataframe OR List(symbols). 
        """   
        
        type_col = {
            "spot": "isSpotTradingAllowed",
            "margin": "isMarginTradingAllowed"
        }

        expr = None
        if base_currency:
            expr = pl.col("symbol").str.ends_with(base_currency)
        if type in ("spot", "margin"):
            if expr is not None:
                expr &= pl.col(type_col[type])
            else:
                expr = pl.col(type_col[type])
        if status in ("trading", "break"):
            if expr is not None:
                expr &= pl.col("status").eq(status.upper())
            else:
                expr = pl.col("status").eq(status.upper())        
        
        #print(expr)

        task = self.__loop.create_task(
                        self.__get(url= exchange_info)
                        )

        result = self.__loop.run_until_complete(task)

        if result:
            df = pl.from_dicts(result["symbols"])
            if expr is not None:
                df = df.filter(expr)
            if output_type == "symbols_as_list":
                return df.select("symbol").sort("symbol").to_series().to_list()
            elif output_type == "pandas":
                return df.to_pandas(use_pyarrow_extension_array= True)
            else:
                return df

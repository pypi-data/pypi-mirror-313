import pandas as pd
from typing import Union
from datetime import datetime
class SubscribeUpdate:
    def __init__(self, realtime:bool, tickers: list, fields:list, period:int, by:str,
                 
                callback: callable,
                wait_for_full_timeFrame: bool,
                from_date: Union[str, datetime, None] = None)-> None:
        
        self.tickers: list
        self._stop: bool
       
    def get_data(self) -> pd.DataFrame: ...
    def stop(self) -> None: ...


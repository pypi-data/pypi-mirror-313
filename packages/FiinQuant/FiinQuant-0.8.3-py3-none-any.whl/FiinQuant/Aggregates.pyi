import pandas as pd
from typing import Union
from datetime import datetime

# class Bar:
#     def __init__(self, 
#                  access_token: str, 
#                  ticker: str,  
#                  by: str,  
#                  from_date: Union[str , datetime],  
#                  to_date: Union[str , datetime],  
#                 ) -> None:...

#     def get(self, data_type: str) -> BarData: ...

# class IndexBars(Bar) : 
#     def get(self) -> BarData: ...

# class TickerBars(Bar):
#     def get(self) -> BarData: ...

# class CoveredWarrantBars(Bar):
#     def get(self) -> BarData: ...
    
# class DerivativeBars(Bar):
#     def get(self) -> BarData: ...


class BarData:
    def __init__(self, data) -> None:
        self.__private_attribute: pd.DataFrame = data
        self.Timestamp: Union[str, datetime]
        self.Open: float
        self.High: float
        self.Low: float
        self.Close: float
        self.Volume: int
        self.Ticker: str
        self.BU: int
        self.SD: int
        self.FB: float
        self.FS: float
        self.FN: float
        
    def to_dataFrame(self) -> pd.DataFrame: ...

class BarDataUpdate:
    def __init__(self, data) -> None:
        self.__private_attribute: pd.DataFrame
    def to_dataFrame(self) -> pd.DataFrame: ...


class GetBarData:
    def __init__(self, 
                 tickers: Union[str, list],
                 by: str, 
                 from_date: Union[str, datetime, None], 
                 to_date: Union[str, datetime, None],
                 adjusted: bool, 
                 fields: list, 
                 period: int) -> None: ...
    
    def get(self) -> BarData: ...


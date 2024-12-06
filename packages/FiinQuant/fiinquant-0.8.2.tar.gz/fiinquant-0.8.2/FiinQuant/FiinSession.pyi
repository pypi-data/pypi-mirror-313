# from FiinIndicator import FiinIndicator
from Aggregates import IndexBars, TickerBars, CoveredWarrantBars, DerivativeBars, GetBarData
from SubscribeCoveredWarrantEvents import SubscribeCoveredWarrantEvents
from SubscribeIndexEvents import SubscribeIndexEvents
from SubscribeTickerEvents import SubscribeTickerEvents
from SubscribeTickerUpdate import SubscribeTickerUpdate
from SubscribeDerivativeEvents import SubscribeDerivativeEvents
from SubscribeEvents import SubscribeEvents
from SubscribeUpdate import SubscribeUpdate
from datetime import datetime, timedelta
from FiinIndicator import _FiinIndicator
from typing import Union

class FiinSession:
    def __init__(self, username: str, password: str):...

    def login(self) -> FiinSession: ...
        
   
    def FiinIndicator(self) -> _FiinIndicator: ...
    
    def IndexBars(self, tickers: str, by: str, 
                  from_date: Union [str, datetime] = datetime.now() - timedelta(days=30), 
                  to_date: Union [str, datetime] = datetime.now(), 
                  adj: bool = True) -> IndexBars:...
    
    def TickerBars(self, tickers: str, by: str, 
                  from_date: Union [str, datetime] = datetime.now() - timedelta(days=30), 
                  to_date: Union [str, datetime] = datetime.now(), 
                  adj: bool = True) -> TickerBars:...
    
    def DerivativeBars(self, tickers: str, by: str, 
                  from_date: Union [str, datetime] = datetime.now() - timedelta(days=30), 
                  to_date: Union [str, datetime] = datetime.now(), 
                  adj: bool = True) -> DerivativeBars:...
    
    def CoveredWarrantBars(self, tickers: str, by: str, 
                  from_date: Union [str, datetime] = datetime.now() - timedelta(days=30), 
                  to_date: Union [str, datetime] = datetime.now(), 
                  adj: bool = True) -> CoveredWarrantBars:...
    
    def SubscribeDerivativeEvents(self,
                            tickers: list, 
                            callback: callable) -> SubscribeDerivativeEvents: ...
    def SubscribeCoveredWarrantEvents(self,
                            tickers: list, 
                            callback: callable) -> SubscribeCoveredWarrantEvents: ...
    def SubscribeTickerEvents(self,
                            tickers: list, 
                            callback: callable) -> SubscribeTickerEvents: ...
    def SubscribeIndexEvents(self,
                            tickers: list, 
                            callback: callable) -> SubscribeIndexEvents: ...
    def SubscribeTickerUpdate(self,
                            tickers: list, 
                            callback: callable,
                            by: str,
                            from_date: str,
                            wait_for_full_timeFrame: bool) -> SubscribeTickerUpdate: ...
    
    def SubscribeEvents(self, 
                        tickers: list, 
                        callback: callable) -> SubscribeEvents: ...
    
    def SubscribeUpdate(self,
            realtime: bool,
            tickers: list,
            fields: list,
            period: int,
            by: str,
            from_date: Union [str, datetime, None],
            callback: callable,
            wait_for_full_timeFrame: bool) -> SubscribeUpdate: ...

    def GetBarData(self, tickers: Union [str, list], by: str, 
                from_date: Union [str, datetime, None] = None, 
                to_date: Union [str, datetime, None] = None, 
                adjusted: bool = True,
                fields: list = [],
                period: int = 0) -> GetBarData: ...

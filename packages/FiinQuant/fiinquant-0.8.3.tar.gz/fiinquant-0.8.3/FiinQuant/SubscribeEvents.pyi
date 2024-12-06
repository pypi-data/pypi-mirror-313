class SubscribeEvents:
    def __init__(self,tickers: list, callback: callable) -> None:
        self.tickers: list
        self._stop: bool
        
    def start(self) -> None: ...
        
    def stop(self) -> None: ...


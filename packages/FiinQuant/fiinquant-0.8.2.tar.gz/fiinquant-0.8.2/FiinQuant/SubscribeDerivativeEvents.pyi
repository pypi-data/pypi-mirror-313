class SubscribeDerivativeEvents:
    def __init__(self, access_token: str, tickers: list, callback: callable) -> None:
        self.tickers: list
        self._stop: bool

    def start(self) -> None: ...
        
    def stop(self) -> None: ...


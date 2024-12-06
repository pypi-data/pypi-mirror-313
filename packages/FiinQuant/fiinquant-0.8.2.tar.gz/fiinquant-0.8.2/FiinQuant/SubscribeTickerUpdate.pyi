class SubscribeTickerUpdate:
    def __init__(self, access_token: str, tickers: list, callback: callable, by: str, from_date: str, wait_for_full_timeFrame: bool) -> None:
        self.tickers: list
        self._stop: bool
    def start(self) -> None: ...
    def stop(self) -> None: ...



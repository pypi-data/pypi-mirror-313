import pandas as pd
class IndexData:
    def __init__(self, data) -> None:
        self.__private_attribute: pd.DataFrame
        self.TotalMatchVolume: int
        self.MarketStatus: str
        self.TradingDate: str
        self.ComGroupCode: str
        self.ReferenceIndex: float
        self.OpenIndex: float
        self.CloseIndex: float
        self.HighestIndex: float
        self.LowestIndex: float
        self.IndexValue: float
        self.IndexChange: float
        self.PercentIndexChange: float
        self.MatchVolume: int
        self.MatchValue: float
        self.TotalMatchValue: float
        self.TotalDealVolume: int
        self.TotalDealValue: float
        self.TotalStockUpPrice: int
        self.TotalStockDownPrice: int
        self.TotalStockNoChangePrice: int
        self.TotalStockOverCeiling: int
        self.TotalStockUnderFloor: int
        self.ForeignBuyVolumeTotal: int
        self.ForeignBuyValueTotal: float
        self.ForeignSellVolumeTotal: int
        self.ForeignSellValueTotal: float
        self.VolumeBu: int
        self.VolumeSd: int

    def to_dataFrame(self) -> pd.DataFrame: 
        ...

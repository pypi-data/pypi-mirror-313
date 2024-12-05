"""Analytics Module."""

from datetime import datetime, timedelta, timezone


class Analytics:
    """Analytics class."""

    def __init__(self, parent):
        """Class constructor."""
        self.parent = parent

    def __date_range(self, since, to, since_lag=30, to_lag=0):
        now = datetime.now().astimezone(timezone.utc)
        return {
            "dateRange": {
                "from": since or (now - timedelta(days=since_lag)).strftime("%Y-%m-%d"),
                "to": to or (now + timedelta(days=to_lag)).strftime("%Y-%m-%d"),
            }
        }

    def best_prices(self):
        """Get best bid and best ask in order list.

        POST  api/v1/clientapi/bestBidAsk
        """
        return self.parent.post("/clientapi/bestBidAsk")

    def best_prices_precise(self):
        """Get best bid and best ask in order list.

        POST  api/v1/clientapi/bestBidAskPrecise
        """
        return self.parent.post("/clientapi/bestBidAskPrecise")

    def total_trading_volume(self):
        """Get total trading volume.

        GET  api/v1/analytics/{underlier}/{numeraire}/totalTradingVolume
        """
        return self.parent.get("/analytics/WETH/USDC/totalTradingVolume")

    def total_contracts_traded(self):
        """Get total contracts traded.

        GET  /api/v1/analytics/{underlier}/{numeraire}/totalContractsTraded
        """
        return self.parent.get("/analytics/WETH/USDC/totalContractsTraded")

    def total_open_interest(self):
        """Get total open interest.

        GET  /api/v1/analytics/{underlier}/{numeraire}/totalOpenInterest
        """
        return self.parent.get("/analytics/WETH/USDC/totalOpenInterest")

    def total_value_locked(self):
        """Get total value locked.

        GET  /api/v1/analytics/{underlier}/{numeraire}/totalValueLocked
        """
        return self.parent.get("/analytics/WETH/USDC/totalValueLocked")

    def trades(self, since=None, to=None):
        """Get trades.

        POST  /api/v1/analytics/{underlier}/{numeraire}/trades
        """
        payload = self.__date_range(since, to)
        return self.parent.post("/analytics/WETH/USDC/trades", payload)

    def open_interest_by_product(self, since=None, to=None, to_lag=60):
        """Get open interest by product.

        POST  /api/v1/analytics/{underlier}/{numeraire}/openInterestByProduct
        """
        payload = self.__date_range(since, to, to_lag=to_lag)
        return self.parent.post("/analytics/WETH/USDC/openInterestByProduct", payload)

    def open_interest_by_strike(self, since=None, to=None, to_lag=60):
        """Get open interest by strike.

        POST  /api/v1/analytics/{underlier}/{numeraire}/openInterestByStrike
        """
        date_range = self.__date_range(since, to, to_lag=to_lag)

        payload = {**date_range, "strikeRange": {"from": 1, "to": 2500000000000}}
        return self.parent.post("/analytics/WETH/USDC/openInterestByStrike", payload)

    def daily_volume(self, since=None, to=None, since_lag=30):
        """Get daily volume.

        POST  /api/v1/analytics/{underlier}/{numeraire}/dailyVolume
        """
        date_range = self.__date_range(since, to, since_lag=since_lag)
        payload = {**date_range}
        return self.parent.post("/analytics/WETH/USDC/dailyVolume", payload)

    def all(self):
        """Get analytics."""
        return {
            "totalTradingVolume": self.total_trading_volume(),
            "totalContractsTraded": self.total_contracts_traded(),
            "totalOpenInterest": self.total_open_interest(),
            "totalValueLocked": self.total_value_locked(),
            "trades": self.trades(),
            "openInterestByProduct": self.open_interest_by_product(),
            "openInterestByStrike": self.open_interest_by_strike(),
            "dailyVolume": self.daily_volume(),
        }

"""Protocol Module."""


class Protocol:
    """Protocol Class."""

    def __init__(self, parent):
        """Class constructor."""
        self.parent = parent

    def system_info(self):
        """Get System Info."""
        return self.parent.post("/clientapi/systemInfo")

    def next_auction(self):
        """Get next auctions."""
        return self.parent.post("/clientapi/nextAuction")

    def contract_list(self, flat=False):
        """Get contract list."""
        contracts = self.parent.post("/clientapi/contractList")

        def parse_economics(row):
            return (
                row["currencyPair"],
                row["expiry"],
                row["priceCurrency"],
                row["qtyCurrency"],
                row.get("strike"),
            )

        if flat:
            return [
                [x["contractId"], x["payoff"], *parse_economics(x["economics"])]
                for x in contracts.get("payload")
            ]
        return contracts

    def contract_list_by_ids(self, ids):
        """Get contract list by Id."""
        body = {"ids": ids}
        return self.parent.post("/clientapi/contractListByIds", json=body)

    def historical_contracts(self, expiry):
        """Get historical contracts."""
        body = {"expiry": expiry}
        return self.parent.post("/clientapi/historicalContracts", json=body)
    
    def orderbook(self):
        """Get orderbbok if flagged as MARKET_MAKER"""
        return self.parent.post('/clientapi/orderbook')
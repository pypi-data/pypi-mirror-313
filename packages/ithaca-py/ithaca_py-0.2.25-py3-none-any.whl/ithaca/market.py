"""Market Module."""


class Market:
    """Market Class."""

    def __init__(self, parent):
        """Class constructor."""
        self.parent = parent

    def reference_prices(self, currency_pair, expiry=None):
        """Get reference prices."""
        if expiry is None:
            body = {"currencyPair": currency_pair}
        else:
            body = {"expiry": expiry, "currencyPair": currency_pair}
        return self.parent.post("/clientapi/referencePrices", json=body)

    def spot_prices(self):
        """Get spot prices."""
        return self.parent.post("/clientapi/spotPrices")

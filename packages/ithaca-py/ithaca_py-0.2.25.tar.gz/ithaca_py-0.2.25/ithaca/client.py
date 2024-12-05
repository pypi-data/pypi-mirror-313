"""Client Module."""

import pandas as pd


class Client:
    """Client class."""

    def __init__(self, parent):
        """Class constructor."""
        self.parent = parent

    def fundlock_state(self):
        """Get client fundlock state.

        Returns:
            _type_: _description_
        """
        return self.parent.post("/clientapi/clientFundLockState")

    def positions_lock_state(self):
        """Get client locked positions collateral.

        Returns:
            _type_: _description_
        """
        return self.parent.post("/clientapi/getLockedCollateral")

    def current_positions(self, _filter=None, details=False):
        """Return a list of the clients positions.

        Args:
            filter (_type_, opt.): COMBINE_STRATEGIES | SHOW_ORDERS.
            details (bool, opt.): If True, returns a DF with contract details.

        Returns:
            _type_: _description_
        """
        body = {"filter": _filter}
        res = self.parent.post("/clientapi/clientCurrentPositions", body)
        if details:
            contracts = self.parent.protocol.contract_list().get("payload")
            contracts = pd.DataFrame(
                list(
                    map(
                        lambda x: {
                            "contractId": x["contractId"],
                            "payoff": x["payoff"],
                            **x["economics"],
                        },
                        contracts,
                    )
                )
            ).set_index("contractId")
            return (
                pd.DataFrame(res.get("payload")).set_index("contractId").join(contracts)
            )
        return res

    def trade_history(
        self,
        date_from: int = None,
        date_to: int = None,
        offset: int = None,
        limit: int = None,
        status: str = None,
    ):
        """Get trade history."""
        """date_from/to are timestamps in backend"""
        body = {key: value for key, value in {
            'from': date_from,
            'to': date_to,
            'offset': offset,
            'limit': limit,
            'status': status
        }.items() if value is not None}

        if body:
            return self.parent.post("/clientapi/tradeHistory", json=body)
        else:
            return self.parent.post("/clientapi/tradeHistory")

    def historical_positions(self, expiry, _filter="NO_DETAILS"):
        """Get client historical positions.

        Args:
            expiry (int): Ithaca expiry date.
            filter (_type_, opt.): NO_DETAILS | COMBINE_STRATEGIES | SHOW_ORDERS.
        
        """
        body = {"expiry": expiry, "filter": _filter}
        return self.parent.post("/clientapi/clientHistoricalPositions", json=body)

    def historical_positions_by_date(self, _from: int, to: int):
        """Get details of client's past positions filtered by period.

        - if from or to is null last 30 days pos. are returned
        - if from-to period is > 90 days, pos. to-90 days to are returned

        Args:
            _from (int): miliseconds from 1970
            to (int): to miliseconds from 1970

        Example:
            {
                'result': 'OK',
                'details': '',
                'payload': {'totalCollateral': {},
                'expiryPrices': {'WETH/USDC': 2257.43},
                'payoff': {},
                'positions': []}
            }

        Returns:
            dict: _description_
        """
        body = {"from": _from, "to": to}
        return self.parent.post(
            "/clientapi/clientHistoricalPositionsByDatePeriod", json=body
        )

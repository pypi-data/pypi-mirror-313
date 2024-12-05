"""Calculation Module."""

from math import exp, log, pi, sqrt

from scipy.stats import norm
from logger import logger


class Calculation:
    """Calculation Class."""

    def __init__(self, parent):
        """Class constructor."""
        self.parent = parent

    def calc_portfolio_collateral(self):
        """Calculate portfolio collateral."""
        return self.parent.post("/clientapi/calcPortfolioCollateral")

    def estimate_order_payoff(
        self, legs, price, order_type="LIMIT", time_in_force="GOOD_TILL_CANCEL"
    ):
        """Calculate order payoff."""
        legs = [
            {"contractId": contract_id, "quantity": qty, "side": side}
            for contract_id, side, qty in legs
        ]
        order = {
            "clientOrderId": 1,
            "totalNetPrice": price,
            "legs": legs,
            "orderType": order_type,
            "timeInForce": time_in_force,
            "clientEthAddress": self.parent.address.lower(),
        }
        return self.parent.post("/clientapi/estimateOrderPayoff", json=order)

    def estimate_order_lock(
        self, legs, price, order_type="LIMIT", time_in_force="GOOD_TILL_CANCEL"
    ):
        """Estimate order lock."""
        legs = [
            {"contractId": contract_id, "quantity": qty, "side": side}
            for contract_id, side, qty in legs
        ]
        order = {
            "clientOrderId": 1,
            "totalNetPrice": price,
            "legs": legs,
            "orderType": order_type,
            "timeInForce": time_in_force,
            "clientEthAddress": self.parent.address.lower(),
        }
        return self.parent.post("/clientapi/estimateOrderLock", json=order)


    def estimate_multi_order_lock(
            self, orders_array, order_type="LIMIT", time_in_force="GOOD_TILL_CANCEL", consider_existing_positions=False, debug=False
    ):
        """Estimate lock for array of orders."""
        payload = []
        for idx, (legs, price) in enumerate(orders_array, 1):
            legs = [
                {"contractId": contract_id, "quantity": qty, "side": side}
                for contract_id, side, qty in legs
            ]
            order = {
                "clientOrderId": idx,
                "totalNetPrice": price,
                "legs": legs,
                "orderType": order_type,
                "timeInForce": time_in_force,
                "clientEthAddress": self.parent.address.lower() if consider_existing_positions else f"{'0x':0<42}",
            }
            payload.append(order)

        if debug:
            logger.debug(f"[DEBUG] payload: {payload}")

        return self.parent.post("/clientapi/estimatePositionedOrdersLock", json=payload)


    def estimate_order_fees(
        self, legs, price, order_type="LIMIT", time_in_force="GOOD_TILL_CANCEL"
    ):
        """Estimate order fees.

        Args:
            legs ([type]): [description]
            price ([type]): [description]
            order_type (str, optional): Defaults to "LIMIT".
            time_in_force (str, optional): Defaults to "GOOD_TILL_CANCEL".

        Returns:
            [type]: [description]
        """
        legs = [
            {"contractId": contract_id, "quantity": qty, "side": side}
            for contract_id, side, qty in legs
        ]
        order = {
            "clientOrderId": 1,
            "totalNetPrice": price,
            "legs": legs,
            "orderType": order_type,
            "timeInForce": time_in_force,
            "clientEthAddress": self.parent.address.lower(),
        }
        return self.parent.post("/clientapi/estimateOrderFees", json=order)

    def black_formula_extended(self, call_put_flag, f, k, t, sigma, df=1.0):
        """
        Black formula for pricing European call and put options.

        (with extended Greeks, excluding Rho)

        Parameters:
        call_put_flag: 'c' for call, 'p' for put.
        F: Forward price of the underlying asset.
        K: Strike price.
        t: Time to expiration.
        sigma: Volatility.
        df: Discount factor.

        Returns:
        price, delta, gamma, vega, theta, volga
        """
        d1 = (log(f / k) + 0.5 * sigma**2 * t) / (sigma * sqrt(t))
        d2 = d1 - sigma * sqrt(t)

        pdf_d1 = exp(-0.5 * d1**2) / sqrt(2 * pi)

        if call_put_flag == "c":
            price = df * (f * norm.cdf(d1) - k * norm.cdf(d2))
            delta = df * norm.cdf(d1)
        elif call_put_flag == "p":
            price = df * (k * norm.cdf(-d2) - f * norm.cdf(-d1))
            delta = -df * norm.cdf(-d1)

        gamma = df * pdf_d1 / (f * sigma * sqrt(t))
        vega = f * df * pdf_d1 * sqrt(t)
        theta = (
            -(f * pdf_d1 * sigma * df) / (2 * sqrt(t)) - df * k * norm.cdf(d2) / t
            if call_put_flag == "p"
            else -(f * pdf_d1 * sigma * df) / (2 * sqrt(t)) + df * k * norm.cdf(d1) / t
        )
        volga = vega * d1 * d2 / sigma

        return price, delta, gamma, vega, theta, volga

    def black_vanilla_price(self, call_put_flag, f, k, t, sigma, df=1.0):
        """
        Black formula for pricing European call and put options.

        Parameters:
        call_put_flag: 'c' for call, 'p' for put.
        f: Forward price of the underlying asset.
        k: Strike price.
        t: Time to expiration.
        sigma: Volatility.
        df: Discount factor.

        Returns:
        price
        """
        result, _, _, _, _, _ = self.black_formula_extended(
            call_put_flag, f, k, t, sigma, df
        )
        return result

    def black_digital_price(
        self, call_put_flag, f, k, t, sigma, dsigmadstrike=0, df=1.0
    ):
        """
        Black formula for pricing European digital call and put options.

        Parameters:
        call_put_flag: 'c' for call, 'p' for put.
        F: Forward price of the underlying asset.
        K: Strike price.
        t: Time to expiration.
        sigma: Volatility.
        df: Discount factor.

        Returns:
        price
        """
        d1 = (log(f / k) + 0.5 * sigma**2 * t) / (sigma * sqrt(t))
        d2 = d1 - sigma * sqrt(t)

        if call_put_flag == "c":
            price = df * norm.cdf(d2)
        elif call_put_flag == "p":
            price = df * norm.cdf(-d2)

        if dsigmadstrike != 0.0:
            _, _, _, vega_vanilla, _, _ = self.black_formula_extended(
                call_put_flag, f, k, t, sigma
            )
            price = price + vega_vanilla * dsigmadstrike * (
                1.0 if dsigmadstrike == "P" else -1.0
            )
        return price

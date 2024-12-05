"""Ithaca SDK."""

import logging

import requests
from eth_account import Account
from tenacity import retry, stop_after_attempt, wait_exponential
from urllib3 import Retry

from .analytics import Analytics
from .auth import Auth
from .calculation import Calculation
from .client import Client
from .constants import ENVS
from .fundlock import Fundlock
from .market import Market
from .orders import Orders  # type: ignore  # noqa: F401
from .protocol import Protocol
from .socket import Socket


class IthacaSDK:
    """
    Ithaca SDK Class

    Properties:
        auth (Auth): Authentication
        protocol (Protocol): Protocol
        market (Market): Market
        client (Client): Client
        orders (Orders): Orders
        calculation (Calculation): Calculation
        socket (Socket): Socket
        fundlock (Fundlock): Fundlock
        analytics (Analytics): Analytics
    """

    def __init__(
        self,
        eth_address=None,
        private_key=None,
        api_endpoint=None,
        ws_endpoint=None,
        graphql_endpoint=None,
        rpc_endpoint=None,
        env_name="CANARY",
    ):
        """
        Ithaca SDK Constructor. By default, one should specify a private_key for on-chain and backend authentication followed by the environment one wishes to access.


        Args:
          private_key (str): Private Key
          api_endpoint (str): API Endpoint
          ws_endpoint (str): Websocket Endpoint
          graphql_endpoint (str): Graphql Endpoint
          rpc_endpoint (str): RPC Endpoint
          env_name (str): (Depreciated) Environment Name
        """
        if not all([api_endpoint, ws_endpoint, graphql_endpoint, rpc_endpoint]):
            logging.warning(
                f"Endpoint specifications not found, defaulting to 'env_name': {env_name}"
            )
            logging.warning(f"api_endpoint: {api_endpoint}")
            logging.warning(f"ws_endpoint: {ws_endpoint}")
            logging.warning(f"graphql_endpoint: {graphql_endpoint}")
            logging.warning(f"rpc_endpoint: {rpc_endpoint}")
            self.env = ENVS.get(env_name)
        else:
            self.env = {
                "base_url": api_endpoint,
                "ws_url": ws_endpoint,
                "subgraph": graphql_endpoint,
                "rpc_url": rpc_endpoint,
            }
        if all([eth_address, private_key]):
            logging.warning(
                f"Shouldn't specify both 'eth_address' and 'private_key'. Address from private key will be used."
            )
        self.address = eth_address
        if private_key:
            self.account = Account.from_key(private_key)
            self.address = self.account.address
        else:
            self.account = None
        self.session = requests.Session()
        self.base_url = self.env.get("base_url")
        self.subgraph_url = self.env.get("subgraph")
        self.ws_url = self.env.get("ws_url")
        self.rpc_url = self.env.get("rpc_url")

        self.auth = Auth(self)
        self.protocol = Protocol(self)
        self.market = Market(self)
        self.client = Client(self)
        self.orders = Orders(self)
        self.calculation = Calculation(self)
        self.socket = Socket(self)
        self.fundlock = Fundlock(self)
        self.analytics = Analytics(self)

    @retry(
        stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=30)
    )
    def post(self, endpoint, json=None):
        """Make Post Request.

        Args:
            endpoint (_type_): _description_
            json (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        verify = False if "localhost" in self.base_url else True
        res = self.session.post(
            self.base_url + endpoint, json=json, verify=verify, timeout=30
        )
        try:
            return res.json()
        except requests.JSONDecodeError as e:
            logging.error(
                f"JSON decode error for POST endpoint {endpoint}, res: {res}, {e}"
            )
            return res
        except Exception as e:
            logging.error(f"error in POST endpoint {endpoint}, res: {res}, {e}")
            raise

    @retry(
        stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=30)
    )
    def get(self, endpoint):
        """Make GET request.

        Args:
            endpoint (_type_): _description_

        Returns:
            _type_: _description_
        """
        headers = {"Content type": "application/json"}
        verify = True if self.base_url.startswith("https") else False
        res = self.session.get(
            self.base_url + endpoint, params=headers, verify=verify, timeout=30
        )
        try:
            return res.json()
        except requests.JSONDecodeError as e:
            logging.error(
                f"JSON decode error for GET endpoint {endpoint}, res: {res}, {e}"
            )
            return res
        except Exception as e:
            logging.error(f"error in GET endpoint {endpoint}, res: {res}, {e}")
            raise

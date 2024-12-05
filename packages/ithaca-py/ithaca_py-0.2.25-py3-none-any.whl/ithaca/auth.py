"""Auth Module."""

import base64
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from eth_account import messages
from eth_typing import Hash32
from eth_utils import keccak
from logger import logger


class Auth:
    """Handle authentication processes, including RSA and Ethereum message signing."""

    def __init__(self, parent, private_key_path="private-key.pem"):
        """
        Initialize the authentication handler.

        Args:
            parent: The parent context or object that holds the Auth instance.
            private_key_path (str): Path to the RSA private key file.
        """
        self.parent = parent
        self.private_key_path = private_key_path
        self.private_key = self.load_private_key()

    def request_auth(self):
        """Request a nonce for authentication from the server."""
        credentials = {"ethAddress": self.parent.address}
        return self.parent.post("/auth/requestAuth", json=credentials)

    def load_private_key(self):
        """
        Load the RSA private key from the specified file.

        Returns:
            The RSA private key or None if the file does not exist.
        """
        if os.path.exists(self.private_key_path):
            with open(self.private_key_path, "rb") as key_file:
                return load_pem_private_key(key_file.read(), password=None)
        return

    def sign_message(self, typed_data) -> str:
        """Sign a message using the appropriate method."""
        if self.private_key:
            return self.sign_rsa_message(typed_data)
        else:
            return self.sign_eth_message(typed_data)

    def validate_key_exist(self):
        """
        Validate that the private key exists.

        Raises:
            ValueError: If the private key does not exist.
        """
        if not self.private_key:
            raise ValueError("Private key does not exist.")

    def _construct_typed_data(self, nonce: str) -> dict:
        """
        Construct the structured data required for EIP-712 signing.

        Args:
            nonce (str): The nonce to be included in the signed message.

        Returns:
            The structured message data.
        """
        return {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                ],
                "AuthMessage": [{"name": "content", "type": "string"}],
            },
            "primaryType": "AuthMessage",
            "domain": {"name": "Ithaca", "version": "0.1"},
            "message": {"content": nonce},
        }

    def sign_eth_message(self, typed_data) -> str:
        """
        Sign a message using the Ethereum account's private key.

        Args:
            nonce (str): The message to sign.

        Returns:
            The signature as a hex string.
        """
        signable_message = messages.encode_typed_data(full_message=typed_data)
        signature = self.parent.account.sign_message(signable_message)

        # Zero-pad the r and s components of the signature to 64 hex characters
        # and v to 2 hex characters
        r_hex = hex(signature.r)[2:].rjust(64, "0")
        s_hex = hex(signature.s)[2:].rjust(64, "0")
        v_hex = hex(signature.v)[2:].rjust(2, "0")

        return ".".join([v_hex, r_hex, s_hex])

    def sign_rsa_message(self, typed_data) -> str:
        """
        Sign a message with the RSA private key.

        Args:
            message (str): The message to sign.

        Returns:
            The Base64 encoded signature.
        """
        self.validate_key_exist()
        signable_message = messages.encode_typed_data(full_message=typed_data)
        joined = (
            b"\x19"
            + signable_message.version
            + signable_message.header
            + signable_message.body
        )
        hashed_data = Hash32(keccak(joined))
        signature = self.private_key.sign(
            hashed_data, padding.PKCS1v15(), hashes.SHA256()
        )
        return f"RSA_SIGN:{base64.b64encode(signature).decode('utf-8')}"

    def generate_rsa_key_pair_and_save(self) -> str:
        """
        Generate an RSA key pair and saves the private key.

        Returns:
            The public key in Base64 encoded DER format.
        """
        if not self.private_key:
            self.private_key = rsa.generate_private_key(
                public_exponent=65537, key_size=2048
            )
            pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
            with open(self.private_key_path, "wb") as key_file:
                key_file.write(pem)
        public_key_der = self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return base64.b64encode(public_key_der).decode("utf-8")

    def login(self) -> bool:
        """
        Attempt to log in using Ethereum signature-based authentication.

        Returns:
            True if login was successful, False otherwise.
        """
        return self._login_with_signature_method(self.sign_eth_message)

    def login_rsa(self) -> bool:
        """
        Attempt to log in using RSA signature-based authentication.

        Returns:
            True if login was successful, False otherwise.
        """
        return self._login_with_signature_method(self.sign_rsa_message)

    def _login_with_signature_method(self, sign_method) -> bool:
        """
        Attempt login using a specified signature method.

        Args:
            sign_method: The method to use for signing the authentication message.

        Returns:
            True if login was successful, False otherwise.
        """
        logger.debug("Attempting login...")
        nonce_response = self.request_auth()
        nonce = nonce_response.get("nonce")
        if nonce:
            logger.debug("Received nonce")
            data = self._construct_typed_data(nonce)
            signature = sign_method(typed_data=data)
            auth_response = self.parent.post(
                "/auth/validateAuth", json={"nonce": nonce, "signature": signature}
            )
            if "payload" in auth_response:
                self.parent.user = auth_response["payload"]
                logger.debug("Login successful.")
                return True
            else:
                logger.debug("Login failed. No payload in auth response.")
        else:
            logger.debug("Login failed. No nonce received.")

        return False

    def link_rsa_key(self):
        """Link the RSA public key to the account.

        By generating a new RSA key pair, saving the private key,
        and sending the public key to the server for association with the user account.

        :return: The server's response to the RSA key link request.
        """
        try:
            public_key = self.generate_rsa_key_pair_and_save()
            credentials = {"rsaPublicKey": public_key}
            response = self.parent.post("/keys/requestLinkRsaKey", json=credentials)
            nonce = response["payload"]
            data = self._construct_typed_data(nonce)
            rsa_signature = self.sign_rsa_message(data)
            eth_signature = self.sign_eth_message(data)
            confirm_response = self.parent.post(
                "/keys/confirmLinkRsaKey",
                json={
                    "nonce": nonce,
                    "rsaSignature": rsa_signature,
                    "signature": eth_signature,
                },
            )
            return confirm_response
        except KeyError:
            # Handle the error (e.g., log it, return a specific value, etc.)
            error_msg = (
                "Error: 'payload' key not found in the response. "
                "This may indicate an RSA key is already linked to the account."
            )
            log.error(error_msg)
            return None
        except Exception as e:
            # Catch other exceptions
            logger.error(f"An unexpected error occurred: {e}")
            return None

    def unlink_rsa_key(self):
        """
        Unlink the RSA key from the account and deletes the private key file.

        :return: The server's response to the RSA key unlink request.
        """
        unlink_response = self.parent.post("/keys/unlink")
        try:
            return unlink_response.json()['result']
        except Exception as e:
            # Catch other exceptions
            logger.error(f"An unexpected error occurred: {e}")
            return None
        

    def remove_private_key(self):
        """Remove the private key file from the filesystem."""
        if os.path.exists(self.private_key_path):
            os.remove(self.private_key_path)
            self.private_key = None

    def get_linked_rsa_key(self):
        """
        Retrieve the RSA key linked to the account from the server.

        :return: The server's response containing the RSA key information.
        """
        return self.parent.get("/keys/getRsaKey")

    def logout(self):
        """Close session with Ithaca backend."""
        return self.parent.post("/auth/logout")

    def get_session_info(self):
        """Get current authenticated session with Ithaca backend."""
        return self.parent.get("/auth/getSessionInfo")

    def add_account_data(self, name, value):
        """Add account data.

        Args:
            name (str): Name of data
            value (str): Value of data
        """
        body = {"name": name, "value": value}
        return self.parent.post("/clientapi/addAccountData", json=body)
    

    def list_linked(self):
        """List linked wallets."""
        return self.parent.get("/linked_wallets/list")
    
    def list_managed_addresses(self):
        """List managed wallets."""
        return self.parent.get("/linked_wallets/switch_list")
    
    def switch_to_managed(self, address):
        """Switch to a managed wallet."""
        return self.parent.post("/auth/switch", {"addr": address.lower()})

    def link_address(self, address):
        """Link an address."""
        response = self.parent.post("/linked_wallets/request_link", {"addr": address.lower()})
        try:
            nonce = response["payload"]
            data = self._construct_typed_data(nonce)
            eth_signature = self.sign_eth_message(data)
            confirm_response = self.parent.post(
                "/linked_wallets/confirm_link",
                json={
                    "nonce": nonce,
                    "signature": eth_signature,
                },
            )
            return confirm_response
        except KeyError:
            # Handle the error (e.g., log it, return a specific value, etc.)
            error_msg = (
                "Error: 'payload' key not found in the response. "
                "This may indicate that wallet is already linked to the account."
            )
            logger.error(error_msg)
            return None
        
    def unlink_address(self, address):
        """Unlink an address."""
        response = self.parent.post("/linked_wallets/unlink", {"addr": address.lower()})
        return response

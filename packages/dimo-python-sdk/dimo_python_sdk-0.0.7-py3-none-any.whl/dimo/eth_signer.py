from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_bytes, remove_0x_prefix, add_0x_prefix


class EthSigner:
    @staticmethod
    def sign_message(message: str, private_key: str) -> str:
        private_key = add_0x_prefix(remove_0x_prefix(private_key))
        message_hash = encode_defunct(text=message)
        account = Account.from_key(private_key)
        signed_message = account.sign_message(message_hash)

        return add_0x_prefix(signed_message.signature.hex())
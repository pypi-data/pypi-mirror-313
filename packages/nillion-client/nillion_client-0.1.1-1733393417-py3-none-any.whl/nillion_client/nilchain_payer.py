from abc import ABCMeta, abstractmethod

from cosmpy.aerial.client import LedgerClient, prepare_and_broadcast_basic_transaction
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey
from nillion_client_proto.nillion.meta.v1.tx_pb2 import MsgPayFor, Amount

from . import Network


class NilChainPayer(metaclass=ABCMeta):
    @abstractmethod
    async def submit_payment(
        self, amount: int, resource: bytes, gas_limit: int | None = None
    ) -> str:
        """Submits a payment to the chain."""
        pass

    @staticmethod
    def prepare_msg(resource: bytes, address, amount) -> MsgPayFor:
        return MsgPayFor(
            resource=resource,
            from_address=address,
            amount=[Amount(denom="unil", amount=str(amount))],
        )


class ChainClient(NilChainPayer):
    def __init__(
        self,
        network: Network,
        wallet_private_key: PrivateKey,
        gas_limit: int,
        wallet_prefix: str = "nillion",
    ):
        self.network = network
        self.payments_wallet = LocalWallet(wallet_private_key, wallet_prefix)
        self.gas_limit = gas_limit
        payments_config = NetworkConfig(
            chain_id=network.chain_id,
            url=f"grpc+http://{network.chain_grpc_endpoint}/",
            fee_minimum_gas_price=0,
            fee_denomination="unil",
            staking_denomination="unil",
            faucet_url=None,
        )
        self.payments_client = LedgerClient(payments_config)

    async def submit_payment(
        self, amount: int, resource: bytes, gas_limit: int | None = None
    ) -> str:
        transaction = Transaction()
        message = ChainClient.prepare_msg(
            resource, str(Address(self.payments_wallet.public_key(), "nillion")), amount
        )
        transaction.add_message(message)

        gas_limit = gas_limit if gas_limit else self.gas_limit
        submitted_transaction = prepare_and_broadcast_basic_transaction(
            self.payments_client, transaction, self.payments_wallet, gas_limit=gas_limit
        )

        submitted_transaction.wait_to_complete()

        return submitted_transaction.tx_hash

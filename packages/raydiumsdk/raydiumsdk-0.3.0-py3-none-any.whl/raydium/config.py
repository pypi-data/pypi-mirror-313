from solana.rpc.api import Client
from solders.keypair import Keypair #type: ignore
import os


PRIV_KEY = os.getenv('PRIVATE_KEY')
RPC = os.getenv('RPC_URL')

UNIT_BUDGET =  100_000
UNIT_PRICE =  1_000_000
client = Client(RPC)
payer_keypair = Keypair.from_base58_string(PRIV_KEY)
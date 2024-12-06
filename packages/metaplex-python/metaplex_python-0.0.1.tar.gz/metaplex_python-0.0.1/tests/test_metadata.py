from metaplex_python import Metadata
import pytest
from solana.rpc.api import Client
from solders.pubkey import Pubkey


@pytest.fixture
def client() -> Client:
    return Client("https://api.mainnet-beta.solana.com")


@pytest.fixture
def token_mint() -> Pubkey:
    return Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")


def test_metadata(client: Client, token_mint: Pubkey) -> None:
    # 1. Get the pubkey for the metadata PDA using the token mint pubkey
    pda_str, bump = Metadata.find_pda(str(token_mint))

    pda = Pubkey.from_string(pda_str)
    assert pda == Pubkey.from_string("5x38Kp4hvdomTCnCrAny4UtMUt5rQBdB6px2K1Ui45Wq")

    # 2. Fetch the account info of the metadata PDA
    response = client.get_account_info(pda)
    assert (value := response.value)

    # 3. Parse the metadata account data
    metadata = Metadata(value.data)
    assert metadata.mint() == str(token_mint)
    assert metadata.symbol() == "USDC"

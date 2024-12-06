class Metadata:
    """
    A class for the Solana [Metaplex token metadata account](https://developers.metaplex.com/token-metadata).
    """

    @staticmethod
    def find_pda(mint_pubkey_str: str) -> tuple[str, int]:
        """
        Finds the PDA and bump of the Metaplex token metadata account of the given token.
        """

    def __init__(self, data: bytes) -> None:
        """
        Initializes a new Metaplex token metadata account with the given account data.
        Note that this account data comes from the `solana.rpc.api.Client.get_account_info` method:

        ```python
        from metaplex_python import Metaplex
        from solana.rpc.api import Client
        from solders.pubkey import Pubkey

        client = Client("https://api.mainnet-beta.solana.com")
        token_mint = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
        pda_str, bump = Metaplex.find_pda(str(token_mint))
        pda = Pubkey.from_string(pda_str)
        response = client.get_account_info(pda)
        metadata = Metaplex(response.value.data)
        ```
        """

    def mint(self) -> str:
        """
        Returns the mint pubkey of the token.
        """

    def symbol(self) -> str:
        """
        Returns the symbol of the token. Right-padded `\0`'s are removed.
        """

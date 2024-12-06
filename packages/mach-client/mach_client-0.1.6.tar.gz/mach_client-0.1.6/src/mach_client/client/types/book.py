from pydantic import BaseModel


class OrderDirection(BaseModel):
    src_token_address: str
    dst_token_address: str
    src_lzc: int
    dst_lzc: int

    def to_eth(self) -> dict:
        return {
            "srcAsset": self.src_token_address,
            "dstAsset": self.dst_token_address,
            "dstLzc": self.dst_lzc,
        }

    def to_tron(self) -> list:
        return [
            self.src_token_address,
            self.dst_token_address,
            self.dst_lzc,
        ]


class OrderFunding(BaseModel):
    src_amount_in: int
    dst_amount_out: int
    bond_token_address: str
    bond_amount: int
    bond_fee: int

    def to_eth(self) -> dict:
        return {
            "srcQuantity": self.src_amount_in,
            "dstQuantity": self.dst_amount_out,
            "bondFee": self.bond_fee,
            "bondAsset": self.bond_token_address,
            "bondAmount": self.bond_amount,
        }

    def to_tron(self) -> list:
        return [
            self.src_amount_in,
            self.dst_amount_out,
            self.bond_fee,
            self.bond_token_address,
            self.bond_amount,
        ]


class OrderExpiration(BaseModel):
    timestamp: int
    challenge_offset: int
    challenge_window: int

    def to_eth(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "challengeOffset": self.challenge_offset,
            "challengeWindow": self.challenge_window,
        }

    def to_tron(self) -> list:
        return [
            self.timestamp,
            self.challenge_offset,
            self.challenge_window,
        ]

from dataclasses import dataclass, fields
from typing import Any, Iterator

from eth_account.messages import encode_typed_data
from eth_utils import keccak

from atlantiscore.lib.string import snake_to_camel_case
from atlantiscore.types import EVMAddress, PrivateKey


@dataclass
class EIP712Domain:
    name: str | None = None
    version: str | None = None
    chain_id: int | None = None
    verifying_contract: EVMAddress | None = None

    def types(self) -> list[dict]:
        types = []
        if self.name is not None:
            types.append(create_type_info("name", "string"))
        if self.version is not None:
            types.append(create_type_info("version", "string"))
        if self.chain_id is not None:
            types.append(create_type_info("chainId", "uint256"))
        if self.verifying_contract is not None:
            types.append(create_type_info("verifyingContract", "address"))
        return types

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        for field in fields(EIP712Domain):
            attr = field.name
            value = getattr(self, attr)
            if value is None:
                continue

            yield (snake_to_camel_case(attr), value)


class EIP712Signer:
    private_key: PrivateKey
    domain: EIP712Domain

    def __init__(self, private_key: PrivateKey, domain: EIP712Domain) -> None:
        self.private_key = private_key
        self.domain = domain

    def sign(
        self,
        message: dict,
        primary_type: str,
        additional_types: dict = {},
    ) -> bytes:
        domain_data = dict(self.domain)
        if verifying_contract := domain_data.get("verifyingContract"):
            domain_data["verifyingContract"] = str(verifying_contract)
        payload = {
            "types": {"EIP712Domain": self.domain.types(), **additional_types},
            "primaryType": primary_type,
            "domain": domain_data,
            "message": message,
        }
        encoded_data = encode_typed_data(full_message=payload)
        return self.private_key.sign_recoverable(
            b"\x19" + encoded_data.version + encoded_data.header + encoded_data.body,
            hasher=keccak,
        )


def create_type_info(name: str, type: str) -> dict[str, str]:
    return {"name": name, "type": type}

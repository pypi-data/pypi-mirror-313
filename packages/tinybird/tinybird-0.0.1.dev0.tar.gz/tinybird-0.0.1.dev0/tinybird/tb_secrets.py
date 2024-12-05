from datetime import datetime
from typing import Any, Dict, Optional, Union

from nacl import secret
from nacl.encoding import Base64Encoder


class Secret:
    def __init__(
        self,
        master_key: Optional[bytes],
        name: str,
        value: str | bytes,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        edited_by: Optional[str] = None,
    ) -> None:
        """
        >>> secret = Secret(Base64Encoder.decode("T67++TQ85w+bJH5jHKkdenvQyloztdipgP8F1q+w4CY=".encode()), "test", "1234")
        >>> assert(secret.value)
        """
        self.name = name
        if master_key:
            assert isinstance(value, str)
            self.value = self.encrypt(master_key, value)
        else:
            assert isinstance(value, bytes)
            self.value = value
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.edited_by = edited_by

    @classmethod
    def from_dict(cls, secret: Dict[str, Any]) -> "Secret":
        return Secret(
            master_key=None,
            name=secret["name"],
            value=secret["value"],
            created_at=secret.get("created_at"),
            updated_at=secret.get("updated_at"),
            edited_by=secret.get("edited_by"),
        )

    def __repr__(self) -> str:
        return f"secret: {self.name}"

    def __eq__(self, other: Union["Secret", Any]) -> bool:
        return other is not None and isinstance(self, type(other)) and (self.name == other.name)

    def touch(self):
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "edited_by": self.edited_by,
            "type": "secret",
        }

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "edited_by": self.edited_by,
            "type": "secret",
        }

    def to_json(self) -> Dict[str, Any]:
        secret = self.to_public_dict()
        secret["created_at"] = secret["created_at"].isoformat()
        secret["updated_at"] = secret["updated_at"].isoformat()
        return secret

    def encrypt(self, secrets_key: bytes, value: str) -> bytes:
        box = secret.SecretBox(secrets_key)
        encrypted = box.encrypt(value.encode())
        return Base64Encoder.encode(encrypted)


def secret_decrypt(secrets_key: bytes, value: bytes) -> str:
    """
    >>> secret_decrypt(Base64Encoder.decode("T67++TQ85w+bJH5jHKkdenvQyloztdipgP8F1q+w4CY=".encode()), b'XDZFehn9iryWQSGZkZyf79fMS7d28ncsHb4dHo2el7XoOrHQ78VDRolwZZg=')
    '1234'
    """
    box = secret.SecretBox(secrets_key)
    encrypted = Base64Encoder.decode(value)
    return box.decrypt(encrypted).decode()

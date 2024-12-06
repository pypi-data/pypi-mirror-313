from typing import Dict, List, Mapping, Union, Tuple

NadaValue = Union[
    SecretUnsignedInteger,
    SecretInteger,
    SecretBoolean,
    Array,
    SecretBlob,
    UnsignedInteger,
    Integer,
    Boolean,
    EcdsaPrivateKey,
    EcdsaDigestMessage,
    EcdsaSignature,
]

class SecretUnsignedInteger:
    """Encodes a secret as an unsigned integer."""

    value: int

    def __init__(self, value: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class SecretInteger:
    """Encodes a secret as an integer."""

    value: int

    def __init__(self, value: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class SecretBoolean:
    """Encodes a secret as a boolean."""

    value: bool

    def __init__(self, value: bool) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class Array:
    """Encodes multiple values as an array."""

    value: List[NadaValue]

    def __init__(self, value: List[NadaValue]) -> None: ...
    def __len__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class SecretBlob:
    """Encodes a secret as a blob."""

    value: bytearray

    def __init__(self, value: bytearray) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class UnsignedInteger:
    """Encodes a public variable value as an unsigned integer."""

    value: int

    def __init__(self, value: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class Integer:
    """Encodes a public variable value as an integer."""

    value: int

    def __init__(self, value: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class Boolean:
    """Encodes a public variable value as a boolean."""

    value: bool

    def __init__(self, value: bool) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class EcdsaPrivateKey:
    """Encodes a secret as an ecdsa private key."""

    value: bytearray

    def __init__(self, value: bytearray) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class EcdsaDigestMessage:
    """Encodes an ecdsa digest message."""

    value: bytearray

    def __init__(self, value: bytearray) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class EcdsaSignature:
    """Encodes an ecdsa signature."""

    value: Tuple[bytearray, bytearray]

    def __init__(self, value: Tuple[bytearray, bytearray]) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

class ProgramRequirements:
    """A program preprocessing requirements"""

    alpha_elements: int
    """The amount of alphas required by the program"""

    runtime_elements: Dict[str, int]
    """A dictionary of runtime elements required by the program"""

class ProgramMetadata:
    """Metadata for a Nada program."""

    memory_size: int
    """The program memory size"""

    total_instructions: int
    """The total number of instructions"""

    instructions: Dict[str, int]
    """The program instructions"""

    preprocessing_requirements: ProgramRequirements
    """The program preprocessing requirements"""

def extract_program_metadata(program: bytes) -> ProgramMetadata:
    """Extract the program metadata to be used when uploading a program."""
    ...

class EncryptedNadaValue:
    """An encrypted Nada value."""

    ...

class EncryptedNadaValues:
    """A collection of encrypted Nada values."""

    ...

def decode_values(bincode_bytes: bytes) -> EncryptedNadaValues:
    """Decode a set of values."""
    ...

def encode_values(values: EncryptedNadaValues) -> bytes:
    """Encode a set of values."""
    ...

def compute_values_size(values: Mapping[str, NadaValue]) -> int:
    """Compute the size of encoded values."""
    ...

class PartyId:
    """Represents a party identifier."""

    @classmethod
    def new(cls, id: str) -> PartyId: ...
    @classmethod
    def from_bytes(cls, bytes: bytes) -> "PartyId": ...
    """Creates a party identifier from an array of bytes."""

class PartyJar:
    """A jar where every party puts an element."""

    @classmethod
    def new(cls, count: int) -> PartyJar: ...
    def add_element(self, party: PartyId, element: EncryptedNadaValues): ...
    """Adds an element to the jar."""

class EncryptedPartyShares:
    """Each party's shares."""

    def get(self, party_id: PartyId) -> EncryptedNadaValues: ...

class NadaValuesClassification:
    """A classification of Nada values."""

    particles: int
    """The number of particles."""

    shares: int
    """The number of shares."""

    public: int
    """The number of public values."""

    ecdsa_private_key_shares: int
    """The number of ecdsa private key shares."""

class SecretMasker:
    """A secret masker. This allows masking and unmasking secrets."""

    @classmethod
    def new_64_bit_safe_prime(
        cls, polynomial_degree: int, parties: List[PartyId]
    ) -> "SecretMasker":
        """Construct a new masker that uses a 64 bit safe prime under the hood."""

    @classmethod
    def new_128_bit_safe_prime(
        cls, polynomial_degree: int, parties: List[PartyId]
    ) -> "SecretMasker":
        """Construct a new masker that uses a 128 bit safe prime under the hood."""

    @classmethod
    def new_256_bit_safe_prime(
        cls, polynomial_degree: int, parties: List[PartyId]
    ) -> "SecretMasker":
        """Construct a new masker that uses a 256 bit safe prime under the hood."""

    def mask(self, values: Mapping[str, NadaValue]) -> EncryptedPartyShares:
        """Mask a set of values."""

    def unmask(self, jar: PartyJar) -> Dict[str, NadaValue]:
        """Unmask a set of values."""

    def classify_values(
        self, values: Mapping[str, NadaValue]
    ) -> NadaValuesClassification:
        """Classify the given cleartext values. This allows getting the totals per value type which is a required parameter when storing values."""

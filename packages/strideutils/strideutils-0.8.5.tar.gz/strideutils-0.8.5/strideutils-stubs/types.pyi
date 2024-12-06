from enum import Enum

class DepositRecordStatus(str, Enum):
    TRANSFER_QUEUE: str
    TRANSFER_IN_PROGRESS: str
    DELEGATION_QUEUE: str
    DELEGATION_IN_PROGRESS: str

class CallbackId(str, Enum):
    TRANSFER: str
    DELEGATE: str
    UNDELEGATE: str
    REDEMPTION: str

class UnbondingRecordStatus(str, Enum):
    UNBONDING_QUEUE: str
    UNBONDING_IN_PROGRESS: str
    EXIT_TRANSFER_QUEUE: str
    EXIT_TRANSFER_IN_PROGRESS: str
    CLAIMABLE: str

from enum import Enum


class RollType(Enum):
    approver = "approver"
    complainer = "complainer"
    admin = "admin"


class State(Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"

from typing import Optional

from pydantic import BaseModel, Field


class SolverRequest(BaseModel):
    """
    Request for a solver, with inputs and quality guarantees.
    """

    solverInput: Optional[BaseModel] = None
    falsePositiveRate: float = 0.01

    class Config:
        extra = "forbid"


class SolverReceipt(BaseModel):
    """
    Solver receipt as bloom filter and number of inserted items.
    """

    bloomFilter: bytes = b"BgAAAAAAAADYxCJU"
    countItems: int = 0

    class Config:
        extra = "forbid"


class SolverResponse(BaseModel):
    """
    Solver response with output and receipt.
    """

    solverOutput: Optional[BaseModel] = None
    solverReceipt: SolverReceipt = SolverReceipt()

    class Config:
        extra = "forbid"


class VerifierRequest(BaseModel):
    """
    Verifier request, with solver request and solver receipt as
    input, as well as `verificationRatio` to control the minimum required confidence.
    """

    solverRequest: SolverRequest = SolverRequest()
    solverReceipt: SolverReceipt = SolverReceipt()
    verificationRatio: float = Field(0.1, ge=0, le=1)

    class Config:
        extra = "forbid"


class VerifierResponse(BaseModel):
    """
    Verifier response, with number of verified items and
    the verification outcome.
    """

    countItems: int = 0
    isVerified: bool = False

    class Config:
        extra = "forbid"

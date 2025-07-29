from pydantic import BaseModel, Field


class PowerInput(BaseModel):
    base: float = Field(..., description="Base must be a float")
    exponent: float = Field(..., description="Exponent must be a float")


class FibonacciInput(BaseModel):
    n: int = Field(ge=0, description="n must be >= 0")


class FactorialInput(BaseModel):
    n: int = Field(ge=0, description="n must be >= 0")

from pydantic import BaseModel, Field

class PowerInput(BaseModel):
    base: float
    exponent: float

class FibonacciInput(BaseModel):
    n: int = Field(ge=0, description="n must be >= 0")

class FactorialInput(BaseModel):
    n: int = Field(ge=0, description="n must be >= 0")

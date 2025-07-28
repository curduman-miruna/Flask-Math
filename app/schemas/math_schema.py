from pydantic import BaseModel, Field

class PowerInput(BaseModel):
    base: float = Field(ge=-1e5, le=1e5, description="Base must be between -100,000 and 100,000")
    exponent: float = Field(ge=-10_000, le=10_000, description="Exponent must be between -10,000 and 10,000")

class FibonacciInput(BaseModel):
    n: int = Field(ge=0, le=10_000_000, description="n must be >= 0 and <= 10 million")
class FactorialInput(BaseModel):
    n: int = Field(ge=0, le=1_000_000, description="n must be >= 0 and <= 1 million")

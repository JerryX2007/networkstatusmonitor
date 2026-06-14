from pydantic import BaseModel, Field

class Monitor(BaseModel):
    name: str = Field(min_length=1)
    target: str = Field(min_length=1)
    port: int = Field(gt=0, lt=65536, default=80)
    timeout: float = Field(gt=0, default=3.0)
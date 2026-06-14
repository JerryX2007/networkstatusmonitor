from pydantic import BaseModel

class Monitor(BaseModel):
    name: str
    target: str
    port: int = 80
    timeout: float = 3.0
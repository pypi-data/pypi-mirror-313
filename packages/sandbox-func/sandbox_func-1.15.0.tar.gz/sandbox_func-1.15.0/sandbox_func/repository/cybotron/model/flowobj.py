from pydantic import BaseModel


class FlowWebRequest(BaseModel):
    input: dict = {}
    skipSteps: list = []
    debug: bool = False

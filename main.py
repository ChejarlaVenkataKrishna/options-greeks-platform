from fastapi import FastAPI
from greeks import BlackScholes
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    S: float
    K: float
    T: float
    r: float
    sigma: float
    option_type: str

@app.post("/calculate")
def calculate(data: InputData):
    model = BlackScholes(data.S, data.K, data.T, data.r, data.sigma)

    return {
        "price": model.call_price() if data.option_type=='call' else model.put_price(),
        "delta": model.delta(data.option_type),
        "gamma": model.gamma(),
        "vega": model.vega(),
        "theta": model.theta(data.option_type),
        "rho": model.rho(data.option_type)
    }
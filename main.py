import datetime

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import uvicorn


app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": "Running"})


@app.get("/")
def main():
    xmas = datetime.datetime(datetime.datetime.now().year, 12, 25)
    today = datetime.datetime.now()
    days_to_xmas = (xmas - today).days

    return {'Days' : days_to_xmas}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, log_level="warning")

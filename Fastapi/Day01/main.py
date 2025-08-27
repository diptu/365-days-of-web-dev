from fastapi import FastAPI

from enum import Enum

app = FastAPI()


class JobType(str, Enum):
    PT = "Part-Time"
    FT = "Full-Time"
    CN = "Contructual"


@app.get("/")
async def health_check():
    return {"mesage": "ok"}


@app.get("/jobs/{type}")
async def get_item(job_type: JobType):
    if job_type is job_type.PT:
        return {"msg": "You are a part time employee"}
    if job_type is job_type.FT:
        return {"msg": "You are a Full time employee"}
    return {"msg": "You are a Contructual employee"}


def main():
    print("Hello from day01!")


if __name__ == "__main__":
    main()

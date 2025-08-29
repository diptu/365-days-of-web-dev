# main.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.v1.endpoints.endpoint:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

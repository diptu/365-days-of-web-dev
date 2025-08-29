# main.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",  # points to the `app` object inside app/__init__.py
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

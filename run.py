import uvicorn
import os

if __name__ == "__main__":
    # Start the FastAPI uvicorn server on port 8000
    print("Initializing AI Document Classifier FastAPI Server on http://localhost:8000")
    print("API Documentation available at http://localhost:8000/docs")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

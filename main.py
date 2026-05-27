from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, labels, documents, classifier, analytics

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Document Classifier API",
    description="Backend services for user authentication, document text extraction, label management, and scikit-learn model training/predictions.",
    version="1.0.0"
)

# Configure CORS for local development integrations
# Allow the default Vite port (5173), common React ports, and localhost wildcards
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth.router)
app.include_router(labels.router)
app.include_router(documents.router)
app.include_router(classifier.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "AI Document Classifier REST API is operating successfully.",
        "docs_url": "/docs"
    }

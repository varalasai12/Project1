from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# ==========================================
# Auth Schemas
# ==========================================
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

# ==========================================
# Label / Category Schemas
# ==========================================
class LabelCreate(BaseModel):
    name: str
    color: Optional[str] = "#3B82F6"

class LabelResponse(BaseModel):
    id: int
    name: str
    color: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ==========================================
# Document Schemas
# ==========================================
class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    uploaded_at: datetime
    is_test_set: bool
    label: Optional[LabelResponse] = None

    class Config:
        from_attributes = True

class DocumentLabelUpdate(BaseModel):
    label_id: Optional[int] = None

class DocumentPreview(BaseModel):
    id: str
    filename: str
    file_type: str
    extracted_text: Optional[str] = None

# ==========================================
# ML & Model Training Schemas
# ==========================================
class ModelTrainingResponse(BaseModel):
    id: str
    trained_at: datetime
    accuracy: str
    precision: str
    recall: str
    f1_score: str
    confusion_matrix: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True

class KeywordHighlight(BaseModel):
    word: str
    score: float
    importance: float  # coefficient driving weight

class PredictionResponse(BaseModel):
    predicted_label: str
    label_id: Optional[int] = None
    confidence: float
    extracted_keywords: List[str]
    word_highlights: List[Dict[str, Any]]
    text_snippet: str

# ==========================================
# Activity & Analytics Schemas
# ==========================================
class ActivityLogResponse(BaseModel):
    id: int
    action: str
    details: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_documents: int
    labeled_documents: int
    unlabeled_documents: int
    active_labels: int
    model_accuracy: Optional[str] = "N/A"
    recent_documents: List[DocumentResponse]
    activities: List[ActivityLogResponse]

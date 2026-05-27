import datetime
import uuid
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    labels = relationship("Label", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    models = relationship("ModelTraining", back_populates="user", cascade="all, delete-orphan")
    activities = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color = Column(String, default="#3B82F6") # Tailwind Blue hex
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="labels")
    documents = relationship("Document", back_populates="label")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    file_type = Column(String, nullable=False) # 'pdf', 'docx', 'txt'
    extracted_text = Column(Text, nullable=True)
    is_test_set = Column(Boolean, default=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    label_id = Column(Integer, ForeignKey("labels.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="documents")
    label = relationship("Label", back_populates="documents")


class ModelTraining(Base):
    __tablename__ = "model_trainings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trained_at = Column(DateTime, default=datetime.datetime.utcnow)
    accuracy = Column(String, nullable=True)  # Store formatted floats/percents
    precision = Column(String, nullable=True)
    recall = Column(String, nullable=True)
    f1_score = Column(String, nullable=True)
    confusion_matrix = Column(Text, nullable=True)  # JSON-encoded array of actual vs predicted counts
    model_path = Column(String, nullable=False)
    vectorizer_path = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="models")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False) # e.g., 'UPLOAD', 'TRAIN', 'PREDICT', 'LABEL_CREATE'
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="activities")

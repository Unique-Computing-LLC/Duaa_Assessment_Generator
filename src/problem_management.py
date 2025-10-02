"""
Simplified Problem Management System
"""
import uuid
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class ProblemLibrary(Base):
    __tablename__ = 'problem_libraries'
    id = Column(Integer, primary_key=True)
    library_id = Column(String(36), unique=True, nullable=False)
    course_id = Column(String(50), nullable=False)
    course_name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())

class ProblemCollection(Base):
    __tablename__ = 'problem_collections'
    id = Column(Integer, primary_key=True)
    collection_id = Column(String(36), unique=True, nullable=False)
    library_id = Column(String(36), ForeignKey('problem_libraries.library_id'))
    day_id = Column(String(50), nullable=False)
    day_name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())

class ProblemBank(Base):
    __tablename__ = 'problem_banks'
    id = Column(Integer, primary_key=True)
    bank_id = Column(String(36), unique=True, nullable=False)
    collection_id = Column(String(36), ForeignKey('problem_collections.collection_id'))
    lesson_id = Column(String(50), nullable=False)
    lesson_name = Column(String(200), nullable=False)
    topic = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question_id = Column(String(36), unique=True, nullable=False)
    question_json = Column(JSON, nullable=False)
    problem_bank_id = Column(String(36), ForeignKey('problem_banks.bank_id'))
    topic = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=lambda: __import__('datetime').datetime.utcnow())

class ProblemManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url, future=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, future=True)
        Base.metadata.create_all(bind=self.engine)
    
    def create_hierarchy(self, course_id, course_name, day_id, day_name, lesson_id, lesson_name, topic):
        session = self.SessionLocal()
        try:
            # Create library
            library_id = str(uuid.uuid4())
            library = ProblemLibrary(library_id=library_id, course_id=course_id, course_name=course_name)
            session.add(library)
            session.flush()  # Flush to get the ID
            
            # Create collection
            collection_id = str(uuid.uuid4())
            collection = ProblemCollection(collection_id=collection_id, library_id=library_id, day_id=day_id, day_name=day_name)
            session.add(collection)
            session.flush()  # Flush to get the ID
            
            # Create bank
            bank_id = str(uuid.uuid4())
            bank = ProblemBank(bank_id=bank_id, collection_id=collection_id, lesson_id=lesson_id, lesson_name=lesson_name, topic=topic)
            session.add(bank)
            
            session.commit()
            return {"library_id": library_id, "collection_id": collection_id, "bank_id": bank_id}
        finally:
            session.close()
    
    def assign_question(self, question_id, bank_id):
        session = self.SessionLocal()
        try:
            question = session.query(Question).filter(Question.question_id == question_id).first()
            if question:
                question.problem_bank_id = bank_id
                session.commit()
                return True
            return False
        finally:
            session.close()
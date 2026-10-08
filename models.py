from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String)
    date = Column(String)
    status = Column(String, default="PROCESSING")
    total = Column(Integer)
    successful = Column(Integer, default=0)
    failed = Column(Integer, default=0)


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    name = Column(String)
    email = Column(String)
    status = Column(String)
    file_path = Column(String, nullable=True)
    error = Column(String, nullable=True)
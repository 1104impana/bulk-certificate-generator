from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Job, Certificate
from certificate import generate_certificate


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bulk Certificate Generator")


# ---------- Database dependency ----------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ---------- Request schemas ----------

class Recipient(BaseModel):
    name: str
    email: EmailStr


class CertificateRequest(BaseModel):
    event_name: str
    date: str
    recipients: list[Recipient]


# ---------- Create generation job ----------

@app.post("/api/certificates/")
def create_certificates(
    request: CertificateRequest,
    db: Session = Depends(get_db)
):

    if not request.recipients:
        raise HTTPException(
            status_code=400,
            detail="Recipients list cannot be empty"
        )

    job = Job(
        event_name=request.event_name,
        date=request.date,
        status="PROCESSING",
        total=len(request.recipients),
        successful=0,
        failed=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient in request.recipients:

        certificate = Certificate(
            job_id=job.id,
            name=recipient.name,
            email=recipient.email,
            status="PROCESSING"
        )

        db.add(certificate)
        db.commit()
        db.refresh(certificate)

        try:
            path = generate_certificate(
                recipient.name,
                request.event_name,
                request.date,
                certificate.id
            )

            certificate.status = "SUCCESS"
            certificate.file_path = path
            job.successful += 1

        except Exception as e:

            certificate.status = "FAILED"
            certificate.error = str(e)
            job.failed += 1

        db.commit()

    job.status = "COMPLETED"
    db.commit()

    return {
        "job_id": job.id,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed
    }


# ---------- Job status ----------

@app.get("/api/certificates/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    certificates = (
        db.query(Certificate)
        .filter(Certificate.job_id == job_id)
        .all()
    )

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed,
        "certificates": [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "status": c.status,
                "error": c.error
            }
            for c in certificates
        ]
    }


# ---------- Download certificate ----------

@app.get("/api/certificates/{job_id}/{certificate_id}")
def download_certificate(
    job_id: int,
    certificate_id: int,
    db: Session = Depends(get_db)
):

    certificate = (
        db.query(Certificate)
        .filter(
            Certificate.id == certificate_id,
            Certificate.job_id == job_id
        )
        .first()
    )

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if certificate.status != "SUCCESS":
        raise HTTPException(
            status_code=400,
            detail="Certificate was not generated successfully"
        )

    return FileResponse(
        certificate.file_path,
        media_type="application/pdf",
        filename=f"{certificate.name}_certificate.pdf"
    )
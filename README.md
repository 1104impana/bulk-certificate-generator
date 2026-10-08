# Bulk Certificate Generator

A backend API for generating certificates in bulk for multiple recipients using a predefined certificate template.

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- ReportLab
- Pydantic

## Features

- Bulk certificate generation
- Recipient data validation
- PDF certificate generation
- Job status tracking
- Individual certificate status tracking
- Certificate download
- Individual certificate failure handling
- REST API documentation using FastAPI Swagger UI

## Project Structure

```text
certificate-generator/
|
├── generated/
|   └── Generated certificate PDFs
|
├── main.py
├── database.py
├── models.py
├── certificate.py
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd certificate-generator
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### 1. Create Certificate Generation Job

```text
POST /api/certificates/
```

Example request:

```json
{
  "event_name": "Python Workshop",
  "date": "2026-10-08",
  "recipients": [
    {
      "name": "Impana",
      "email": "impana@example.com"
    },
    {
      "name": "Rahul",
      "email": "rahul@example.com"
    }
  ]
}
```

Example response:

```json
{
  "job_id": 1,
  "status": "COMPLETED",
  "total": 2,
  "successful": 2,
  "failed": 0
}
```

### 2. Get Job Status

```text
GET /api/certificates/{job_id}
```

Example:

```text
GET /api/certificates/1
```

Example response:

```json
{
  "job_id": 1,
  "event_name": "Python Workshop",
  "status": "COMPLETED",
  "total": 2,
  "successful": 2,
  "failed": 0,
  "certificates": [
    {
      "id": 1,
      "name": "Impana",
      "email": "impana@example.com",
      "status": "SUCCESS",
      "error": null
    },
    {
      "id": 2,
      "name": "Rahul",
      "email": "rahul@example.com",
      "status": "SUCCESS",
      "error": null
    }
  ]
}
```

### 3. Download Certificate

```text
GET /api/certificates/{job_id}/{certificate_id}
```

Example:

```text
GET /api/certificates/1/1
```

The endpoint returns the generated PDF certificate.

## Processing Flow

```text
Client
  |
  | POST certificate generation request
  v
FastAPI
  |
  | Validate recipient data
  v
Create Generation Job
  |
  | Process each recipient
  v
Generate PDF Certificate
  |
  +---- Success ----> Save certificate and mark SUCCESS
  |
  +---- Failure -----> Record error and mark FAILED
  |
  v
Update Job Status
  |
  v
Return Job Result
```

## Database Design

The application uses two main tables.

### Jobs

Stores information about each bulk generation request.

Fields include:

- Job ID
- Event name
- Date
- Status
- Total recipients
- Successful generations
- Failed generations

### Certificates

Stores information about each individual certificate.

Fields include:

- Certificate ID
- Job ID
- Recipient name
- Recipient email
- Generation status
- Generated file path
- Error message

## Design Decisions

### FastAPI

FastAPI was selected because it provides simple REST API development, automatic request validation, and automatically generated Swagger documentation.

### SQLite

SQLite was selected for the MVP because it requires no separate database server and is easy to set up locally. SQLAlchemy allows the database layer to be migrated to PostgreSQL or another relational database later.

### ReportLab

ReportLab is used to generate PDF certificates programmatically. A single predefined certificate format is used as required.

### Synchronous Processing

The MVP processes all recipients within the API request. This keeps the implementation simple and avoids additional infrastructure such as Redis or Celery.

For a production system handling a large number of certificates, generation could be moved to background workers. The API could return a job ID immediately while workers process certificates asynchronously.

### Individual Failure Handling

Each recipient is processed independently. If certificate generation fails for one recipient, the error is recorded and the remaining recipients continue to be processed.

## Validation and Failure Handling

The API validates:

- Event name
- Date
- Recipient name
- Recipient email
- Non-empty recipient list

Each certificate has its own status:

```text
PROCESSING
SUCCESS
FAILED
```

A failed certificate does not prevent other valid certificates from being generated.

## Testing

Run tests using:

```bash
pytest
```

Tests can cover:

- Creating a generation job
- Recipient input validation
- Certificate generation
- Job status
- Individual certificate failure
- Certificate retrieval

## Future Scope

- Background processing using Celery and Redis
- PostgreSQL for production database storage
- Multiple certificate templates
- Emailing certificates to recipients
- Cloud storage for generated certificates
- Retry mechanism for failed certificates
- Authentication and authorization
- Job cancellation
- Certificate generation history

## Learning

This project provided practical experience with:

- REST API development using FastAPI
- Request validation using Pydantic
- Relational database design
- SQLAlchemy ORM
- PDF generation using ReportLab
- Bulk processing
- Error handling
- API documentation
- Backend architecture and design decisions

## Environment Variables and Configuration

The current MVP does not require any environment variables or external configuration files.

### Database

The application uses SQLite by default:

```text
sqlite:///./certificates.db
```

The database file `certificates.db` is automatically created in the project directory when the application starts.

### Generated Certificates

Generated PDF certificates are stored in:

```text
generated/
```

The directory is automatically created by the application if it does not already exist.

### Application Configuration

The FastAPI application runs locally using:

```bash
uvicorn main:app --reload
```

Default application URL:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Production Configuration

For a production deployment, configuration can be moved to environment variables. Recommended variables include:

```text
DATABASE_URL
GENERATED_CERTIFICATE_PATH
APP_ENV
```

For example:

```text
DATABASE_URL=postgresql://user:password@localhost/certificates
GENERATED_CERTIFICATE_PATH=generated/
APP_ENV=production
```

Environment variables are not required for the current MVP.

## Author

Impana T.
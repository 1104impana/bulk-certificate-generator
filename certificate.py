import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def generate_certificate(name, event_name, date, certificate_id):
    os.makedirs("generated", exist_ok=True)

    path = f"generated/certificate_{certificate_id}.pdf"

    c = canvas.Canvas(path, pagesize=A4)

    width, height = A4

    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(
        width / 2,
        height - 180,
        "CERTIFICATE OF PARTICIPATION"
    )

    c.setFont("Helvetica", 18)
    c.drawCentredString(
        width / 2,
        height - 250,
        "This certificate is proudly presented to"
    )

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(
        width / 2,
        height - 310,
        name
    )

    c.setFont("Helvetica", 16)
    c.drawCentredString(
        width / 2,
        height - 370,
        f"for participating in {event_name}"
    )

    c.drawCentredString(
        width / 2,
        height - 410,
        f"Date: {date}"
    )

    c.save()

    return path
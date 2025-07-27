from fpdf import FPDF
import os

def generate_loan_pdf(user, answers, uploaded_files=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="HSBC Loan Application", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Applicant: {user.name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {user.email}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {user.phone}", ln=True)
    pdf.cell(200, 10, txt=f"Annual Income: £{user.annual_income}", ln=True)
    pdf.cell(200, 10, txt=f"Employment Status: {user.employment_status}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Loan Type: {answers.get('loan_type')}", ln=True)
    pdf.cell(200, 10, txt=f"Amount: £{answers.get('amount')}", ln=True)
    pdf.cell(200, 10, txt=f"Term: {answers.get('term_months', 'N/A')} months", ln=True)
    pdf.cell(200, 10, txt=f"Status: {answers.get('status', 'Pending')}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Uploaded Documents:", ln=True)
    if uploaded_files:
        for fname in uploaded_files:
            pdf.cell(200, 10, txt=f"- {fname}", ln=True)
    else:
        pdf.cell(200, 10, txt="None", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Declaration: I confirm that the above information is correct.", ln=True)
    # Save PDF
    pdf_dir = "static/pdfs"
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"loan_application_{user.id}.pdf")
    pdf.output(pdf_path)
    return pdf_path

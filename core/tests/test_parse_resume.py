from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from core.utils.parse_resume import extract_text_from_uploaded_file

class ParseResumeTests(TestCase):
    def test_extract_text_from_sample_pdf(self):
        with open("core/tests/data/sample_text_pdf.pdf", "rb") as f:
            up = SimpleUploadedFile("sample.pdf", f.read(), content_type="application/pdf")
            text = extract_text_from_uploaded_file(up, ocr_if_empty=False)
            self.assertTrue(len(text) > 10)

    def test_extract_text_from_docx(self):
        with open("core/tests/data/sample.docx", "rb") as f:
            up = SimpleUploadedFile("sample.docx", f.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            text = extract_text_from_uploaded_file(up)
            self.assertTrue("Experience" in text or len(text) > 5)

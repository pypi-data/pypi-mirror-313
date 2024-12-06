import pytest
import unittest
import os
from unittest.mock import patch, Mock
import json

from ecom_data_helpers.document_extraction import (
    extract_docx_to_text,
    extract_pdf_to_text,
    doc_url_to_bytes,
    DocumentProcessor,
    Config,
    analyze_pdf_invoice,
    analyze_image_invoice
)

from ecom_data_helpers.exceptions import (
    PdfImageExtractionExeception,
    DocumentDownloadError,
    TextExtractionError
)

class TestEcomDataHelpersDocumentExtraction(unittest.TestCase):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_extract_docx_to_text_with_success(self):
        filepath = self.ROOT_DIR + "/data/exemplo.docx"
        
        with open(filepath, 'rb') as file: 
            text = extract_docx_to_text(doc_bytes=file.read())
            assert isinstance(text, str)
            assert len(text) > 0

    def test_extract_docx_to_text_with_error(self):
        with pytest.raises(TextExtractionError):
            extract_docx_to_text(doc_bytes=b'invalid bytes')

    def test_extract_pdf_to_text_with_success(self):
        filepath = self.ROOT_DIR + "/data/exemplo.pdf"
        
        with open(filepath, 'rb') as file: 
            text, conversion_process = extract_pdf_to_text(doc_bytes=file.read())
            assert len(text) > 100
            assert conversion_process == 'raw_pdf'

    def test_extract_pdf_to_text_with_error(self):
        with pytest.raises(TextExtractionError):
            extract_pdf_to_text(doc_bytes=b'invalid bytes')

    # def test_extract_pdf_to_text_with_success(self):
    #     filepath = self.ROOT_DIR + "/data/invoce-pdf.pdf"
        
    #     with open(filepath, 'rb') as file: 
    #         analysis = analyze_pdf_invoice(doc_bytes=file.read())
    #         assert isinstance(analysis, dict)
    #         assert len(analysis) > 0

    # def test_analyze_image_invoice_with_success(self):
    #     filepath = self.ROOT_DIR + "/data/invoice-image.jpg"
        
    #     with open(filepath, 'rb') as file: 
    #         analysis = analyze_image_invoice(doc_bytes=file.read())
    #         assert isinstance(analysis, dict)
    #         assert len(analysis) > 0

    def test_document_processor_check_file_type(self):
        # Test PDF detection
        assert DocumentProcessor.check_file_type(b'%PDF-1.4') == 'pdf'
        
        # Test DOCX detection
        assert DocumentProcessor.check_file_type(b'PK\x03\x04') == 'docx'
        
        # Test unknown type
        assert DocumentProcessor.check_file_type(b'other content') == 'unknown'

    def test_config_get_poppler_path(self):
        with patch('os.name', 'nt'):
            assert Config.get_poppler_path() == Config.POPPLER_PATH_WINDOWS
        
        with patch('os.name', 'posix'):
            assert Config.get_poppler_path() == Config.POPPLER_PATH_LINUX

if __name__ == "__main__":
    unittest.main()
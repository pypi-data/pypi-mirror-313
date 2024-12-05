import pytest
import unittest
import os
from unittest.mock import patch, Mock, mock_open
import json

from ecom_data_helpers.document_extraction import (
    extract_docx_to_text,
    extract_pdf_to_text,
    doc_url_to_bytes,
    DocumentProcessor,
    Config
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

    # def test_extract_pdf_to_text_force_image_conversion(self):
    #     filepath = self.ROOT_DIR + "/data/exemplo.pdf"
        
    #     with patch('ecom_data_helpers.document_extraction.convert_from_bytes') as mock_convert:
    #         mock_image = Mock()
    #         mock_convert.return_value = [mock_image]
            
    #         with patch.object(DocumentProcessor, 'process_pdf_page_as_image') as mock_process:
    #             mock_process.return_value = "Extracted text"
                
    #             with open(filepath, 'rb') as file:
    #                 text, conversion_process = extract_pdf_to_text(
    #                     doc_bytes=file.read(),
    #                     force_image_conversion=True
    #                 )
                    
    #                 assert conversion_process == 'pdf_to_image'
    #                 assert text == "Extracted text"
    #                 mock_convert.assert_called_once()
    #                 mock_process.assert_called_once()

    def test_extract_pdf_to_text_with_error(self):
        with pytest.raises(TextExtractionError):
            extract_pdf_to_text(doc_bytes=b'invalid bytes')

    def test_document_processor_check_file_type(self):
        # Test PDF detection
        assert DocumentProcessor.check_file_type(b'%PDF-1.4') == 'pdf'
        
        # Test DOCX detection
        assert DocumentProcessor.check_file_type(b'PK\x03\x04') == 'docx'
        
        # Test unknown type
        assert DocumentProcessor.check_file_type(b'other content') == 'unknown'

    # def test_document_processor_extract_text_from_image_error(self):
    #     with patch('boto3.client') as mock_boto3:
    #         mock_textract = Mock()
    #         mock_boto3.return_value = mock_textract
    #         mock_textract.detect_document_text.side_effect = Exception('Textract error')
            
    #         with pytest.raises(TextExtractionError):
    #             DocumentProcessor.extract_text_from_image(b'image content')

    # def test_document_processor_process_pdf_page_as_image(self):
    #     mock_image = Mock()
    #     mock_extracted_text = "Extracted text from image"
        
    #     with patch('builtins.open', mock_open()) as mock_file:
    #         with patch.object(DocumentProcessor, 'extract_text_from_image') as mock_extract:
    #             mock_extract.return_value = mock_extracted_text
                
    #             result = DocumentProcessor.process_pdf_page_as_image(mock_image)
                
    #             assert result == mock_extracted_text
    #             mock_image.save.assert_called_once_with(Config.TEMP_IMAGE_PATH, "JPEG")
    #             mock_file.assert_called_once_with(Config.TEMP_IMAGE_PATH, 'rb')

    def test_config_get_poppler_path(self):
        with patch('os.name', 'nt'):
            assert Config.get_poppler_path() == Config.POPPLER_PATH_WINDOWS
        
        with patch('os.name', 'posix'):
            assert Config.get_poppler_path() == Config.POPPLER_PATH_LINUX

if __name__ == "__main__":
    unittest.main()
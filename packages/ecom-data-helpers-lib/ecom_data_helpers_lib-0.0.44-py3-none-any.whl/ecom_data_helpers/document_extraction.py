import logging
from typing import Optional, Tuple, Dict, Any
from io import BytesIO
import os

import boto3
import httpx
from PyPDF2 import PdfReader
import docx
from pdf2image import convert_from_bytes
from PIL import Image

from .exceptions import (
    PdfImageExtractionExeception,
    DocumentDownloadError,
    TextExtractionError
)
from .utils import timeit

# Configure logging
logger = logging.getLogger(__name__)

# Configuration
class Config:
    POPPLER_PATH_WINDOWS = r"T:\libs\poppler\Library\bin"
    POPPLER_PATH_LINUX = "/opt/bin/"
    MIN_TEXT_LENGTH = 100
    TEMP_IMAGE_PATH = "/tmp/page.jpg"
    
    @classmethod
    def get_poppler_path(cls) -> str:
        return cls.POPPLER_PATH_WINDOWS if os.name == 'nt' else cls.POPPLER_PATH_LINUX

# Initialize AWS clients
textract_client = boto3.client('textract',region_name='us-east-1')

class DocumentProcessor:
    @staticmethod
    def extract_text_from_image(image: bytes) -> str:
        """Extract text from image using AWS Textract"""
        try:
            logger.info("Processing image with AWS Textract")
            response = textract_client.detect_document_text(
                Document={'Bytes': image}
            )
            return ''.join([
                item['Text'] 
                for item in response['Blocks'] 
                if item['BlockType'] == 'LINE'
            ])
        except Exception as e:
            logger.error(f"Textract processing failed: {str(e)}")
            raise TextExtractionError(f"Failed to extract text from image: {str(e)}")

    @staticmethod
    def process_pdf_page_as_image(image: Image) -> str:
        """Process a single PDF page as image"""
        try:
            image.save(Config.TEMP_IMAGE_PATH, "JPEG")
            with open(Config.TEMP_IMAGE_PATH, 'rb') as f:
                return DocumentProcessor.extract_text_from_image(f.read())
        finally:
            if os.path.exists(Config.TEMP_IMAGE_PATH):
                os.remove(Config.TEMP_IMAGE_PATH)

    @staticmethod
    def check_file_type(file_bytes: bytes) -> str:
        """Determine file type from bytes"""
        if file_bytes.startswith(b'%PDF-'):
            return "pdf"
        if file_bytes.startswith(b'PK\x03\x04'):
            return "docx"
        return "unknown"

@timeit
def extract_pdf_to_text(doc_bytes: bytes, force_image_conversion: bool = False) -> Tuple[str, str]:
    """Extract text from PDF document"""
    text = ''
    conversion_process = "raw_pdf"

    try:
        # Try direct text extraction first
        if not force_image_conversion:
            pdf_stream = BytesIO(doc_bytes)
            reader = PdfReader(pdf_stream)
            text = ' '.join(
                page.extract_text() 
                for page in reader.pages
            )

        if force_image_conversion or len(text) < Config.MIN_TEXT_LENGTH:
            conversion_process = "pdf_to_image"
            text = ''
            
            images = convert_from_bytes(
                doc_bytes,
                fmt="jpeg",
                poppler_path=Config.get_poppler_path()
            )
            
            logger.info(f"Converting {len(images)} PDF pages to images")
            
            for img in images:
                text += DocumentProcessor.process_pdf_page_as_image(img)

        return text, conversion_process

    except Exception as e:
        logger.error(f"PDF extraction failed: {str(e)}")
        raise TextExtractionError(f"Failed to extract text from PDF: {str(e)}")

@timeit
def extract_docx_to_text(doc_bytes: bytes) -> str:
    """Extract text from DOCX document"""
    try:
        doc = docx.Document(BytesIO(doc_bytes))
        return '\n'.join(
            para.text for para in doc.paragraphs if para.text.strip()
        )
    except Exception as e:
        logger.error(f"DOCX extraction failed: {str(e)}")
        raise TextExtractionError(f"Failed to extract text from DOCX: {str(e)}")

@timeit
def doc_url_to_bytes(url: str) -> bytes:
    """Download document from URL"""
    try:
        response = httpx.get(url, verify=False)
        response.raise_for_status()
        return response.content
    except httpx.HTTPError as e:
        logger.error(f"Failed to download document: {str(e)}")
        raise DocumentDownloadError(f"Failed to download document from {url}: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error downloading document: {str(e)}")
        raise DocumentDownloadError(f"Unexpected error downloading document from {url}: {str(e)}")

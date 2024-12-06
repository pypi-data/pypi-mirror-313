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
import pandas as pd

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
    def analyze_image_document(image: bytes) -> Dict[str, Any]:
        return textract_client.analyze_document(Document={'Bytes': image}, FeatureTypes=["FORMS", 'TABLES'])

    @staticmethod
    def analyze_pdf_document(image: bytes) -> Dict[str, Any]:
        image.save(Config.TEMP_IMAGE_PATH, "JPEG")
        with open(Config.TEMP_IMAGE_PATH, 'rb') as f:
            return textract_client.analyze_document(Document={'Bytes': f.read()}, FeatureTypes=["FORMS", 'TABLES'])

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

    @staticmethod
    def format_invoice_text(data: dict) -> str:

        def map_blocks(blocks, block_type):
            return {
                block['Id']: block
                for block in blocks
                if block['BlockType'] == block_type
            }

        def get_children_ids(block):
            for rels in block.get('Relationships', []):
                if rels['Type'] == 'CHILD':
                    yield from rels['Ids']

        blocks = data['Blocks']
        tables = map_blocks(blocks, 'TABLE')
        cells = map_blocks(blocks, 'CELL')
        words = map_blocks(blocks, 'WORD')
        selections = map_blocks(blocks, 'SELECTION_ELEMENT')

        # Getting all text
        raw_extracted_text = ''
        for item in blocks:
            if item['BlockType'] == 'LINE':
                raw_extracted_text += item['Text'] + '\n'

        # All tables
        dataframes = []

        # - ------------------------------------- Treating table data
        for i, table in enumerate(tables.values()):

            # Determine all the cells that belong to this table
            table_cells = [cells[cell_id] for cell_id in get_children_ids(table)]

            # Determine the table's number of rows and columns
            n_rows = max(cell['RowIndex'] for cell in table_cells)
            n_cols = max(cell['ColumnIndex'] for cell in table_cells)
            content = [[None for _ in range(n_cols)] for _ in range(n_rows)]

            # Fill in each cell
            for cell in table_cells:
                cell_contents = [
                    words[child_id]['Text']
                    if child_id in words
                    else selections[child_id]['SelectionStatus']
                    for child_id in get_children_ids(cell)
                ]
                i = cell['RowIndex'] - 1
                j = cell['ColumnIndex'] - 1
                content[i][j] = ' '.join(cell_contents)

            # We assume that the first row corresponds to the column names
            dataframe = pd.DataFrame(content[1:], columns=content[0])
            dataframe.columns = dataframe.columns.str.lower()

            dataframes.append(dataframe)

            raw_extracted_text += '\n' + f"Tabela {i}"
            raw_extracted_text += dataframe.to_string()

        return raw_extracted_text

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
def analyze_pdf_invoice(doc_bytes: bytes) -> str:
    """
    Extract text from PDF document

    Args:
        doc_bytes (bytes): The bytes of the PDF document to extract text from.

    Returns:
        str: The extracted text from the PDF document.
    """
    try:

        final_analysis : dict = {}

        images = convert_from_bytes(
            doc_bytes,
            fmt="jpeg",
            poppler_path=Config.get_poppler_path()
        )
            
        logger.info(f"Converting {len(images)} PDF pages to images")
        
        for img in images:

            # print(img.size)

            analysis : dict = DocumentProcessor.analyze_pdf_document(img)
            # formatted_text = DocumentProcessor.format_invoice_text(text)

            final_analysis = analysis

            break

        return final_analysis

    except Exception as e:
        logger.error(f"Invoice extraction failed: {str(e)}")
        raise TextExtractionError(f"Failed to extract text from invoice: {str(e)}")

@timeit
def analyze_image_invoice(doc_bytes: bytes) -> str:
    """
    Extract text from Image document

    Args:
        doc_bytes (bytes): The bytes of the Image document to extract text from.

    Returns:
        str: The extracted text from the Image document. 
    """
    try:
        # analysis : dict = DocumentProcessor.analyze_image_document(doc_bytes)
        return DocumentProcessor.analyze_image_document(doc_bytes)
    except Exception as e:
        logger.error(f"Invoice extraction failed: {str(e)}")
        raise TextExtractionError(f"Failed to extract text from invoice: {str(e)}")

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

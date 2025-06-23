import os
import io
import zipfile
import traceback
import logging
from typing import Union, List, BinaryIO, Tuple

import docx
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from importlib.metadata import PackageNotFoundError

# MODIFIED: Corrected the logger import and initialization
logger = logging.getLogger(__name__)

def handle_parsing_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PdfReadError as e:
            filename = kwargs.get('filename', args[1] if len(args) > 1 else "Unknown")
            error_msg = f"File {filename}: Kesalahan parsing PDF - {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return "", error_msg
        except PackageNotFoundError as e:
            filename = kwargs.get('filename', args[1] if len(args) > 1 else "Unknown")
            error_msg = f"File {filename}: File DOCX tidak valid - {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return "", error_msg
        except Exception as e:
            filename = kwargs.get('filename', args[1] if len(args) > 1 else "Unknown")
            error_msg = f"File {filename}: Gagal diproses - {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return "", error_msg
    return wrapper

@handle_parsing_errors
def parse_resume(file: Union[BinaryIO, str], filename: str = "") -> Tuple[str, str]:
    if isinstance(file, str):
        # If a path is provided, open the file and recall the function
        with open(file, 'rb') as f:
            # We pass the original filename, not the full path
            return parse_resume(f, os.path.basename(file))
    
    # MODIFIED: Logic changed to check file extension instead of file.type
    # This makes it compatible with both Streamlit's UploadedFile and standard file objects.
    file_extension = os.path.splitext(filename)[1].lower()
    
    # Read the file content into bytes
    file_bytes = file.read()

    if file_extension == ".pdf":
        reader = PdfReader(io.BytesIO(file_bytes))
        text = "\n".join([page.extract_text() for page in reader.pages])
        if not text.strip():
            error_msg = f"File {filename}: PDF tidak mengandung teks (mungkin hasil scan)"
            logger.warning(error_msg)
            return "", error_msg
        return text, ""
    elif file_extension == ".docx":
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        if not text.strip():
            error_msg = f"File {filename}: DOCX kosong atau tidak mengandung teks"
            logger.warning(error_msg)
            return "", error_msg
        return text, ""
    
    # If no valid extension is found
    return "", f"File {filename}: Format tidak didukung (harus PDF/DOCX)"

def parse_uploaded_folder(uploaded_folder) -> Tuple[List[str], List[str], List[str]]:
    """Parse semua file resume dari folder yang diupload (zip)"""
    resume_texts = []
    filenames = []
    error_messages = []
    
    with zipfile.ZipFile(io.BytesIO(uploaded_folder.read()), 'r') as zip_ref:
        temp_dir = "temp_uploaded_folder"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        zip_ref.extractall(temp_dir)
        
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.lower().endswith(('.pdf', '.docx')):
                    text, error = parse_resume(file_path, file)
                    if text:
                        resume_texts.append(text)
                        filenames.append(file)
                    if error:
                        error_messages.append(error)
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
    
    return resume_texts, filenames, error_messages
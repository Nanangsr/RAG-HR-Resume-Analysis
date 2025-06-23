# backend/utils/jd_parser.py (FIXED)
from .resume_parser import parse_resume
from typing import Tuple

def parse_jd(file) -> Tuple[str, str]:
    """Ekstrak teks dari file deskripsi pekerjaan (job description)"""
    # MODIFIED: Changed file.name to file.filename to match Flask/Werkzeug's FileStorage object
    filename = getattr(file, 'filename', "JD File")
    return parse_resume(file, filename)
"""LifecycleDesk AI - modular loader

This file keeps the LifecycleDesk AI product behavior intact while the application is split into smaller editable chunks. Each chunk is executed in
order so existing global Streamlit functions continue to work.
"""
from pathlib import Path

CHUNK_DIR = Path(__file__).parent / "decisiondesk_chunks"
CHUNKS = [
    "01_bootstrap_detection.py",
    "02_employee_receptionist.py",
    "03_storage_client_delivery.py",
    "04_proposal_ui.py",
    "05_design_system.py",
    "06_streamlit_runtime.py",
]

for chunk in CHUNKS:
    chunk_path = CHUNK_DIR / chunk
    code = chunk_path.read_text(encoding="utf-8")
    exec(compile(code, str(chunk_path), "exec"), globals())

"""
Document processing and text extraction module
"""
import PyPDF2
from pathlib import Path
from typing import List, Tuple, Dict
from logger import get_logger


class DocumentProcessor:
    """Handles document extraction and chunking for FAISS indexing"""

    def __init__(self, docs_dir: str = None):
        from logger.config_manager import ConfigManager
        config = ConfigManager()

        # Load configuration paths and parameters
        self.docs_dir = Path(docs_dir or config.get("paths.documents", "data/documents"))
        self.chunk_size = int(config.get("chunking.chunk_size", 500))
        self.chunk_overlap = int(config.get("chunking.chunk_overlap", 50))
        self.logger = get_logger(__name__)

        # Ensure the documents directory exists
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"DocumentProcessor initialized with directory: {self.docs_dir}")

    # ----------------------------------------------------------------------
    # TEXT EXTRACTION
    # ----------------------------------------------------------------------

    def extract_from_pdf(self, pdf_path: Path) -> List[Dict]:
        """Extract text content from a PDF file"""
        chunks = []
        try:
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                self.logger.info(f"Extracting text from {pdf_path.name} ({num_pages} pages)...")

                for i, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    if text.strip():
                        chunks.append({
                            "text": text.strip(),
                            "page": i + 1
                        })

            self.logger.info(f"✅ Extracted {len(chunks)} pages from {pdf_path.name}")
        except Exception as e:
            self.logger.error(f"❌ Error reading {pdf_path}: {e}")
        return chunks

    def extract_from_txt(self, txt_path: Path) -> List[Dict]:
        """Extract text content from a TXT file"""
        try:
            with open(txt_path, "r", encoding="utf-8") as file:
                text = file.read()
                if text.strip():
                    self.logger.info(f"✅ Extracted text from {txt_path.name}")
                    return [{"text": text.strip(), "page": 1}]
                else:
                    self.logger.warning(f"⚠️ Empty file: {txt_path.name}")
                    return []
        except Exception as e:
            self.logger.error(f"❌ Error reading {txt_path}: {e}")
            return []

    # ----------------------------------------------------------------------
    # CHUNKING
    # ----------------------------------------------------------------------

    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks (word-based)"""
        words = text.split()
        chunks = []

        step = max(1, self.chunk_size - self.chunk_overlap)
        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + self.chunk_size])
            if chunk:
                chunks.append(chunk)

        return chunks

    # ----------------------------------------------------------------------
    # PROCESS ALL DOCUMENTS
    # ----------------------------------------------------------------------

    def process_all_documents(self) -> Tuple[List[str], List[Dict]]:
        """
        Extract and chunk all PDF and TXT documents from the configured directory.
        Returns:
            Tuple[List[str], List[Dict]]: A list of text chunks and corresponding metadata.
        """
        if not self.docs_dir.exists():
            self.logger.error(f"❌ Documents directory not found: {self.docs_dir}")
            return [], []

        all_chunks = []
        metadata = []

        # Collect all supported files
        files = list(self.docs_dir.glob("*.pdf")) + list(self.docs_dir.glob("*.txt"))

        if not files:
            self.logger.warning(f"⚠️ No documents found in {self.docs_dir}")
            return [], []

        self.logger.info(f"📂 Found {len(files)} document(s) to process...")

        for file_path in files:
            self.logger.info(f"📄 Processing: {file_path.name}")

            if file_path.suffix.lower() == ".pdf":
                pages = self.extract_from_pdf(file_path)
            else:
                pages = self.extract_from_txt(file_path)

            for page_data in pages:
                chunks = self.chunk_text(page_data["text"])

                for idx, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    metadata.append({
                        "document": file_path.name,
                        "page": page_data["page"],
                        "chunk_id": idx,
                        "text": chunk
                    })

        self.logger.info(f"✅ Created {len(all_chunks)} chunks from {len(files)} document(s)")
        return all_chunks, metadata

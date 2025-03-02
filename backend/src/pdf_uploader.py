from pathlib import Path
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_core.documents import Document
from backend.src.utils.log import get_logger, timed

_logger = get_logger(__name__)


class PDFUploader:
    def __init__(self, filepath: Path, chunk_size: int, chunk_overlap: int):
        self.filepath = filepath
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @timed
    def pdf_loader(self) -> List[Document]:
        _logger.info(f"Loading and chunking PDF: {self.filepath}")

        try:
            loader = UnstructuredPDFLoader(self.filepath.as_posix())
            _logger.info(f"Loading PDF from {self.filepath}")
            data = loader.load()
            _logger.info(f"Loaded PDF from {self.filepath}")
        except Exception as e:
            _logger.error(f"Error loading PDF: {e}")
            raise

        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        _logger.info(f"Splitting document into chunks with size {self.chunk_size} and overlap {self.chunk_overlap}")
        chunks = splitter.split_documents(data)
        _logger.info(f"Generated {len(chunks)} chunks from the document.")

        return chunks

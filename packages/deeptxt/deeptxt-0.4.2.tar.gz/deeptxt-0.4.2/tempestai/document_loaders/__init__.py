from tempestai.document_loaders.directory import DirectoryLoader
from tempestai.document_loaders.docx import DocxLoader
from tempestai.document_loaders.html import HTMLLoader
from tempestai.document_loaders.json import JSONLoader
from tempestai.document_loaders.pdf import PDFLoader
from tempestai.document_loaders.s3 import S3Loader
from tempestai.document_loaders.watson_discovery import  WatsonDiscoveryLoader

__all__ = [
    "DirectoryLoader",
    "DocxLoader",
    "HTMLLoader",
    "JSONLoader",
    "PDFLoader",
    "S3Loader",
    "WatsonDiscoveryLoader",
]

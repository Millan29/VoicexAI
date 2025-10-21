"""
Inter-agent message schemas for EPPN

Defines Pydantic models for messages exchanged between agents.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class CrawlRequest(BaseModel):
    urls: List[str]
    interpreter_address: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class PDFReady(BaseModel):
    url: str
    source: str
    metadata: Dict[str, Any]


class ParsedText(BaseModel):
    doc_id: str
    sections: List[Dict[str, Any]]
    entities: List[Dict[str, Any]]
    metadata: Dict[str, Any]


class SummaryReady(BaseModel):
    doc_id: str
    summary: str
    key_points: List[str]
    metadata: Dict[str, Any]


class EthicsReport(BaseModel):
    doc_id: str
    report: Dict[str, Any]
    risks: List[str]
    recommendations: List[str]
    metadata: Dict[str, Any]



""" Data models for one record. """
from dataclasses import dataclass
from typing import Optional

@dataclass
class RecordInfo:
    """ Class for record information. """
    desc: Optional[str] = None
    category: Optional[str] = None
    start_timestamp: Optional[str] = None
    end_timestamp: Optional[str] = None
    task_duration: Optional[str] = None

@dataclass
class RecordForView:
    """ Record information from json for analytic view. """
    date: Optional[str] = None
    desc: Optional[str] = None
    category: Optional[str] = None
    start_timestamp: Optional[str] = None
    end_timestamp: Optional[str] = None
    task_duration: Optional[str] = None

"""Supabase storage utilities."""

from earthquakes_parser.storage.supabase.database import SupabaseDB
from earthquakes_parser.storage.supabase.file_storage import SupabaseFileStorage

__all__ = ["SupabaseDB", "SupabaseFileStorage"]

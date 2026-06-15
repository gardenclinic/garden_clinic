"""Database utility functions for Garden Clinic."""
import streamlit as st
from typing import List, Dict, Any, Optional
from supabase import create_client
import logging

logger = logging.getLogger(__name__)


@st.cache_resource
def get_sb():
    """Get cached Supabase client."""
    try:
        return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    except KeyError as e:
        logger.error(f"Missing Supabase credentials: {e}")
        raise


def sb_all(
    table: str,
    filters: Optional[Dict[str, Any]] = None,
    order: Optional[str] = None,
    desc_order: bool = False,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Fetch all records from a table with optional filters and ordering."""
    try:
        q = get_sb().table(table).select("*")
        if filters:
            for k, v in filters.items():
                q = q.eq(k, v)
        if order:
            q = q.order(order, desc=desc_order)
        if limit:
            q = q.limit(limit)
        return q.execute().data or []
    except Exception as e:
        logger.error(f"Error fetching from {table}: {e}")
        return []


def sb_one(table: str, filters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Fetch a single record."""
    try:
        results = sb_all(table, filters=filters)
        return results[0] if results else None
    except Exception as e:
        logger.error(f"Error fetching one from {table}: {e}")
        return None


def sb_insert(table: str, data: Dict[str, Any]) -> bool:
    """Insert a single record."""
    try:
        get_sb().table(table).insert(data).execute()
        return True
    except Exception as e:
        logger.error(f"Error inserting into {table}: {e}")
        return False


def sb_delete(table: str, col: str, val: Any) -> bool:
    """Delete records matching a condition."""
    try:
        get_sb().table(table).delete().eq(col, val).execute()
        return True
    except Exception as e:
        logger.error(f"Error deleting from {table}: {e}")
        return False


def sb_update(table: str, data: Dict[str, Any], col: str, val: Any) -> bool:
    """Update records matching a condition."""
    try:
        get_sb().table(table).update(data).eq(col, val).execute()
        return True
    except Exception as e:
        logger.error(f"Error updating {table}: {e}")
        return False


def sb_exists(table: str, col: str, val: Any) -> bool:
    """Check if a record exists."""
    try:
        result = get_sb().table(table).select("id").eq(col, val).execute()
        return len(result.data) > 0
    except Exception as e:
        logger.error(f"Error checking existence in {table}: {e}")
        return False


def sb_sum(table: str, col: str, filters: Optional[Dict[str, Any]] = None) -> float:
    """Sum a column, optionally with filters."""
    try:
        rows = sb_all(table, filters=filters)
        return sum(float(r.get(col) or 0) for r in rows)
    except Exception as e:
        logger.error(f"Error summing {col} from {table}: {e}")
        return 0.0


def sb_count(table: str, filters: Optional[Dict[str, Any]] = None) -> int:
    """Count records."""
    try:
        return len(sb_all(table, filters=filters))
    except Exception as e:
        logger.error(f"Error counting {table}: {e}")
        return 0

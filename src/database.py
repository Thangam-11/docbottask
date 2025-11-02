"""
Database operations for logging and storage
"""
import sqlite3
import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from logger import get_logger


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON Encoder to handle NumPy data types"""
    def default(self, obj):
        if isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        return super(NumpyEncoder, self).default(obj)


class Database:
    """Database handler for DocIntel Bot"""

    def __init__(self, db_path: str = None):
        from logger.config_manager import ConfigManager
        config = ConfigManager()

        self.db_path = db_path or config.get('paths.database', 'data/docintel.db')
        self.logger = get_logger(__name__)

        # Create data directory
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        self.setup_tables()
        self.logger.info(f"Database initialized at: {self.db_path}")

    # ---------------------------------------------------------
    # Setup Tables
    # ---------------------------------------------------------
    def setup_tables(self) -> None:
        """Create database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Chat logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                question TEXT NOT NULL,
                retrieved_chunks TEXT,
                answer TEXT NOT NULL,
                citations TEXT,
                execution_time REAL
            )
        """)

        # Test queries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                expected_topic TEXT,
                answer TEXT NOT NULL,
                citations TEXT,
                timestamp TEXT NOT NULL,
                success BOOLEAN DEFAULT 1
            )
        """)

        # System metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                metadata TEXT
            )
        """)

        conn.commit()
        conn.close()
        self.logger.debug("Database tables created/verified")

    # ---------------------------------------------------------
    # Log Chat Interactions
    # ---------------------------------------------------------
    def log_interaction(self, question: str, chunks: List[Dict],
                       answer: str, citations: List[Dict],
                       execution_time: float = 0.0) -> int:
        """Log a chat interaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO chat_logs 
            (timestamp, question, retrieved_chunks, answer, citations, execution_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            question,
            json.dumps(chunks, cls=NumpyEncoder),   # ✅ FIX APPLIED
            answer,
            json.dumps(citations, cls=NumpyEncoder), # ✅ FIX APPLIED
            execution_time
        ))

        log_id = cursor.lastrowid
        conn.commit()
        conn.close()

        self.logger.debug(f"Logged interaction with ID: {log_id}")
        return log_id

    # ---------------------------------------------------------
    # Log Test Queries
    # ---------------------------------------------------------
    def log_test_query(self, query: str, expected_topic: str,
                      answer: str, citations: List[Dict],
                      success: bool = True) -> int:
        """Log a test query result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO test_queries 
            (query, expected_topic, answer, citations, timestamp, success)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            query,
            expected_topic,
            answer,
            json.dumps(citations, cls=NumpyEncoder),  # ✅ FIX APPLIED
            datetime.now().isoformat(),
            1 if success else 0
        ))

        test_id = cursor.lastrowid
        conn.commit()
        conn.close()

        self.logger.debug(f"Logged test query with ID: {test_id}")
        return test_id

    # ---------------------------------------------------------
    # Log System Metrics
    # ---------------------------------------------------------
    def log_metric(self, metric_name: str, metric_value: float,
                   metadata: Dict = None) -> int:
        """Log a system metric"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO system_metrics (timestamp, metric_name, metric_value, metadata)
            VALUES (?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            metric_name,
            metric_value,
            json.dumps(metadata, cls=NumpyEncoder) if metadata else None  # ✅ FIX APPLIED
        ))

        metric_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return metric_id

    # ---------------------------------------------------------
    # Retrieval Methods
    # ---------------------------------------------------------
    def get_chat_logs(self, limit: int = 10) -> List[Tuple]:
        """Retrieve recent chat logs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT timestamp, question, answer, citations, execution_time
            FROM chat_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))

        results = cursor.fetchall()
        conn.close()

        return results

    def get_test_results(self) -> List[Tuple]:
        """Retrieve all test query results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, query, expected_topic, answer, citations, timestamp, success
            FROM test_queries 
            ORDER BY id
        """)

        results = cursor.fetchall()
        conn.close()

        return results

    def get_metrics(self, metric_name: str = None, limit: int = 100) -> List[Tuple]:
        """Retrieve system metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if metric_name:
            cursor.execute("""
                SELECT timestamp, metric_name, metric_value, metadata
                FROM system_metrics 
                WHERE metric_name = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (metric_name, limit))
        else:
            cursor.execute("""
                SELECT timestamp, metric_name, metric_value, metadata
                FROM system_metrics 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))

        results = cursor.fetchall()
        conn.close()

        return results

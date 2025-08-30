"""
Database models for the enhanced chatbot application.
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "chatbot.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_ip TEXT,
                    user_agent TEXT,
                    conversation_context TEXT
                )
            """)
            
            # Contacts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT,
                    company TEXT,
                    position TEXT,
                    notes TEXT,
                    interest_level INTEGER DEFAULT 5,
                    source TEXT DEFAULT 'chatbot',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_contacted DATETIME,
                    status TEXT DEFAULT 'new'
                )
            """)
            
            # Analytics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    event_data TEXT,
                    session_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_ip TEXT,
                    user_agent TEXT
                )
            """)
            
            # Unknown questions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unknown_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    first_asked DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_asked DATETIME DEFAULT CURRENT_TIMESTAMP,
                    resolved BOOLEAN DEFAULT FALSE,
                    response_added TEXT
                )
            """)
            
            # Documents metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    content_summary TEXT,
                    keywords TEXT,
                    last_modified DATETIME,
                    processed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            conn.commit()
    
    def log_conversation(self, session_id: str, user_message: str, bot_response: str,
                        user_ip: str = None, user_agent: str = None, context: Dict = None):
        """Log a conversation exchange."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversations 
                (session_id, user_message, bot_response, user_ip, user_agent, conversation_context)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session_id, user_message, bot_response, user_ip, user_agent, 
                  json.dumps(context) if context else None))
            conn.commit()
    
    def add_contact(self, email: str, name: str = None, phone: str = None,
                   company: str = None, position: str = None, notes: str = None,
                   interest_level: int = 5) -> bool:
        """Add or update a contact."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO contacts 
                    (name, email, phone, company, position, notes, interest_level, last_contacted)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, email, phone, company, position, notes, interest_level, datetime.now()))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding contact: {e}")
            return False
    
    def log_analytics_event(self, event_type: str, event_data: Dict = None,
                           session_id: str = None, user_ip: str = None, user_agent: str = None):
        """Log an analytics event."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analytics 
                (event_type, event_data, session_id, user_ip, user_agent)
                VALUES (?, ?, ?, ?, ?)
            """, (event_type, json.dumps(event_data) if event_data else None,
                  session_id, user_ip, user_agent))
            conn.commit()
    
    def add_unknown_question(self, question: str):
        """Add or update an unknown question."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Check if question already exists
            cursor.execute("SELECT id, frequency FROM unknown_questions WHERE question = ?", (question,))
            result = cursor.fetchone()
            
            if result:
                # Update frequency and last_asked
                cursor.execute("""
                    UPDATE unknown_questions 
                    SET frequency = frequency + 1, last_asked = ?
                    WHERE id = ?
                """, (datetime.now(), result[0]))
            else:
                # Insert new question
                cursor.execute("""
                    INSERT INTO unknown_questions (question)
                    VALUES (?)
                """, (question,))
            
            conn.commit()
    
    def get_analytics_summary(self, days: int = 7) -> Dict:
        """Get analytics summary for the last N days."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total conversations
            cursor.execute("""
                SELECT COUNT(*) FROM conversations 
                WHERE timestamp >= datetime('now', '-{} days')
            """.format(days))
            total_conversations = cursor.fetchone()[0]
            
            # Unique sessions
            cursor.execute("""
                SELECT COUNT(DISTINCT session_id) FROM conversations 
                WHERE timestamp >= datetime('now', '-{} days')
            """.format(days))
            unique_visitors = cursor.fetchone()[0]
            
            # New contacts
            cursor.execute("""
                SELECT COUNT(*) FROM contacts 
                WHERE created_at >= datetime('now', '-{} days')
            """.format(days))
            new_contacts = cursor.fetchone()[0]
            
            # Most common questions (top 5)
            cursor.execute("""
                SELECT question, frequency FROM unknown_questions 
                ORDER BY frequency DESC, last_asked DESC 
                LIMIT 5
            """)
            common_questions = cursor.fetchall()
            
            return {
                'total_conversations': total_conversations,
                'unique_visitors': unique_visitors,
                'new_contacts': new_contacts,
                'common_unknown_questions': common_questions,
                'period_days': days
            }
    
    def get_recent_contacts(self, limit: int = 10) -> List[Dict]:
        """Get recent contacts."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, email, company, position, interest_level, created_at
                FROM contacts 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            columns = ['name', 'email', 'company', 'position', 'interest_level', 'created_at']
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def add_document_metadata(self, filename: str, file_path: str, file_type: str,
                             content_summary: str = None, keywords: List[str] = None):
        """Add document metadata."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO documents 
                (filename, file_path, file_type, content_summary, keywords, last_modified)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (filename, file_path, file_type, content_summary, 
                  json.dumps(keywords) if keywords else None, 
                  datetime.fromtimestamp(Path(file_path).stat().st_mtime)))
            conn.commit()
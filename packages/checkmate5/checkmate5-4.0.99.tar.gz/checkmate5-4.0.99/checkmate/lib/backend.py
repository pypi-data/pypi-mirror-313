from blitzdb import FileBackend as BlitzDBFileBackend
from blitzdb.backends.sql import Backend as BlitzDBSQLBackend
from typing import Any, Optional, Dict
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class FileBackend(BlitzDBFileBackend):
    def __init__(self, path: str) -> None:
        """Initialize FileBackend with specified path.
        
        Args:
            path: Path to store the database files
            
        Raises:
            ValueError: If path is invalid
        """
        logger.debug(f"Initializing FileBackend with path: {path}")
        super().__init__(path)
        self.path = path

    def test_connection(self) -> bool:
        """Test the file access.
        
        Returns:
            bool: True if file access is successful
            
        Raises:
            ConnectionError: If file access test fails
        """
        try:
            self.begin()
            self.commit()
            logger.info("File access test successful")
            return True
        except Exception as e:
            logger.error(f"File access test failed: {str(e)}")
            raise ConnectionError(f"File access test failed: {str(e)}")

    @contextmanager
    def session(self):
        """Context manager for file operations.
        
        Yields:
            FileBackend: Self with active session
        """
        try:
            self.begin()
            yield self
            self.commit()
        except Exception as e:
            logger.error(f"Session error: {str(e)}")
            self.rollback()
            raise

class SQLBackend(BlitzDBSQLBackend):
    def __init__(self, connection: Any) -> None:
        """Initialize SQL Backend with database connection.
        
        Args:
            connection: SQLAlchemy engine or connection object
            
        Raises:
            ConnectionError: If database connection fails
        """
        logger.debug(f"Initializing SQL Backend with connection: {connection}")
        super().__init__(connection)
        self.connection = connection

    def test_connection(self) -> bool:
        """Test the database connection.
        
        Returns:
            bool: True if connection is successful
            
        Raises:
            ConnectionError: If connection test fails
        """
        try:
            with self.connection.connect() as conn:
                conn.execute('SELECT 1')
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            raise ConnectionError(f"Database connection test failed: {str(e)}")

    @contextmanager
    def session(self):
        """Context manager for database sessions.
        
        Yields:
            SQLBackend: Self with active session
        """
        try:
            self.begin()
            yield self
            self.commit()
        except Exception as e:
            logger.error(f"Session error: {str(e)}")
            self.rollback()
            raise
        finally:
            if hasattr(self.connection, 'dispose'):
                self.connection.dispose()

    def close(self) -> None:
        """Clean up database connections."""
        try:
            if hasattr(self.connection, 'dispose'):
                self.connection.dispose()
            logger.info("Closed SQL Backend connection")
        except Exception as e:
            logger.error(f"Error closing backend: {str(e)}")
            raise

# For backward compatibility
Backend = SQLBackend  # Default to SQLBackend for existing code

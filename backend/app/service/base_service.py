from sqlalchemy.orm import Session

class BaseService:
    """Base service class that provides common database initialization"""

    def __init__(self, db: Session):
        self.db = db

from typing import Any, Optional, Tuple
from sqlalchemy.exc import SQLAlchemyError
from ..repositories.managers import ReportManager
from .base import BaseController


class ReportController(BaseController):
    manager = ReportManager


    @classmethod
    def get_most_requested_ingredient(cls) -> Tuple[Any, Optional[str]]:
        try:
            return cls.manager.get_most_requested_ingredient(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)


    @classmethod
    def get_most_revenue_month(cls) -> Tuple[Any, Optional[str]]:
        try:
            return cls.manager.get_most_revenue_month(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
        
        
    @classmethod
    def get_best_customers(cls) -> Tuple[Any, Optional[str]]:
        try:
            return cls.manager.get_best_customers(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)


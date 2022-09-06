from app.common.http_methods import GET
from flask import Blueprint

from .base_service import BaseService
from ..controllers.controller_factory import ControllerFactory


report = Blueprint('report', __name__)
base_service = BaseService()
controller = ControllerFactory.get_controller('report')


@report.route('/most-requested', methods=GET)
def most_requested_ingredient():
    return base_service.get_most_requested_ingredient(controller)


@report.route('/most-revenue-month', methods=GET)
def most_revenue_month():
    return base_service.get_most_revenue_month(controller)


@report.route('/best-customers', methods=GET)
def best_customers():
    return base_service.get_best_customers(controller)

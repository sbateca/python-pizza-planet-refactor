from app.common.http_methods import GET, POST, PUT
from flask import Blueprint

from .base_service import BaseService
from ..controllers.controller_factory import ControllerFactory


beverage = Blueprint('beverage', __name__)
base_service = BaseService()
controller = ControllerFactory.get_controller('beverage')


@beverage.route('/',methods=POST)
def create_beverage():
    return base_service.create(controller)


@beverage.route('/', methods=PUT)
def update_beverage():
    return base_service.update(controller)


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    return base_service.get_by_id(_id, controller)


@beverage.route('/', methods=GET)
def get_beverages():
    return base_service.get_all(controller)

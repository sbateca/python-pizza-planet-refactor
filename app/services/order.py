from app.common.http_methods import GET, POST
from flask import Blueprint, jsonify, request

from ..services.base_service import BaseService
from ..controllers.controller_factory import ControllerFactory


order = Blueprint('order', __name__)
base_service = BaseService()
controller = ControllerFactory.get_controller('order')


@order.route('/', methods=POST)
def create_order():
    return base_service.create(controller)


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    return base_service.get_by_id(_id, controller)


@order.route('/', methods=GET)
def get_orders():
    return base_service.get_all(controller)

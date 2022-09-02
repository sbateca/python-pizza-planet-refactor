from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from .base_service import BaseService
from ..controllers.controller_factory import ControllerFactory


size = Blueprint('size', __name__)
base_service = BaseService()
controller = ControllerFactory.get_controller('size')


@size.route('/', methods=POST)
def create_size():
    return base_service.create(controller)


@size.route('/', methods=PUT)
def update_size():
    return base_service.update(controller)


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    return base_service.get_by_id(_id, controller)


@size.route('/', methods=GET)
def get_all_sizes():
    return base_service.get_all(controller)

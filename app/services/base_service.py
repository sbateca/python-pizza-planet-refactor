from flask import jsonify, request


class BaseService:


    @classmethod
    def create(cls, controller):
        data, error = controller.create(request.json)
        response = data if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code


    @classmethod
    def update(cls, controller):
        data, error = controller.update(request.json)
        response = data if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code


    @classmethod
    def get_by_id(cls, _id: int, controller):
        data, error = controller.get_by_id(_id)
        response = data if not error else {'error': error}
        status_code = 200 if data else 404 if not error else 400
        return jsonify(response), status_code


    @classmethod
    def get_all(cls, controller):
        data, error = controller.get_all()
        response = data if not error else {'error': error}
        status_code = 200 if data else 404 if not error else 400
        return jsonify(response), status_code


    @classmethod
    def get_most_requested_ingredient(cls, controller):
        data, error = controller.get_most_requested_ingredient()
        response = data if not error else {'error': error}
        status_code = 200 if data else 404 if not error else 400
        return jsonify(response), status_code


    @classmethod
    def get_most_revenue_month(cls, controller):
        data, error = controller.get_most_revenue_month()
        response = data if not error else {'error': error}
        status_code = 200 if data else 404 if not error else 400
        return jsonify(response), status_code


    @classmethod
    def get_best_customers(cls, controller):
        data, error = controller.get_best_customers()
        response = data if not error else {'error': error}
        status_code = 200 if len(data) >= 0 else 404 if not error else 400
        return jsonify(response), status_code

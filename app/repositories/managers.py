from typing import Any, Dict, List, Optional, Sequence

from sqlalchemy.sql import text, column
from sqlalchemy import func, desc
from sqlalchemy.orm import aliased


from .models import Beverage, Ingredient, Order, OrderDetail, Size, db
from .serializers import (BeverageSerializer, IngredientSerializer, OrderSerializer,
                          SizeSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        for ingredient in ingredients:
            cls.session.add(OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price,
                                                 beverage_id = None, beverage_price = None))
        for beverage in beverages:
            cls.session.add(OrderDetail(order_id=new_order._id, ingredient_id=None, ingredient_price=None,
                                                 beverage_id = beverage._id, beverage_price = beverage.price))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()


class ReportManager(BaseManager):


    @classmethod
    def get_most_requested_ingredient(cls):
        inner_query = cls.session.query(func.count(Ingredient._id).label('number'), OrderDetail, Ingredient).\
                                filter(Ingredient._id is not None).\
                                filter(Ingredient._id == OrderDetail.ingredient_id).\
                                group_by(Ingredient._id).subquery()
        
        aliased_query = aliased(inner_query)
        row_list = [row for row in cls.session.query(func.max(aliased_query.c.number), aliased_query.c.name).all()]

        most_requested_ingredient: list = []
        for ingredient in row_list:
            row = {
                'requests': ingredient[0],
                'name': ingredient[1]
            }
            most_requested_ingredient.append(row)
        return most_requested_ingredient


    @classmethod
    def get_most_revenue_month(cls):
        result = cls.session.query(func.sum(Order.total_price).label('total'), func.strftime("%Y %m", Order.date).label('month')).\
                                                    group_by(func.strftime("%Y %m", Order.date)).\
                                                    order_by(desc('total')).first()
        if result is None:
            return {"total": None, "month": None}
        else:
            return {
                "total": result.total,
                "month": result.month
            }


    @classmethod
    def get_best_customers(cls):
        row_list = [row for row in cls.session.query(func.count(Order.client_name).label('number'), Order.client_name).\
                                                    group_by(Order.client_name).\
                                                    order_by(desc('number')).limit(3).offset(0).all()]
        
        best_customers: list = []
        for customer in row_list:
            row = {
                'orders': customer[0],
                'name': customer[1]
            }
            best_customers.append(row)
        return best_customers

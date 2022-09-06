import pytest

from app.controllers import ReportController


def test_get_most_requested_ingredient(app):
    most_requested, error = ReportController.get_most_requested_ingredient()
    assert(error is None)
    assert(type(most_requested) == list)


def test_get_most_revenue_month(app):
    most_revenue, error = ReportController.get_most_revenue_month()
    assert(error is None)
    assert(type(most_revenue) == dict)


def test_get_best_customers(app):
    best_customers, error = ReportController.get_best_customers()
    assert(error is None)
    assert(type(best_customers) == list)

import pytest


def test_get_most_requested_ingredient(client, report_uri):
    response = client.get(f'{report_uri}most-requested')
    pytest.assume(response.status.startswith('200'))


def test_get_most_revenue_month(client, report_uri):
    response = client.get(f'{report_uri}most-revenue-month')
    pytest.assume(response.status.startswith('200'))


def test_get_best_customers(client, report_uri):
    response = client.get(f'{report_uri}best-customers')
    if len(response.data) >= 0:
        pytest.assume(response.status.startswith('200'))
    else:
        pytest.assume(response.status.startswith('404'))

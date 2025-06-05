"""
import pytest
from graphene.test import Client
from sales.schema import schema  # Adjust import if needed
from sales.models import Products, Users, Customers, Orders
from unittest.mock import patch

@pytest.fixture
def setup_data(db):
    product = Products.objects.create(product_name="Test Product")
    customer = Customers.objects.create(customer_name="Test Customer")
    user = Users.objects.create(name="Test User")
    return product, customer, user

@pytest.fixture
def graphql_client():
    return Client(schema)

@pytest.mark.django_db
class TestOrderMutations:

    @patch('sales.utils.send_admin_mail.send_alert_email')
    def test_create_order(self, mock_send_email, graphql_client, setup_data):
        product, customer, user = setup_data

        mutation = '''
            mutation CreateOrder($productId: Int!, $customerId: Int!, $userId: Int!) {
                createOrder(productId: $productId, customerId: $customerId, userId: $userId) {
                    order {
                        orderId
                        productId
                        customerId
                        userId
                    }
                }
            }
        '''

        variables = {
            'productId': product.product_id,
            'customerId': customer.customer_id,
            'userId': user.user_id,
        }

        executed = graphql_client.execute(mutation, variables=variables)
        order_data = executed['data']['createOrder']['order']

        assert order_data['orderId'] is not None
        assert order_data['productId'] == product.product_id
        assert order_data['customerId'] == customer.customer_id
        assert order_data['userId'] == user.user_id
        mock_send_email.assert_called_once_with(customer.customer_name, product.product_name, user.name)

    def test_update_order(self, graphql_client, setup_data):
        product, customer, user = setup_data
        order = Orders.objects.create(product_id=product.product_id, customer_id=customer.customer_id, user_id=user.user_id)

        mutation = '''
            mutation UpdateOrder($orderId: Int!, $productId: Int, $customerId: Int) {
                updateOrder(orderId: $orderId, productId: $productId, customerId: $customerId) {
                    order {
                        orderId
                        productId
                        customerId
                    }
                }
            }
        '''

        new_product = Products.objects.create(product_name="New Product")

        variables = {
            'orderId': order.order_id,
            'productId': new_product.product_id,
            'customerId': customer.customer_id,
        }

        executed = graphql_client.execute(mutation, variables=variables)
        updated_order = executed['data']['updateOrder']['order']

        assert updated_order['orderId'] == order.order_id
        assert updated_order['productId'] == new_product.product_id
        assert updated_order['customerId'] == customer.customer_id

    def test_update_order_not_found(self, graphql_client):
        mutation = '''
            mutation UpdateOrder($orderId: Int!) {
                updateOrder(orderId: $orderId) {
                    order {
                        orderId
                    }
                }
            }
        '''
        variables = {'orderId': 9999}

        executed = graphql_client.execute(mutation, variables=variables)
        assert executed.get('errors') is not None
        assert 'Order not found' in executed['errors'][0]['message']

    def test_delete_order(self, graphql_client, setup_data):
        product, customer, user = setup_data
        order = Orders.objects.create(product_id=product.product_id, customer_id=customer.customer_id, user_id=user.user_id)

        mutation = '''
            mutation DeleteOrder($orderId: Int!) {
                deleteOrder(orderId: $orderId) {
                    ok
                }
            }
        '''
        variables = {'orderId': order.order_id}
        executed = graphql_client.execute(mutation, variables=variables)

        assert executed['data']['deleteOrder']['ok'] is True
        assert not Orders.objects.filter(order_id=order.order_id).exists()

    def test_delete_order_not_found(self, graphql_client):
        mutation = '''
            mutation DeleteOrder($orderId: Int!) {
                deleteOrder(orderId: $orderId) {
                    ok
                }
            }
        '''
        variables = {'orderId': 9999}

        executed = graphql_client.execute(mutation, variables=variables)
        assert executed.get('errors') is not None
        assert 'Order not found' in executed['errors'][0]['message']


"""
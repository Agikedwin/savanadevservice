import pytest
from django.utils import timezone
from sales.models import Users, Customers, ProductCategory, Products, Orders


@pytest.mark.django_db
class TestModels:

    @pytest.fixture
    def user(self):
        return Users.objects.create(
            name="John Doe",
            username="johndoe",
            password="securepassword",
            role=1,
            description="Admin user"
        )

    @pytest.fixture
    def customer(self, user):
        return Customers.objects.create(
            customer_name="Acme Corp",
            customer_contact="1234567890123",
            customer_email="acme@example.com",
            customer_type="Retail",
            user=user
        )

    @pytest.fixture
    def category(self, user):
        return ProductCategory.objects.create(
            category_name="Electronics",
            category_type="Consumer",
            description="All electronic items",
            user=user
        )

    @pytest.fixture
    def product(self, category, user):
        return Products.objects.create(
            product_name="Smartphone",
            category=category,
            user=user,
            price=599
        )

    @pytest.fixture
    def order(self, product, customer, user):
        return Orders.objects.create(
            product=product,
            customer=customer,
            user=user
        )

    # ----------- Function Return Tests (e.g. __str__) -----------

    def test_users_str_returns_name(self, user):
        assert user.__str__() == "John Doe"

    def test_customers_str_returns_id_as_str(self, customer):
        assert customer.__str__() == str(customer.customer_id)

    def test_category_str_returns_id_as_str(self, category):
        assert category.__str__() == str(category.category_id)

    def test_product_str_returns_id_as_str(self, product):
        assert product.__str__() == str(product.product_id)

    def test_orders_str_returns_id_as_str(self, order):
        assert order.__str__() == str(order.order_id)

    # ----------- Functional Field Tests -----------

    def test_users_fields(self, user):
        assert user.name == "John Doe"
        assert user.username == "johndoe"
        assert user.password == "securepassword"
        assert user.role == 1
        assert user.description == "Admin user"

    def test_customers_fields(self, customer):
        assert customer.customer_name == "Acme Corp"
        assert customer.customer_contact == "1234567890123"
        assert customer.customer_email == "acme@example.com"
        assert customer.customer_type == "Retail"
        assert isinstance(customer.date_created, timezone.datetime)

    def test_category_fields(self, category):
        assert category.category_name == "Electronics"
        assert category.category_type == "Consumer"
        assert category.description == "All electronic items"
        assert isinstance(category.date_created, timezone.datetime)

    def test_product_fields(self, product):
        assert product.product_name == "Smartphone"
        assert product.price == 599
        assert isinstance(product.date_created, timezone.datetime)

    def test_order_fields(self, order):
        assert isinstance(order.date_created, timezone.datetime)

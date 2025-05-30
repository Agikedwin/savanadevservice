from django.db.models import Avg
from graphene_django import DjangoObjectType
import graphene
from sales.models import Products, ProductCategory
from sales.utils.sma_utils import send_sms
from sales.utils.send_admin_mail import send_alert_email  # Uncomment when used


class ProductsType(DjangoObjectType):
    class Meta:
        model = Products
        fields = ('category_id', 'product_name', 'price', 'customer_id', 'user_id')


class ProductQueries(graphene.ObjectType):
    all_products = graphene.List(ProductsType)
    average_price_by_category = graphene.Float(category_id=graphene.Int(required=True))

    def resolve_all_products(root, info):
        return Products.objects.all()

    def resolve_average_price_by_category(self, info, category_id):
        category = ProductCategory.objects.filter(category_id=category_id).first()

        if not category:
            print(f"Category with id {category_id} does not exist.")
            return 0.0

        avg_result = Products.objects.filter(category_id=category.category_id).aggregate(avg_price=Avg('price'))
        avg_price = avg_result.get('avg_price')

        if avg_price is not None:
            customer_contact = '+254717450644'
            message = 'Please be notified that your order has been placed'

            sms_sent = send_sms(customer_contact, message)
            if sms_sent:
                print("✅ SMS sent to customer successfully.")
            else:
                print(" Failed to send SMS to the customer.")
            return avg_price

        print("No products found in this category.")
        return 0.0

    def send_customer_alerts(self):
        customer_contact = '+254717450644'
        message = 'Please be notified that your order has been placed'

        sms_sent = send_sms(customer_contact, message)
        if sms_sent:
            print("✅ SMS sent to customer successfully.")
        else:
            print(" Failed to send SMS to the customer.")

        # Uncomment below to enable email notifications
        # try:
        #     send_alert_email()
        #     print("✅ Admin email sent successfully.")
        # except Exception as e:
        #     print(f" Failed to send admin email: {e}")

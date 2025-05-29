from django.db.models import Avg
from graphene_django import DjangoObjectType
import graphene
from sales.models import Products,ProductCategory
from sales.utils.sma_utils import send_sms
from  sales.utils.send_admin_mail import send_alert_email



class ProductsType(DjangoObjectType):
    class Meta:
        model = Products
        fields = ('category_id', 'product_name','price','customer_id','user_id')

class ProductQueries(graphene.ObjectType):
    all_products = graphene.List(ProductsType)
    average_price_by_category = graphene.Float(category_id=graphene.Int(required=True))


    def resolve_all_products(root, info):
        return Products.objects.all()

    def resolve_average_price_by_category(self, info, category_id):
        print('Ready to send sms')
        category_exists = ProductCategory.objects.filter(category_id=category_id).first()
        print(category_exists)
        if not category_exists:
            raise Exception(f"The category with id {category_id} does not exist")
        result = Products.objects.filter(category_id=category_exists.category_id).aggregate(avg_price=Avg('price'))


        #write a decorator function here to handle sms sending
        print('Ready to send sms')
        customer_contact = '+254717450644'
        message = 'Please be notified that your order has been placed'
        res = send_sms(customer_contact, message)

        if res:
            print(f"SMS sent to customer successfully")

        else:
            print(f"Failed to send SMS to the customer")
        print('Done sending sms')

        print('Try sending email ')
        #send_alert_email()
        print('Done sending admin email')
        return result['avg_price']

    def send_customer_alerts(self, request):
        customer_contact= '+254717450644'
        message = 'Please be notified that your order has been placed'
        res = send_sms(customer_contact, message)

        if res :
            print(f"SMS sent to customer successfully")

        else:
            print(f"Failed to send SMS to the customer")


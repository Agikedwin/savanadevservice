from graphene_django import DjangoObjectType
import graphene
from sales.models import Customers

class CustomersType(DjangoObjectType):
    class Meta:
        model = Customers
        fields = "__all__"

class CustomerQueries(graphene.ObjectType):
    all_customers = graphene.List(CustomersType)
    customer_by_id = graphene.Field(CustomersType, id=graphene.Int(required=True))

    def resolve_all_customers(root, info):
        return Customers.objects.all()

    def resolve_customer_by_id(root, info, id):
        return Customers.objects.filter(customer_id=id).first()

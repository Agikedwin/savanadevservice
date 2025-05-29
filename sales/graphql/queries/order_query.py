from graphene_django import DjangoObjectType
import graphene
from sales.models import Orders

class OrdersType(DjangoObjectType):
    class Meta:
        model = Orders
        fields = "__all__"

class OrderQueries(graphene.ObjectType):
    all_orders = graphene.List(OrdersType)

    def resolve_all_orders(root, info):
        return Orders.objects.all()

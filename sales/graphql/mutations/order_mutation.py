import graphene
from graphene_django import DjangoObjectType
from sales.models import Orders, Products,Users,Customers
from sales.utils.send_admin_mail import send_alert_email

class OrdersType(DjangoObjectType):
    class Meta:
        model = Orders
        fields = "__all__"

class CreateOrder(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        customer_id = graphene.Int(required=True)
        user_id = graphene.Int(required = True)


    order = graphene.Field(OrdersType)
    @classmethod
    def mutate(cls,root, info, product_id, customer_id,user_id):
        product = Products.objects.filter(product_id=product_id).first()
        customer = Customers.objects.filter(customer_id=customer_id).first()
        user = Users.objects.filter(user_id=user_id).first()
        print(customer)

        order = Orders(
            product_id=product.product_id,
            customer_id=customer.customer_id,
            user_id = user.user_id
        )
        order.save()
        #Send the admin email here
        send_alert_email(customer.customer_name, product.product_name,user.name)
        return CreateOrder(order=order)

class UpdateOrder(graphene.Mutation):
    class Arguments:
        order_id = graphene.Int(required=True)
        product_id = graphene.Int()
        customer_id = graphene.Int()

    order = graphene.Field(OrdersType)

    def mutate(self, info, order_id, product_id=None, customer_id=None):
        order = Orders.objects.filter(order_id=order_id).first()
        if not order:
            raise Exception("Order not found")
        if product_id:
            order.product_id = product_id
        if customer_id:
            order.customer_id = customer_id
        order.save()
        return UpdateOrder(order=order)

class DeleteOrder(graphene.Mutation):
    class Arguments:
        order_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, order_id):
        order = Orders.objects.filter(order_id=order_id).first()
        if not order:
            raise Exception("Order not found")
        order.delete()
        return DeleteOrder(ok=True)

class OrderMutations(graphene.ObjectType):
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()

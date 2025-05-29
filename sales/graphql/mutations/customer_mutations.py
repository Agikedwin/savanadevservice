import graphene
from graphene_django import DjangoObjectType
from sales.models import Customers,Users

class CustomersType(DjangoObjectType):
    class Meta:
        model = Customers
        fields = "__all__"


class CreateCustomer(graphene.Mutation):
    class Arguments:
        customer_name = graphene.String(required=True)
        customer_contact = graphene.String()
        customer_email = graphene.String()
        customer_type = graphene.String()
        user_id = graphene.Int()

    customer = graphene.Field(CustomersType)

    @classmethod
    def mutate(cls,root, info, customer_name,customer_contact,customer_email,customer_type,user_id):
        user = Users.objects.filter(user_id=user_id).first()
        customer = Customers(
            customer_name=customer_name,
            customer_contact=customer_contact,
            customer_email=customer_email,
            customer_type=customer_type,
            user_id=user.user_id
        )
        customer.save()
        return CreateCustomer(customer=customer)

class UpdateCustomer(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required=True)
        name = graphene.String()

    customer = graphene.Field(CustomersType)

    def mutate(self, info, customer_id, name=None):
        customer = Customers.objects.filter(customer_id=customer_id).first()
        if not customer:
            raise Exception("Customer not found")
        if name:
            customer.name = name
        customer.save()
        return UpdateCustomer(customer=customer)

class DeleteCustomer(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, customer_id):
        customer = Customers.objects.filter(customer_id=customer_id).first()
        if not customer:
            raise Exception("Customer not found")
        customer.delete()
        return DeleteCustomer(ok=True)

class CustomerMutations(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    update_customer = UpdateCustomer.Field()
    delete_customer = DeleteCustomer.Field()

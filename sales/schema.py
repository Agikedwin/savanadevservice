from unicodedata import category
import graphene

from sales.graphql.queries.user_query import UserQueries
from sales.graphql.queries.customer_query import CustomerQueries
from sales.graphql.queries.product_category_query import CategoryQueries
from sales.graphql.queries.product_query import ProductQueries
from sales.graphql.queries.order_query import OrderQueries

from sales.graphql.mutations.user_mutations import UserMutations
from sales.graphql.mutations.customer_mutations import CustomerMutations
from sales.graphql.mutations.product_mutation import ProductMutations
from sales.graphql.mutations.product_category_mutation import CategoryMutations
from sales.graphql.mutations.order_mutation import OrderMutations

class Query(UserQueries,CustomerQueries,CategoryQueries,ProductQueries,OrderQueries):
    pass

class Mutation(UserMutations,CustomerMutations,ProductMutations,CategoryMutations,OrderMutations):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

"""


import graphene
from graphene_django import DjangoObjectType
from graphene import relay, Mutation

from .models import Users, Customers, ProductCategory, Products, Orders


# --- Object Types ---
class CustomersType(DjangoObjectType):
    class Meta:
        model = Customers
        fields = '__all__'


class UsersType(DjangoObjectType):
    class Meta:
        model = Users
        fields = ('user_id','name', 'role', 'description')


class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory
        fields = ('category_name', 'category_type')
        interfaces = (relay.Node,)


class ProductsType(DjangoObjectType):
    class Meta:
        model = Products
        fields = ('category_id', 'product_name')


class OrdersType(DjangoObjectType):
    class Meta:
        model = Orders
        fields = '__all__'


# --- Query ---
class Query(graphene.ObjectType):
    all_users = graphene.List(UsersType)
    user_by_id = graphene.Field(UsersType, userId=graphene.Int(required=True))
    all_customers = graphene.List(CustomersType)
    customer_by_id = graphene.Field(CustomersType, id=graphene.Int(required=True))
    all_prod_categories = graphene.List(ProductCategoryType)
    all_orders = graphene.List(OrdersType)
    all_products = graphene.List(ProductsType)

    def resolve_all_users(root, info):
        return Users.objects.all()

    def resolve_user_by_id(root, info, userId):
        return Users.objects.filter(user_id=userId).first()

    def resolve_all_customers(root, info):  # ❗ Fixed typo: was `all_customer`
        return Customers.objects.all()

    def resolve_customer_by_id(root, info, id):
        return Customers.objects.filter(customer_id=id).first()

    def resolve_all_prod_categories(root, info):  # ❗ Fixed name: was `all_category`
        return ProductCategory.objects.all()
    def resolve_all_orders(root, info):
        return  Orders.objects.all()

    def resolve_all_products(root, info):
        return  Products.objects.all()

class CreateUserMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        role = graphene.Int()
        description = graphene.String()

    user = graphene.Field(UsersType)
    @classmethod
    def mutate(cls, root, info, name, role,description):
        user = Users(name=name,role=role, description=description)
        user.save()
        return CreateUserMutation(user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required =True)
        name = graphene.String()
        description = graphene.String()

    user = graphene.Field(UsersType)

    @classmethod
    def mutate(cls, root, info, user_id, name, description):
        user = Users.objects.filter(user_id=user_id).first()

        if not user:
            raise  Exception("User not found")

        if name is not None:
            user.name = name
        if description is not  None:
            user.description = description
        user.save()
        return UpdateUser(user=user)

class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required = True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root ,info, user_id):
        user = Users.objects.filter(user_id=user_id).first()

        if not  user:
            raise Exception("User not found")

        user.delete()
        return DeleteUser(ok = True)


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUser.Field()
    delete_User = DeleteUser.Field()

# --- Schema ---
schema = graphene.Schema(query=Query, mutation=Mutation)


"""
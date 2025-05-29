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


class Query(UserQueries, CustomerQueries, CategoryQueries,
            ProductQueries, OrderQueries):
    pass


class Mutation(UserMutations, CustomerMutations, ProductMutations,
               CategoryMutations, OrderMutations):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)



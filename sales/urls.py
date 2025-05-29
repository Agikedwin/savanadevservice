from graphene_django.views import GraphQLView
from django.urls import path

from sales.schema import schema

urlpatterns = [
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
    path("oauth2/code/ql", GraphQLView.as_view(graphiql=True, schema=schema))
]

import graphene
from sales.models import Users
from graphene_django import DjangoObjectType

class UsersType(DjangoObjectType):
    class Meta:
        model = Users
        fields = ("user_id", "name", "role", "description")

class UserQueries(graphene.ObjectType):
    all_users = graphene.List(UsersType)
    user_by_id = graphene.Field(UsersType, userId=graphene.Int(required=True))

    def resolve_all_users(root, info):
        return Users.objects.all()

    def resolve_user_by_id(root, info, userId):
        return Users.objects.filter(user_id=userId).first()

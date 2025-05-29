import graphene
from sales.models import Users
from graphene_django import DjangoObjectType

class UsersType(DjangoObjectType):
    class Meta:
        model = Users
        fields = ("user_id", "name", "role", "description")

class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        role = graphene.Int(required=True)
        description = graphene.String()

    user = graphene.Field(UsersType)

    @classmethod
    def mutate(cls, root, info, name, role, description=None):
        user = Users(name=name, role=role, description=description)
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        name = graphene.String()
        role = graphene.Int()
        description = graphene.String()

    user = graphene.Field(UsersType)

    @classmethod
    def mutate(cls, root, info, user_id, name=None, role=None, description=None):
        user = Users.objects.filter(user_id=user_id).first()
        if not user:
            raise Exception("User not found")
        if name is not None:
            user.name = name
        if role is not None:
            user.role = role
        if description is not None:
            user.description = description
        user.save()
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, user_id):
        user = Users.objects.filter(user_id=user_id).first()
        if not user:
            raise Exception("User not found")
        user.delete()
        return DeleteUser(ok=True)


class UserMutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

import graphene
from graphene_django import DjangoObjectType
from sales.models import ProductCategory, Users

class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory
        fields = ('category_name','category_type','description','user_id')

class CreateCategory(graphene.Mutation):
    class Arguments:
        category_name = graphene.String(required=True)
        category_type = graphene.String()
        description = graphene.String()
        user_id = graphene.Int()

    category = graphene.Field(ProductCategoryType)

    @classmethod
    def mutate(cls,root, info, category_name, category_type,description,user_id):
        print(f"values {category_name} {category_type} {description} {user_id}")

        user = Users.objects.filter(user_id=user_id).first()


        if not user:
            raise Exception("User with supplied id not found ")
        category = ProductCategory(
            category_name=category_name,
            category_type=category_type,
            description=description,
            user_id=user.user_id
        )
        category.save()
        return CreateCategory(category=category)

class UpdateCategory(graphene.Mutation):
    class Arguments:
        category_id = graphene.Int(required=True)
        category_name = graphene.String()
        category_type = graphene.String()

    category = graphene.Field(ProductCategoryType)

    @classmethod
    def mutate(cls,root, info, category_id, category_name=None, category_type=None):
        category = ProductCategory.objects.filter(category_id=category_id).first()
        if not category:
            raise Exception("Category not found")
        if category_name:
            category.category_name = category_name
        if category_type:
            category.category_type = category_type
        category.save()
        return UpdateCategory(category=category)

class DeleteCategory(graphene.Mutation):
    class Arguments:
        category_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls,root, info, category_id):
        category = ProductCategory.objects.filter(category_id=category_id).first()
        if not category:
            raise Exception("Category not found")
        category.delete()
        return DeleteCategory(ok=True)

class CategoryMutations(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
import graphene
from sales.models import Products, ProductCategory, Users
from graphene_django import DjangoObjectType

class ProductsType(DjangoObjectType):
    class Meta:
        model = Products
        fields = ('category_id', 'product_name','user_id')

class CreateProduct(graphene.Mutation):
    class Arguments:
        product_name = graphene.String(required=True)
        category_id = graphene.Int(required=True)
        user_id = graphene.Int()
        price = graphene.Int()

    product = graphene.Field(ProductsType)

    @classmethod
    def mutate(cls,root, info, product_name,price, category_id,user_id):

        product_category = ProductCategory.objects.filter(category_id=category_id).first()
        if not product_category:
            raise Exception(f'Category id {category_id} is not found')

        user = Users.objects.filter(user_id=user_id).first()
        if not user:
            raise Exception(f'User with  id {user_id} is not found')

        product = Products(
            product_name=product_name,
            price=price,
            category_id=product_category.category_id,
            user_id=user.user_id
        )
        product.save()
        return CreateProduct(product=product)

class UpdateProduct(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        product_name = graphene.String()
        category_id = graphene.Int()

    product = graphene.Field(ProductsType)

    @classmethod
    def mutate(cls,self, info, product_id, product_name=None, category_id=None):
        product = Products.objects.filter(product_id=product_id).first()
        if not product:
            raise Exception("Product not found")
        if product_name:
            product.product_name = product_name
        if category_id:
            product.category_id = category_id
        product.save()
        return UpdateProduct(product=product)

class DeleteProduct(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls,self, info, product_id):
        product = Products.objects.filter(product_id=product_id).first()
        if not product:
            raise Exception("Product not found")
        product.delete()
        return DeleteProduct(ok=True)

class ProductMutations(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

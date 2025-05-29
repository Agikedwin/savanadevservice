from graphene_django import DjangoObjectType
import graphene
from sales.models import ProductCategory

class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory
        fields = ('category_name','category_type','category_id','description','user_id')

class CategoryQueries(graphene.ObjectType):
    all_prod_categories = graphene.List(ProductCategoryType)

    def resolve_all_prod_categories(root, info):
        return ProductCategory.objects.all()

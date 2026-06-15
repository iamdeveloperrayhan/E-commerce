from django.shortcuts import render
from products.models import Product,Category

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    category_slug = request.GET.get('category',None)

    if category_slug:
        current_category = Category.objects.filter(
            slug = category_slug
        ).first()

        products = Product.objects.filter(
            category = current_category
        )
    categories = Category.objects.all()
    return render(
        request=request,
        template_name='products/product_category.html',
        context={
            'products': products,
            'categories': categories,
            'current_category': category_slug,
        }
    )


def product_detail_view(request,pk):
    product = Product.objects.filter(id=pk).first()
    if product:
        return render(
            request=request,
            template_name='products/product_detail.html',
            context={
                'product': product,
            }
        )
    else:
        return render(
            request=request,
            template_name='products/product_detail.html',
            context={
                'message': "Product detail not found!",
            }
        )




from django.shortcuts import render, redirect
from .models import Products, Order
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    product_objects = Products.objects.all()

    # search code
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = Products.objects.filter(title__icontains=item_name)

    # paginator
    paginator = Paginator(product_objects, 4)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    return render(request, 'shop/index.html', {'product_object': product_objects})

def detail(request, id):
    product_object = Products.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product_object': product_object})
    
@login_required
def checkout(request):
    user_data = request.user
    # manual form input
    if request.method == "POST":
        total = request.POST.get('total', '')
        items = request.POST.get('items','')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zipcode = request.POST.get('zipcode', '')

        order = Order(total=total, items=items, name=name, email=email, address=address, city=city, state=state, zipcode=zipcode)
        try:
            order.save()
        except:
            pass

        return redirect('index')

    return render(request, 'shop/checkout.html', context={'user':user_data})
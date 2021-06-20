from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

import datetime

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count, Min, Sum, Value
from django.db.models.functions import Concat
# from .forms import AddToCartForm, AddToCartInListForm
# from .models import Category, SubCategory, SubSubCategory, Product
from apps.order.models import Order, OrderItem
from apps.vendor.models import Vendor, Customer
from apps.product.models import Product

from apps.cart.cart import Cart

# @login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


def changeOrderStatus(request, id, val):
    Order.objects.filter(id=id).update(status=val)
    return HttpResponse("")


def changeVendorEnalbed(request, id, val):
    Vendor.objects.filter(id=id).update(enabled=val)
    return HttpResponse("")   
 
def changeProductVisible(request, id, val):
    print(id, val)
    Product.objects.filter(id=id).update(visible=val)
    return HttpResponse("")   

# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        if load_template == "orders":
            context = page_orders(request)
        elif load_template == "vendors":
            context = page_vendors(request)
        elif load_template == "customers":
            context = page_customers(request)
        elif load_template == "product_review":
            context = page_product_review(request)
        context['segment'] = load_template

        
        html_template = loader.get_template( load_template + ".html")
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))


def page_orders(request):
    context = {}
    orders = Order.objects.all()
    context['orders'] = orders

    
    today = datetime.date.today()
    start_week = today - datetime.timedelta(today.weekday())
    end_week = start_week + datetime.timedelta(7)

    # users = {}
    # for order in orders:
    #     username = order.first_name + " " + order.last_name
    #     if username.lower() not in users:
    #         users[username.lower()] = {"f": order.first_name, "l": order.last_name}

    # for user in users:
    #     daily_orders = Order.objects.filter(first_name__iexact=users[user]["f"], last_name__iexact=users[user]["l"], created_at__year=today.year, created_at__month=today.month, created_at__day=today.day).aggregate
    #     weekly_orders = Order.objects.filter(first_name__iexact=users[user]["f"], last_name__iexact=users[user]["l"], created_at__range=[start_week, end_week])
    # o = Order.objects.extra(select={'username': Concat('first_name', Value(' '),  'last_name')}).annotate(count=Count('paid_amount'))
    # o = Order.objects.all().values("first_name", "last_name").annotate(count=Count('first_name'), amount=Sum('paid_amount')).order_by()

    daily_orders = Order.objects.filter(created_at__year=today.year, created_at__month=today.month, created_at__day=today.day).values("first_name", "last_name").annotate(count=Count('first_name'), amount=Sum('paid_amount')).order_by()
    weekly_orders = Order.objects.filter(created_at__range=[start_week, end_week]).values("first_name", "last_name").annotate(count=Count('first_name'), amount=Sum('paid_amount')).order_by()
    monthly_orders = Order.objects.filter(created_at__year=today.year, created_at__month=today.month).values("first_name", "last_name").annotate(count=Count('first_name'), amount=Sum('paid_amount')).order_by()

    statistics = []
    for order in daily_orders:
        statistics.append({'period': 'daily', 'username': order["first_name"] + " " + order["last_name"], 'count': order["count"], 'amount': order["amount"]})

    for order in weekly_orders:
        statistics.append({'period': 'weekly', 'username': order["first_name"] + " " + order["last_name"], 'count': order["count"], 'amount': order["amount"]})

    for order in monthly_orders:
        statistics.append({'period': 'monthly', 'username': order["first_name"] + " " + order["last_name"], 'count': order["count"], 'amount': order["amount"]})

    context['statistics'] = statistics

    return context


def page_vendors(request):
    context = {}
    vendors = Product.objects.select_related("vendor").all().values("vendor__id", "vendor__company_name", "vendor__company_code", "vendor__email", "vendor__address", "vendor__phone", "vendor__enabled").annotate(products=Count("vendor__company_name")).order_by()
    vendor_list = []
    for vendor in vendors:
        vendor_list.append({"id": vendor["vendor__id"], "name": vendor["vendor__company_name"], "code": vendor["vendor__company_code"], "email": vendor["vendor__email"], "address": vendor["vendor__address"], "phone": vendor["vendor__phone"], "enabled": vendor["vendor__enabled"], "products": vendor["products"]})
    context['vendors'] = vendor_list
    
    return context


def page_customers(request):
    context = {}
    customers = Customer.objects.all()
    customer_list = []
    for customer in customers:
        customer_list.append({"id": customer.user_id, "name": customer.customername, "email": customer.email, "address": customer.address, "phone": customer.phone, "created": customer.created_at})
    context['customers'] = customer_list
    
    return context


def page_product_review(request):
    context = {}
    products = Product.objects.filter(visible=False)
    product_list = []
    for product in products:
        # print(product.category_id, product.category, product.category)
        print(product.category_id, product.category, product.category.sub_category, product.category.sub_category.category)
        product_list.append({"id": product.id, "title": product.title, "description": product.description, "price": product.price, "date_added": product.date_added, "image": product.image, "vendor": product.vendor.company_name, "slug": product.category.sub_category.category.slug + "/" + product.category.sub_category.slug + "/" + product.category.slug + "/" + product.slug, "main_category": product.category.sub_category.category.title, "sub_category": product.category.sub_category.title, "sub_sub_category": product.category.title, "num_available": product.num_available, "visible": product.visible})
    context['products'] = product_list
    
    return context


def product_admin(request, category_slug, subcategory_slug, subsubcategory_slug, product_slug):
    cart = Cart(request)

    product = get_object_or_404(
        Product, category__slug=subsubcategory_slug, slug=product_slug)

    cart = Cart(request)

    if cart.has_product(product.id):
        product.in_cart = True
    else:
        product.in_cart = False

    return render(request, 'product/product_admin.html', {'product': product})

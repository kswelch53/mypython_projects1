from django.shortcuts import render, HttpResponse, redirect
from .models import Product
from ..shoes1.models import *
# allows flash messages to html
from django.contrib import messages
import datetime


# displays all shoes for sale on shoes.html
def shoes(request):
    if 'user_id' not in request.session:
        return redirect('shoes1:index')
    else:
        print("This is shoes method in shoes2 views.py")

        # excludes all shoes that have been sold
        context = {
            'products': Product.objects.all().exclude(sold="True"),
        }
        return render(request, 'shoes2/shoes.html', context)


# displays dashboard.html, form for sellers to list shoes for sale, buy/sell tables
# sums buyer purchase total and seller sales total for session user as buyer/seller
def dashboard(request):
    print("This is dashboard method in shoes2 views.py")
    buyer_total = 0
    seller_total = 0

# designates session user as buyer and seller
    user_id = request.session['user_id']
    this_buyer = User.objects.get(id=user_id)
    this_seller = User.objects.get(id=user_id)

# gets all of seller's shoes
    sellers_shoes = Product.objects.filter(seller_link=this_seller)
# creates 2 arrays: not sold and sold
    shoes_not_sold = [] # for table 1
    shoes_sold = [] # for table 2
# sorts all of seller's Products by sold status
    for shoes in sellers_shoes:
        print(shoes.name)
        if shoes.sold == False:
            shoes_not_sold.append(shoes) # table 1: creates array of all seller's shoes that were not sold
            print("Not sold:", shoes.name)
        else: # if sold status is True
            shoes_sold.append(shoes) # table 2: creates array of all seller's shoes that were sold
            print("Sold:", shoes.name, "Buyer is:", shoes.buyer_link.first_name)
# get amount for each shoes sold, total them
            product_price = shoes.amount
            seller_total = seller_total + product_price
            print("Seller total is:", seller_total)


# for table 3: gets all shoes bought by session user
# sold status can be ignored here; if buyer_link exists, the shoes have been sold
    shoes_bought = Product.objects.filter(buyer_link=this_buyer)
    for shoes in shoes_bought:
        print(shoes, "purchased by", this_buyer.first_name)
        # get amount for each shoes bought, total them
        product_price = shoes.amount
        buyer_total = buyer_total + product_price
        print("Buyer total is", buyer_total)


    context = {
        # 'products': Product.objects.all(),
        'shoes_not_sold': shoes_not_sold, # table 1
        'shoes_sold': shoes_sold, # table 2
        'seller_total': seller_total, # table 2 total
        'shoes_bought': shoes_bought, # table 3
        'buyer_total': buyer_total, # table 3 total
    }
    return render(request, 'shoes2/dashboard.html', context)


# this is a create method
# session user lists an item for sale, creating a Product object
def list_forsale(request):
    print("This is list_forsale method in shoes2 views.py")
    if request.method == "POST":
    # gets form data
        seller_id = request.session['user_id']
        this_seller = User.objects.get(id=seller_id)
        product_name = request.POST['name']
        product_amount = request.POST['amount']
        print(this_seller.first_name, this_seller.last_name, "is selling", product_name, "for $", product_amount)
# create Product
        this_product = Product.objects.create(seller_link=this_seller, name=product_name, amount=product_amount)
        return redirect('shoes2:shoes')
    return redirect('shoes2:list_forsale')


# When buyer purchases a Product, buyer is linked to Product and sold status changes to True
def buy(request, shoes_id):
    print("This is buy method in shoes2 views.py")
    user_id = request.session['user_id']
    this_buyer = User.objects.get(id=user_id) # identifies session user as buyer
    this_product = Product.objects.get(id=shoes_id) # gets selected Product
    this_product.buyer_link = this_buyer # links buyer to Product
    this_product.date_bought = datetime.date.today() # sets sell date
    # changes sold status to True
    this_product.sold = "True"
    this_product.save()

# checks
    print("Product is:", this_product.name)
    print("Buyer is:", this_product.buyer_link.first_name)
    print("Seller is:", this_product.seller_link.first_name)
    print("Date posted is:", this_product.date_posted)
    print("Date sold is:", this_product.date_bought)
    print("Amount is: $", this_product.amount)
    print("Sold status is:", this_product.sold)

    return redirect('shoes2:dashboard')


# seller can unlist a Product by deleting it
def remove(request, shoes_id):
    print("This is remove method in shoes2 views.py")
    this_product = Product.objects.get(id=shoes_id)
    this_product.delete()
    print("Deleted")
    return redirect('shoes2:dashboard')

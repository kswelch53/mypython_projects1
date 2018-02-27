from django.shortcuts import render, HttpResponse, redirect
from decimal import Decimal
from .models import Product

secret_key = "checkout"

# Create your views here.
def index(request):
    print("This is amadon_index in views.py")
    counter = 0
    if 'chargeamount' not in request.session:
        request.session['chargeamount'] = 0
        request.session['counter'] = 0
        print("Chargeamount is", request.session['chargeamount'])
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'amadon_store/index.html', context)

def clear(request):
    print("This is clear function in views.py");
    request.session['chargeamount'] = 0
    request.session['counter'] = 0
    return redirect('amadon_store:index')


def process_order(request):
    print("This is process_order in views.py")
    print("Option is:", request.POST['quantity'])

    if request.method == "POST":
        print("Item is:", request.POST['item'])

    # item is the id number of the Product object
    # there are 4 products: tshirt, sweater, cup and book
    if request.POST["item"] == "1":
        quantity = int(request.POST['quantity'])
        price = 19.99 * quantity
        price = round(price, 2)
        # price = Decimal(price)
        request.session['counter'] = request.session['counter'] + quantity
        counter = request.session['counter']
        print("T-shirt price is: $", price, "Counter is:", counter)

        request.session['price'] = price

        request.session['chargeamount'] = round(request.session['chargeamount'] + price, 2)
        print("Your charge is: $", request.session['chargeamount'])
        return redirect('amadon_store:checkout')

    if request.POST["item"] == "2":
        quantity = int(request.POST['quantity'])
        price = 29.99 * quantity
        price = round(price, 2)
        request.session['counter'] = request.session['counter'] + quantity
        counter = request.session['counter']
        print("Sweater price is: $", price, "Counter is:", counter)
        request.session['price'] = price
        request.session['chargeamount'] = round(request.session['chargeamount'] + price, 2)
        print("Your charge is: $", request.session['chargeamount'])
        return redirect('amadon_store:checkout')

    if request.POST["item"] == "3":
        quantity = int(request.POST['quantity'])
        price = 4.99 * quantity
        price = round(price, 2)
        request.session['counter'] = request.session['counter'] + quantity
        counter = request.session['counter']
        print("Cup price is: $", price, "Counter is:", counter)
        request.session['price'] = price
        request.session['chargeamount'] = round(request.session['chargeamount'] + price, 2)
        print("Your charge is: $", request.session['chargeamount'])
        return redirect('amadon_store:checkout')

    if request.POST["item"] == "4":
        quantity = int(request.POST['quantity'])
        price = 49.99 * quantity
        price = round(price, 2)
        request.session['counter'] = request.session['counter'] + quantity
        counter = request.session['counter']
        print("Book price is: $", price, "Counter is:", counter)
        request.session['price'] = price
        request.session['chargeamount'] = round(request.session['chargeamount'] + price, 2)
        print("Your charge is: $", request.session['chargeamount'])
        return redirect('amadon_store:checkout')

    return redirect('amadon_store:index')


def checkout(request):
    print("This is checkout function in views.py")
    return render(request, 'amadon_store/checkout.html')

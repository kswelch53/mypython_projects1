from django.shortcuts import render, HttpResponse, redirect
from random import randint

# Create your views here.
def ninjagold_index(request):
    print("This is ninjagold_index method in views.py")
    if 'goldcounter' not in request.session:
        request.session['goldcounter'] = 0
        request.session['updatelist'] = list()
    if 'color' not in request.session:
        request.session['color'] = "black"
    return render(request, 'ninja_gold/index.html')

def clear(request):
    print("This is clear method in ninja_gold views.py")
    request.session['goldcounter'] = 0
    request.session['updatelist'] = list()
    return redirect('ninja_gold:index')

def process_money(request):
    print("This is process_money method in ninja_gold views.py")
    winlose = "earned"
    if request.POST["place"] == "farm":
        request.session['color'] = "green"
        gold = randint(10,20)
        updatelist = winlose, gold, "farm"
        request.session['goldcounter'] = request.session['goldcounter'] + gold
    if request.POST["place"] == "cave":
        request.session['color'] = "black"
        gold = randint(5,10)
        updatelist = winlose, gold, "cave"
        request.session['goldcounter'] = request.session['goldcounter'] + gold
    if request.POST["place"] == "house":
        request.session['color'] = "purple"
        gold = randint(2,5)
        updatelist = winlose, gold, "house"
        request.session['goldcounter'] = request.session['goldcounter'] + gold
    if request.POST["place"] == "casino":
        gold = randint(-50, 50)
        if gold >= 0:
            print("Color is", request.session['color'])
            print("Gold won is", gold)
            request.session['color'] = "blue"
            print("Color is", request.session['color'])
            updatelist = winlose, gold, "casino"
            request.session['goldcounter'] = request.session['goldcounter'] + gold
        else:
            print("Color is", request.session['color'])
            print("Gold lost is", gold)
            request.session['color'] ="red"
            print("Color is", request.session['color'])
            gold = abs(gold)
            winlose = "lost"
            updatelist = winlose, gold, "casino"
            request.session['goldcounter'] = request.session['goldcounter'] + gold
    request.session['updatelist'].append(updatelist)
    return redirect('ninja_gold:index')

from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.forms import ItemForm
from lists.models import Item, List
from django.core.exceptions import ValidationError

# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(list_)

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"

    items = Item.objects.filter(list=list_)
    counter= items.count()
    status = 'yey, waktunya berlibur'

    if counter == 0:
         status = 'yey, waktunya berlibur'
    elif counter < 5:
         status = 'sibuk tapi santai'
    else:
         status = 'oh tidak'
    return render(request, 'list.html', {'items': items, 'status': status, 'list': list_})

'''
def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
'''

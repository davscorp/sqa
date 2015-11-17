from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError

# Create your views here.
def home_page(request):
  #  if request.method == 'POST':
  #      return HttpResponse(request.POST['item_text'])
  #  return HttpResponse(b'<html><title>David Lawrence - 1206208523</title></html>')
  #  item = Item()
  #  item.text = request.POST.get('item_text', '')
  #  item.save()

  # return render(request, 'home.html', {
  #      'new_item_text': item.text
  # })
    #if request.method == 'POST':
     #  Item.objects.create(text=request.POST['item_text'])
       #return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    counter= items.count()
    status = ''

    if counter == 0:
         status = 'yey, waktunya berlibur'
    elif counter < 5:
         status = 'sibuk tapi santai'
    else:
         status = 'oh tidak'
    return render(request, 'list.html', {'items': items, 'status': status, 'list': list_})

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect('/lists/%d/' % (list_.id,))

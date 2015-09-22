from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item

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
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    #return render(request, 'home.html')

    items = Item.objects.all()
    counter= items.count()
    status = ''  

    if counter == 0:
         status = 'yey, waktunya berlibur'
    elif counter < 5: 
         status = 'sibuk tapi santai'
    else: 
         status = 'oh tidak'
    return render(request, 'home.html', {'items': items, 'status': status})

def new_list(request):
#    pass
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')

def view_list(request):
#     pass
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        return HttpResponse(request.POST['item_text'])
  #  return HttpResponse(b'<html><title>David Lawrence - 1206208523</title></html>')
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })

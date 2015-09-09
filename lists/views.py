from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page(request):
#    return HttpResponse('<html><title>David Lawrence - 1206208523</title></html>')
     return render(request, 'index.html')

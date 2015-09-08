from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return HttpResponse('<html><title>David Lawrence - 1206208523</title></html>')

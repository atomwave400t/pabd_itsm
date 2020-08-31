from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, 'pabd_itsm/index.html')

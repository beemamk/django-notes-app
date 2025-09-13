# In my_project/views.py (or another app's views.py)

from django.shortcuts import render

def register_view(request):
    return render(request, 'register.html')
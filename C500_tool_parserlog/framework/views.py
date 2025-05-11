from django.shortcuts import render, redirect
from django.http import HttpResponse

# views.py
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, 'Layouts/_root.html')

def index2(request):
    return HttpResponse("Hello, world. You're at the framework index2.")

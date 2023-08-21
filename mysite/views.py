from django.shortcuts import render, redirect
from django.http import request

# Create your views here.

def index(request):
    return render(request, 'index.html')

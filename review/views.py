from django.http import HttpResponse
from django.shortcuts import render

def display(request, id):
    return HttpResponse("hello!")

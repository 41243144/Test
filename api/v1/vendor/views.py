from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def health(request):
    return JsonResponse({"status": "ok", "app": "vendor"})

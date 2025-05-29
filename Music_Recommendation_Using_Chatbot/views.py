import subprocess
from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views import View

from Backend.tone_analysis import select_and_run_function


def my_view(request):
    # Your view logic goes here
    return render(request, 'index.html')

class sample(View):
    def get(self, request,function_name, param1):
        print(param1)
        print(function_name)
        # Your processing logic here
        return JsonResponse({'output': param1})

class tone_analyser(View):
    def get(self, request, function_name, param1):
        result = select_and_run_function(function_name, param1)
        # Convert the output to JSON
        print(result)
        return JsonResponse({"output": result})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import multiprocessing
import requests


@csrf_exempt
def send(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            encoded_data = data.get('data', '')
            create_new_process(encoded_data)
            return JsonResponse({'success': 'cool'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def create_new_process(data):
    process = multiprocessing.Process(target=send_data, args=(data, ))
    process.start()
    process.join()


def send_data(data):
    try:
        url = "http://127.0.0.1:8000/api/data/"
        response = requests.post(url, json=data)
        print(response.json())
    except Exception as ex:
        print(ex)

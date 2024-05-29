import numpy as np
import tensorflow as tf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def home(request):
    return render(request, 'audio_app/audio_recorder.html')


# TensorFlow Lite 모델 로드 및 초기화
interpreter = tf.lite.Interpreter(model_path=r"C:\Users\Yaggo\OneDrive\Desktop\py\django\advan\audio_project\converted_tflite\soundclassifier_with_metadata.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

@csrf_exempt
def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_data'):
        audio_file = request.FILES['audio_data']
        audio_data = np.frombuffer(audio_file.read(), dtype=np.int16)

         # audio_data 길이가 int16 (2바이트)의 배수인지 확인하고 조정
        if len(audio_data) % 2 != 0:
            # 길이가 홀수인 경우 마지막 바이트를 제거
            audio_data = audio_data[:-1]

          # 데이터를 numpy 배열로 변환
        audio_data = np.frombuffer(audio_data, dtype=np.int16)

        # 데이터 정규화 및 타입 변환
        audio_data = audio_data.astype(np.float32) / 32768.0  # 16-bit 데이터를 [-1, 1] 범위로 정규화

        # 모델 입력 크기에 맞게 데이터 조정 및 차원 확장
        if audio_data.size < input_details[0]['shape'][1]:
            padding = np.zeros((input_details[0]['shape'][1] - audio_data.size,), dtype=np.float32)
            audio_data = np.concatenate((audio_data, padding), axis=0)
        elif audio_data.size > input_details[0]['shape'][1]:
            audio_data = audio_data[:input_details[0]['shape'][1]]
        audio_data = np.expand_dims(audio_data, axis=0)

        # TensorFlow Lite 모델 실행
        interpreter.set_tensor(input_details[0]['index'], audio_data)
        interpreter.invoke()

        # 예측 결과 가져오기
        output_data = interpreter.get_tensor(output_details[0]['index'])[0]
        predicted_indices = np.argsort(-output_data)[:3]  # 상위 3개 결과
        predicted_scores = output_data[predicted_indices]

        probabilities = tf.nn.softmax(output_data).numpy()

        return JsonResponse({'predicted_probabilities': probabilities.tolist()})
    else:
        return JsonResponse({'error': 'No audio file provided'}, status=400)

from django.urls import path, include
from audio_app.views import home  # views를 임포트하는 부분이 추가되어야 합니다.

urlpatterns = [
    path('', home, name='home'),  # 홈 페이지 URL
    path('audio/', include('audio_app.urls')),  # 기존 오디오 앱 URL
]


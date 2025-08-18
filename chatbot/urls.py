from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),             # / -> Home
    path('chat/', views.chat_page, name='chat_page'),        # /chat/ -> Chat page
    path('get_response/', views.get_response, name='get_response'),
]

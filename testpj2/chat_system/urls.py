from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:room_id>/', views.chat_room, name='chat_room'),
    path('my-chats/', views.my_chats, name='my_chats'),
    path('send-message/<int:room_id>/', views.send_message, name='send_message'),
    path('get-messages/<int:room_id>/', views.get_messages, name='get_messages'),
]

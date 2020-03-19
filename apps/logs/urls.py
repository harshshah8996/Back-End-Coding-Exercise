from django.urls import path, include
from logs.views import LogView

urlpatterns = [
    path('', LogView.as_view()),

]

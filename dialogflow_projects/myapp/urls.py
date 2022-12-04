from django.urls import path
from . import views

urlpatterns = [
    path('sample/',views.sample_view),
    path('second/',views.new_sample),
    path('dialogflow-webhook/',views.dialogflow_webhook),
]

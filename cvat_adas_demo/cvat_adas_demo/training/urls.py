from django.urls import path, include
from rest_framework import routers

from cvat_adas_demo.training.views import PredictView

router = routers.DefaultRouter(trailing_slash=False)
router.register('', PredictView, basename='predict')

urlpatterns = [
    path('', include((router.urls, 'predict'), namespace='predict'))
]

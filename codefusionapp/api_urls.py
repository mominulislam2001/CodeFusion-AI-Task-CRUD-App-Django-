# codefusionapp/api_urls.py
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet     # the DRF ViewSet you already have

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')

urlpatterns = router.urls

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Country
from .serializers import CountrySerializer

class CountryViewSet(viewsets.ModelViewSet):
    """
    CRUD + custom actions:
      • /countries/{pk}/regional/          – same region
      • /countries/language/<code>/        – same language (iso-639-3)
      • /countries/search/?q=<name>        – partial name search
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    
    @action(detail=True, methods=['get'])
    def regional(self, request, pk=None):
        country = self.get_object()
        qs = Country.objects.filter(region=country.region).exclude(pk=country.pk)
        return Response(CountrySerializer(qs, many=True).data)

    @action(detail=False, url_path=r'language/(?P<lang>[A-Za-z]{3})')
    def by_language(self, request, lang=None):
        qs = Country.objects.filter(languages__icontains=lang)  # naive contains
        return Response(CountrySerializer(qs, many=True).data)

    def list(self, request, *args, **kwargs):
        q = request.GET.get('q')
        if q:
            self.queryset = self.queryset.filter(name__icontains=q)
        return super().list(request, *args, **kwargs)

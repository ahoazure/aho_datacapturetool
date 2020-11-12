from django.shortcuts import render # This is a default import
from rest_framework import viewsets

from elements.models import (StgDataElement, FactDataElement)
from elements.serializers import (
    StgDataElementSerializer, FactDataElementSerializer)


class StgDataElementViewSet(viewsets.ModelViewSet):
    queryset = StgDataElement.objects.all()
    serializer_class = StgDataElementSerializer


class FactDataElementViewSet(viewsets.ModelViewSet):
    queryset = FactDataElement.objects.all()
    serializer_class = FactDataElementSerializer

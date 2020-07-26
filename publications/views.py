from django.shortcuts import render
from rest_framework import viewsets
from .models import (StgResourceType, StgKnowledgeProduct, StgProductDomain,)
from publications.serializers import (StgResourceTypeSerializer,
    StgKnowledgeProductSerializer,StgKnowledgeDomainSerializer,)

class StgResourceTypeViewSet(viewsets.ModelViewSet):
    queryset = StgResourceType.objects.all()
    serializer_class = StgResourceTypeSerializer


class StgKnowledgeProductViewSet(viewsets.ModelViewSet):
    queryset = StgKnowledgeProduct.objects.all()
    serializer_class = StgKnowledgeProductSerializer


class StgKnowledgeDomainViewSet(viewsets.ModelViewSet):
    queryset = StgProductDomain.objects.all()
    serializer_class = StgKnowledgeDomainSerializer

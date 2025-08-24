from django.db.models import Q
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ad
from .serializers import AdSer
from .pagination import StandardResultsSetPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPublisherOrReadOnly

class AdListView(APIView, StandardResultsSetPagination):
    serializer_class = AdSer

    def get(self, request):
        queryset = Ad.objects.filter(is_public=True)
        result = self.paginate_queryset(queryset, request)
        ser = AdSer(result, many=True)
        return self.get_paginated_response(ser.data)


class AdCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdSer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        ser = AdSer(data=request.data)
        if ser.is_valid():
            ser.validated_data['publisher'] = request.user
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)



class AdDetailView(APIView):
    permission_classes = (IsAuthenticated, IsPublisherOrReadOnly)
    serializer_class = AdSer
    parser_classes = (MultiPartParser,)

    def get_object(self, pk):
        try:
            return Ad.objects.get(pk=pk)
        except Ad.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object()
        ser = AdSer(obj)
        return Response(ser.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj = self.get_object()
        ser = AdSer(data=request.data, instance=obj)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object()
        obj.delete()
        return Response({'response': 'Done'}, status=status.HTTP_204_NO_CONTENT)


class AdSearchView(APIView, StandardResultsSetPagination):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdSer

    def get(self, request):
        q = request.GET.get('q')
        queryset = Ad.objects.filter(Q(title=q) | Q(contain=q))
        result = self.paginate_queryset(queryset, request)
        ser = AdSer(result, many=True)
        return self.get_paginated_response(ser.data)
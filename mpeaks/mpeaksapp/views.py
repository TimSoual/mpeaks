from django.views.decorators.csrf import csrf_exempt

from django.contrib.gis.geos import Polygon

from .models import Peak
from .serializers import PeakSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@csrf_exempt
@api_view(['GET', 'POST'])
def PeakList(request):
    """
    List all peaks, or create a new peak.
    """
    if request.method == 'GET':
        peaks = Peak.objects.all()
        serializer = PeakSerializer(peaks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PeakSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def PeakDetail(request, pk):
    """
    Get, udpate, or delete a specific peak.
    """
    try:
        task = Peak.objects.get(pk=pk)
    except Peak.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PeakSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PeakSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET'])
def PeakFilterList(request):
    """
    Find peaks inside boundary given by a geographical bounding box.
    """
    min_lon = request.query_params.get('minlon')
    min_lat= request.query_params.get('minlat')
    max_lon = request.query_params.get('maxlon')
    max_lat= request.query_params.get('maxlat')

    if not all([min_lon, min_lat, max_lon, max_lat]):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    bbox = (max_lon, max_lat, min_lon, min_lat)
    geom = Polygon.from_bbox(bbox)
    peaks = Peak.objects.filter(location__within=geom)
    serializer = PeakSerializer(peaks, many=True)
    return Response(serializer.data)

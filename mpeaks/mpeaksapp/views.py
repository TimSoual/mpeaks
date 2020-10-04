from django.views.decorators.csrf import csrf_exempt

from django.contrib.gis.geos import Polygon

from .models import Peak
from .serializers import PeakSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

ex = {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [38.66935, -122.633316]
    },
    "properties": {
    "altitude": 4810.0,
    "name": "Mount Saint Helena"
    }
}
peak_response = openapi.Response('peak description', PeakSerializer, examples={'application/json': ex})
peak_responses = openapi.Response('peak description', PeakSerializer(many=True), examples={'application/json': [ex]})

@csrf_exempt
@swagger_auto_schema(method='get', responses={200: peak_responses}, operation_description="List all peaks")
@swagger_auto_schema(method='post', request_body=PeakSerializer, responses={200: peak_responses}, operation_description="Create a new peak")
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
@swagger_auto_schema(method='get', operation_description="Get an existing peak", responses={200: peak_response, 404: 'Error: Not Found'})
@swagger_auto_schema(method='put', operation_description="Update an existing peak", request_body=PeakSerializer, responses={200: peak_response, 404: 'Error: Not Found', 400: 'Bad request'})
@swagger_auto_schema(method='delete', operation_description="Delete an existing peak")
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


minlon_param = openapi.Parameter('minlon', openapi.IN_QUERY, description="Minimum longitude", type=openapi.TYPE_NUMBER)
minlat_param = openapi.Parameter('minlat', openapi.IN_QUERY, description="Minimum latitude", type=openapi.TYPE_NUMBER)
maxlon_param = openapi.Parameter('maxlon', openapi.IN_QUERY, description="Maximum longitude", type=openapi.TYPE_NUMBER)
maxlat_param = openapi.Parameter('maxlat', openapi.IN_QUERY, description="Maximum latitude", type=openapi.TYPE_NUMBER)

@csrf_exempt
@swagger_auto_schema(method='get', operation_description="Get a list of peaks in an area", manual_parameters=[minlon_param, minlat_param, maxlon_param, maxlat_param], responses={200: peak_responses})
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

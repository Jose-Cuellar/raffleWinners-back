from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RaffleCreateSerializer

# Create your views here.
class RaffleCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serrializer = RaffleCreateSerializer(data=request.data)

        if serrializer.is_valid():
            serrializer.save()
            return Response(
                {
                    "message": "Rifa creada",
                    "data": serrializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                "message": "Error creando la rifa",
                "error": serrializer.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
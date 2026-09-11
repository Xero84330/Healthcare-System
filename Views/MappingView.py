from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from Apps.Mapping.models import Mapping
from Serializers.MappingSerializer import MappingSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mapping.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from Apps.Mapping.models import Mapping
from Serializers.MappingSerializer import MappingSerializer


class MappingPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        mappings = Mapping.objects.filter(patient_id=id)
        serializer = MappingSerializer(mappings, many=True)
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            mapping = Mapping.objects.get(id=id)
        except Mapping.DoesNotExist:
            return Response(
                {"detail": "Mapping not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
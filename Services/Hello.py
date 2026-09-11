from rest_framework.views import APIView
from rest_framework.response import Response

class HelloApi(APIView):

    def get(self, request):
        return Response(
            {"Message": "Hello from the backend"}
        )
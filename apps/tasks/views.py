from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime


# Create your views here.
def hello_world(request):
    now = datetime.datetime.now()
    html = '<html lang="en"><body>It is now %s.</body></html>' % now
    return HttpResponse(html)


class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {"status": "request was permitted"}
        return Response(content)

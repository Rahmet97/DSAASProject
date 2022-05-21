import random
import string

from django.shortcuts import redirect
from rest_framework import response, status, generics

from auser.models import Worker
from .utils import get_client_ip
from .models import UrlShort, UrlClicker
from .serializers import UrlSerializer


class UrlShortView(generics.GenericAPIView):
    serializer_class = UrlSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if Worker.objects.filter(employee=request.user).exists():
            boss = request.user.employee_related.get().whose_employee
        else:
            boss = request.user

        serializer.save(director_user=boss)

        serializer.is_valid(raise_exception=True)
        slug = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        serializer.save(slug=slug)
        return response.Response(data={"message": "successfully shorted link"}, status=status.HTTP_200_OK)


def add_url_clicker(request, obj):
    ip = get_client_ip(request)
    if UrlClicker.objects.filter(ip_address=ip).exists():
        clicker = UrlClicker.objects.get(ip_address=ip)
    else:
        clicker = UrlClicker.objects.create(ip_address=ip)
    clicker_id = clicker.id
    if not obj.clickers.filter(id=clicker_id).exists():
        obj.clickers.add(clicker)


def url_redirect(request, slugs):
    data = UrlShort.objects.get(slug=slugs)
    add_url_clicker(request, data)
    return redirect(data.original_url)

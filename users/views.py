import random

from django.core.cache import cache

from rest_framework.views import APIView
import rest_framework.status as status
from rest_framework.response import Response

from .models import User, Device


class RegisterUserView(APIView):

    def post(self, request):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
            return Response({'detail': 'User already registered!'},
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=phone_number)
        # user, created = User.objects.get_or_create(phone_number=phone_number)

        device = Device.objects.create(user=user)

        code = random.randint(10000, 99999)

        # send message (sms or email)
        # cache
        cache.set(str(phone_number), code, 2 * 60)

        return Response({'code': code})

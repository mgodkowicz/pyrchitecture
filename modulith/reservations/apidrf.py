from dependency_injector.wiring import Provide, inject
from django.contrib.auth.models import User
from rest_framework import routers, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from config.containers import ApplicationContainer
from config.root import injector
from reservations.service import SomeKindService, SomeKindServiceDI2


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


@inject
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # service = injector.get(SomeKindService)
    service: SomeKindServiceDI2 = Provide[ApplicationContainer.reservations.service]
    # alternative declaration in __init__
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.service = injector.get(SomeKindService)

    @action(detail=False)
    def add(self, request):
        a, b = int(request.GET.get('a')), int(request.GET.get('b'))
        return Response({'result': self.service.add(a, b)})

    @action(detail=False)
    def add2(self,
             request,
             ):
        print(self.service)
        a, b = int(request.GET.get('a')), int(request.GET.get('b'))
        return Response({'result': self.service.add(a, b)})


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

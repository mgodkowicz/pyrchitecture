from ninja import NinjaAPI

from config.root import injector
from reservations.service import SomeKindService

api = NinjaAPI(version="1")


@api.get("/add")
def add(request, a: int, b: int):
    service = injector.get(SomeKindService)

    return {"result": service.add(a, b)}

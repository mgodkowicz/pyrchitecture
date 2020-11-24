from django.http import HttpRequest, HttpResponse, JsonResponse
from fastapi import APIRouter, Depends, Response, HTTPException
from pydantic import UUID4
from starlette import status

from aggreagates.payments.application.config import payments_facade, create_payments_facade
from aggreagates.payments.application.facade import PaymentsFacade

router = APIRouter()


@router.get("/payment")
def hex_view(facade: PaymentsFacade = Depends(create_payments_facade)):
    result = facade.make_payment(1, 1)

    if result.is_success():
        return Response(status_code=status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.value)


def django_view(
    request: HttpRequest,
    credit_card_id: UUID4,
    amount
) -> HttpResponse:
    result = payments_facade.make_payment(credit_card_id, amount)

    if result.is_success():
        return JsonResponse(status_code=status.HTTP_200_OK, data=result.value)

    raise JsonResponse(status_code=status.HTTP_400_BAD_REQUEST, data=result.value)

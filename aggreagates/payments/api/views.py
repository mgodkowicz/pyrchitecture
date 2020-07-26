from fastapi import APIRouter, Depends, Response, HTTPException
from starlette import status

from aggreagates.payments.application.config import payments_facade
from aggreagates.payments.application.facade import PaymentsFacade

router = APIRouter()


@router.get("/payment")
def hex_view(facade: PaymentsFacade = Depends(payments_facade)):
    result = facade.make_payment(1, 1)

    if result.is_success():
        return Response(status_code=status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.value)

import hashlib
import os
from dataclasses import asdict, dataclass

import requests

from tgbotbase.utils import logger


@dataclass
class Pay2PayResponse:
    payment_id: str
    status: str
    amount: float
    usdt_amount: float
    rate: str
    order_id: str
    type: str
    bank: str
    requisites: str
    card_owner: str
    pay_url: str
    success_url: str
    created_at: str

    def dict(self):
        return asdict(self)

def get_error_code(string: object) -> str:
    return hashlib.md5(str(string).encode()).hexdigest()[:8]

class Pay2Pay:
    """
    Авторизация на всех запросах через указание апи ключа в хедере x-api-key
    """

    def __init__(self, uuid: str, token: str):
        self.uuid = uuid
        self.token = token
        self.headers = {
            "uuid": self.uuid,
            "token": self.token,
            "user-agent": "Python 3.10.0 / TradeOnAcc",
        }
        self.requester = requests.Session()
        self.requester.headers = self.headers

        self.fatal_error_count = 0

    def catch_error(self) -> callable:
        self.fatal_error_count += 1
        if self.fatal_error_count <= 1:
            logfunc = logger.exception
        else:
            logfunc = logger.error
        
        return logfunc

    
    def create_order(self, amount: float, sbp: bool, order_id: str) -> Pay2PayResponse | str:
        """
        Response example:
        {
            "data": {
                "payment_id": "01390fe8-e2ea-4be2-baa8-c3efc7df0f9f",
                "status": "created",
                "amount": 12,
                "usdt_amount": 0.1294777729823047,
                "rate": "92.68",
                "order_id": "order-32-34",
                "type": "card",
                "bank": "Сбербанк",
                "requisites": "4444 4444 4444 4444",
                "card_owner": "Ivan Ivanov",
                "pay_url": "https://pay.pay2pay.io/pay/01390fe8-e2ea-4be2-baa8-c3efc7df0f9f",
                "success_url": "https://pay.pay2pay.io/success/01390fe8-e2ea-4be2-baa8-c3efc7df0f9f",
                "created_at": "2023-01-01T00:00:00.000Z"
            }
        }
        """

        try:
            response = self.requester.post(
                url = "https://gate.pay2pay.io/api/create-order",
                json = {
                    "amount": amount, 
                    "sbp": sbp, 
                    "order_id": order_id
                }
            )
            logger.debug(f"Request create_order Pay2Pay API: {amount=} {sbp=} {order_id=}| {response.status_code=} | {response.text=}")

            data: dict = response.json()

            if data.get("error"):
                logger.error(f"Error create_order Pay2Pay API: {amount=} {sbp=} {order_id=}| {response.status_code=} | {response.text=}")
                return get_error_code(response.text)

            return Pay2PayResponse(**data["data"])

        except Exception as e:
            logfunc = self.catch_error()
            logfunc(f"Fatal error create_order Pay2Pay API: {amount=} {sbp=} {order_id=}| {e=}")
            return get_error_code(e)

    def check_order(self, payment_id: str) -> Pay2PayResponse:
        """
        Response example:
        {
            "data": {
                "payment_id": "01390fe8-e2ea-4be2-baa8-c3efc7df0f9f",
                "status": "created",
                "amount": "12",
                "usdt_amount": "0.1294777729823",
                "rate": "92.68",
                "order_id": "order-32-34",
                "type": "card",
                "bank": "Сбербанк",
                "requisites": "4444 4444 4444 4444",
                "card_owner": "Ivan Ivanov",
                "success_url": "https://pay.pay2pay.io/success/01390fe8-e2ea-4be2-baa8-c3efc7df0f9f",
                "pay_url": "https://pay.pay2pay.io/pay/01390fe8-e2ea-4be2-baa8-c3efc7df0f9f"
            }
        }
        """
        try:
            response = self.requester.get(f"https://gate.pay2pay.io/api/check-order/{payment_id}")
            logger.debug(f"Request check_order Pay2Pay API: {payment_id=}| {response.status_code=} | {response.text=}")

            data: dict = response.json()

            if data.get("error"):
                logger.error(f"Error check_order Pay2Pay API: {payment_id=}| {response.status_code=} | {response.text=}")
                return get_error_code(response.text)

            return Pay2PayResponse(**data["data"])
        
        except Exception as e:
            logfunc = self.catch_error()
            logfunc(f"Fatal error check_order Pay2Pay API: {payment_id=}| {e=}")
            return get_error_code(e)


PAY2PAY_TOKEN = os.getenv("PAY2PAY_TOKEN")
PAY2PAY_UUID = os.getenv("PAY2PAY_UUID")
if PAY2PAY_TOKEN is None or PAY2PAY_UUID is None:
    logger.critical(f"[Pay2PaySDK init error] PAY2PAY_TOKEN or PAY2PAY_UUID is None | {PAY2PAY_TOKEN=}, {PAY2PAY_UUID=}")

Pay2PaySDK = Pay2Pay(PAY2PAY_UUID, PAY2PAY_TOKEN)

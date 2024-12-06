from aiogram.filters.callback_data import CallbackData
from aiogram.filters.state import State, StatesGroup


class CallbackFactory(CallbackData, prefix="kb"):
    action: str


class UserCallbackFactory(CallbackData, prefix="ukb"):
    action: str
    user_id: int


class ModerationCallbackFactory(CallbackData, prefix="mod"):
    action: str
    room_message_id: int


class ProductPartFactory(CallbackData, prefix="part"):
    action: str  # select | back
    selection: int
    session: str


class MultiKeyboardFactory(CallbackData, prefix="mk"):
    action: str  # select | back
    page: int
    item_selected: int
    kb_session: str


class StateFactory:
    class RedeemPromoState(StatesGroup):
        input_code: State = State()

    class YooMoneyAmountState(StatesGroup):
        amount: State = State()

    class InputRefCodeState(StatesGroup):
        input_code: State = State()

    class InputRefAmountState(StatesGroup):
        amount: State = State()

    class InputCount(StatesGroup):
        count: State = State()

    class AskQuestion(StatesGroup):
        value: State = State()

    class AnswerQuestion(StatesGroup):
        value: State = State()

    class Mailing(StatesGroup):
        value: State = State()

    class ModerationComment(StatesGroup):
        value: State = State()

    class OrderExtraData(StatesGroup):
        value: State = State()

    class ScheduleOrder(StatesGroup):
        time_to: State = State()
        time_from: State = State()

    class OrderDeadline(StatesGroup):
        start: State = State()
        end: State = State()

    class NotFoundNeeded(StatesGroup):
        value: State = State()

    class InputFiatAmount(StatesGroup):
        value: State = State()

    class InputLogins(StatesGroup):
        count: State = State()

    class Upload(StatesGroup):
        value: State = State()
        self_cost: State = State()

    class InputAmountTopUp(StatesGroup):
        value: State = State()


class ExceptionFactory:
    class DateTimeExpired(Exception):
        pass

from todos.common.message_bus import MessageBus
from todos.services.accounts.domain.entities import User
from todos.services.accounts.domain.ports import AbstractUnitOfWork


class Service:
    def __init__(self, *, bus: MessageBus, uow: AbstractUnitOfWork):
        self._bus = bus
        self._uow = uow

    def register_user(self, *, email: str, password: str) -> int:
        with self._uow as uow:
            user = User(email=email, password=password)
            uow.repository.create(user)
            uow.commit()

            self._bus.dispatch(User.AccountCreatedEvent(user_id=user.id))

            return user.id
import uuid

from btypes.user import User
from btypes.errors import FullChatException, UserIsNotSuitableError


class Chat:
    MIN_NUMBER_OF_USERS = 1
    MAX_NUMBER_OF_USERS = 2

    def __init__(self, users: list[User] = list):
        self.id = uuid.uuid4()
        self.__started = False
        self.users = list[User]()
        for user in users:
            self.append_user(user)

    def append_user(self, user: User) -> None:
        if self.is_full():
            raise FullChatException
        elif not self.is_suitable_for_user(user):
            raise UserIsNotSuitableError

        self.users.append(user)
        self.__started = self.is_full()

    def remove_user(self, user_id: int) -> None:
        self.users = list(filter(lambda user: user.user_id != user_id, self.users))

    def is_full(self) -> bool:
        return len(self.users) >= self.MAX_NUMBER_OF_USERS

    def is_suitable_for_user(self, user: User) -> bool:
        if len(self.users) != 0:
            chat_user = self.users[0]
            if not chat_user.is_suitable_age(user):
                return False
            elif not chat_user.is_suitable_city(user):
                return False
            elif not chat_user.is_suitable_sex(user):
                return False
        elif self.is_full():
            return False
        return True

    @property
    def started(self) -> bool:
        return self.__started

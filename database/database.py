from typing import Optional
from abc import abstractmethod, ABC

from btypes.user import User


class Database(ABC):
    """
    A class from which any database must be inherited.
    """

    @abstractmethod
    def save_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

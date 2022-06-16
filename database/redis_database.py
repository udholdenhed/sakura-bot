from typing import Optional
from redis import Redis, RedisError

from btypes.user import User
from database.database import Database


class RedisDatabase(Database):
    """
    A class representing the redis database.
    """

    __USER_PREFIX = 'USER_'

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, password: str = ''):
        self.redis = Redis(host=host, port=port, db=db, password=password)

    def save_user(self, user: User) -> bool:
        """
        Saves the user to the database.
        Args:
            user: User variable that will be saved to the database.

        Returns:
            Returns true if the user was successfully saved in the database.
        """

        j = user.to_json()
        key = self.__create_user_key(user.user_id)

        result = self.redis.set(key, j)
        if result is None:
            raise RedisError()

        return result

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Args:
            user_id: User ID, by which it can be retrieved from the database.

        Returns:
            Returns the user if he is in the database otherwise None.
        """

        key = self.__create_user_key(user_id)
        j = self.redis.get(key)
        if j is None:
            return None

        return User.from_json(j)

    @classmethod
    def __create_user_key(cls, user_id: int) -> str:
        return cls.__USER_PREFIX + str(user_id)

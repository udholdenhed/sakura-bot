from typing import Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class User:
    user_id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    user_age: Optional[str]
    user_city: Optional[str]
    user_sex: Optional[str]
    interlocutor_age: Optional[str]
    interlocutor_city: Optional[str]
    interlocutor_sex: Optional[str]

    def __int__(self,
                user_id: int,
                first_name: str,
                last_name: Optional[str] = Optional[None](),
                username: Optional[str] = Optional[None](),
                user_age: Optional[str] = Optional['not_specified'],
                user_city: Optional[str] = Optional['not_specified'],
                user_sex: Optional[str] = Optional['not_specified'],
                interlocutor_age: Optional[str] = Optional['not_specified'],
                interlocutor_city: Optional[str] = Optional['not_specified'],
                interlocutor_sex: Optional[str] = Optional['not_specified']):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.user_age = user_age
        self.user_city = user_city
        self.interlocutor_age = interlocutor_age
        self.interlocutor_city = interlocutor_city

    def is_suitable_age(self, user: 'User') -> bool:
        return \
            user.interlocutor_age == self.user_age and self.interlocutor_age == user.user_age or \
            user.interlocutor_age == 'not_specified' and self.interlocutor_age == user.user_age or \
            user.interlocutor_age == self.user_age and self.interlocutor_age == 'not_specified'

    def is_suitable_city(self, user: 'User'):
        return \
            user.interlocutor_city == self.user_city and self.interlocutor_city == user.user_city or \
            user.interlocutor_city == 'not_specified' and self.interlocutor_city == user.user_city or \
            user.interlocutor_city == self.user_city and self.interlocutor_city == 'not_specified'

    def is_suitable_sex(self, user: 'User'):
        return \
            user.interlocutor_sex == self.user_sex and self.interlocutor_sex == user.user_sex or \
            user.interlocutor_sex == 'not_specified' and self.interlocutor_sex == user.user_sex or \
            user.interlocutor_sex == self.user_sex and self.interlocutor_sex == 'not_specified'

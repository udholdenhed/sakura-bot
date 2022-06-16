from typing import Optional

from btypes.chat import Chat
from btypes.user import User


class Chats:
    def __init__(self):
        self.chats = list()

    def append_chat(self, chat: Chat) -> None:
        self.chats.append(chat)

    def remove_chat(self, chat_id: int) -> None:
        self.chats = list(filter(lambda chat: chat.id != chat_id, self.chats))

    def suitable_chat(self, user: User) -> Optional[Chat]:
        for chat in self.chats:
            if chat.is_suitable_for_user(user):
                return chat
        return None

    def user_chat(self, user_id: int) -> Optional[Chat]:
        for chat in self.chats:
            for user in chat.users:
                if user.user_id == user_id:
                    return chat
        return None

class Chatroom:
    chatroomNextId = 1

    def __init__(self, chatroom_name):
        self.chatroom_name = chatroom_name
        self.chatroom_id = self.chatroomNextId
        self.chatroomNextId += 1
        self.joins = []

    def findOrDefaultJoinInChatroom(self, searched_join):
        for chatroom_join in self.joins:
            if chatroom_join == searched_join:
                return chatroom_join
        return None

    def removeIfExistsJoinInChatroom(self, to_remove_join):
        join = self.findOrDefaultJoinInChatroom(to_remove_join)
        if join is not None:
            self.removeExistingJoinInChatroom(join)

    def removeExistingJoinInChatroom(self, to_remove_join):
        self.joins.remove(to_remove_join)


def findOrDefaultChatroomByName(chatroom_name, chatrooms):
    for chatroom in chatrooms:
        if chatroom.chatroom_name == chatroom_name:
            return chatroom
    return None


def findOrDefaultChatroomById(chatroom_id, chatrooms):
    for chatroom in chatrooms:
        if chatroom.chatroom_id == chatroom_id:
            return chatroom
    return None


def findOrCreateChatroomByName(chatroom_name, chatrooms):
    chatroom = findOrDefaultChatroomByName(chatroom_name, chatrooms)
    if chatroom is None:
        chatroom = Chatroom(chatroom_name)
        chatrooms.append(chatroom)
    return chatroom



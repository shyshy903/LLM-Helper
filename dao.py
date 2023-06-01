import os
import config
import pickle
from LRU_cache import LRUCache


class ChatRecord:
    all_user_dict = {}
    '''
    {"user_id": {
        "session_id": {
            "span_id: { 
                "request": ""
                "answer": ""
                }
            }
        }
    }
    '''
    user_dict_file = ""

    def __int__(self):
        self.user_dict_file = config.USER_DICT_FILE
        if os.path.exists(self.user_dict_file):
            with open(self.user_dict_file, "rb") as pickle_file:
                self.all_user_dict = pickle.load(pickle_file)
                self.all_user_dict.change_capacity(config.USER_SAVE_MAX)
        else:
            with open(self.user_dict_file, "wb") as pickle_file:
                pickle.dump(self.user_dict_file, pickle_file)
        if self.all_user_dict is None or not isinstance(self.all_user_dict, LRUCache):
            self.all_user_dict = LRUCache(config.USER_SAVE_MAX)

    def insert(self, user_id, session_id, span_id, request, answer):
        self.check_user(user_id)
        self.check_session(user_id, session_id)
        self.check_span(user_id, session_id, span_id)
        self.all_user_dict[user_id][session_id][span_id]['request'] = request
        self.all_user_dict[user_id][session_id][span_id]['answer'] = answer

    def check_span(self, user_id, session_id, span_id):
        span_info = self.get_span_id(user_id, session_id, span_id)
        if span_info is None:
            self.insert_span_info(user_id, session_id, span_id)

    def insert_span_info(self,user_id, session_id, span_id):
        self.all_user_dict[user_id][session_id][span_id] = {}

    def check_session(self, user_id, session_id):
        session_info = self.get_session_info(user_id, session_id)
        if session_info is None:
            self.insert_session_info(user_id, session_id)

    def insert_session_info(self, user_id, session_id):
        self.all_user_dict[user_id][session_id] = {}

    def check_user(self, user_id):
        user_info = self.get_user_info(user_id)
        # print(user_info)
        if user_info is None:
            self.insert_user_info(user_id)

    def insert_user_info(self, user_id):
        self.all_user_dict[user_id] = {}
        print(self.all_user_dict)

    def get_user_info(self, user_id):
        user_info = self.all_user_dict.get(user_id)
        return user_info

    def get_session_info(self, user_id, session_id):
        session_info = self.get_user_info(user_id).get(session_id)
        return session_info

    def get_span_id(self, user_id, session_id, span_id):
        span_info = self.get_session_info(user_id, session_id).get(span_id)
        return span_info

chat_record = ChatRecord()

if __name__ == "__main__":
    chat_record.check_user("123")
    print(chat_record.all_user_dict)
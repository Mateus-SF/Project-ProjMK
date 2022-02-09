class Notification:
    __slots__ = '__valid', '__message'

    def __init__(self):
        self.__valid = False
        self.__message = 'Empty notification'

    def set_valid(self, value):
        self.__valid = value

    def add_message(self, value):
        self.__message = self.__message + '; ' + value

    def set_message(self, value):
        self.__message = value

    def __bool__(self):
        return self.__valid

    def __str__(self):
        return self.__message
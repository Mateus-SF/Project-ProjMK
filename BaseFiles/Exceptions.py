class InvalidProjectType(Exception):
    def __init__(self, obj_name='', message=None):
        if message:
            print(message)
        else:
            print(f'\'{obj_name}\'', 'is not a valid project type')
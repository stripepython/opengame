class OpenGameError(RuntimeError):
    pass


class OpenGameWarning(Warning):
    pass


not_created_window = OpenGameError('did not create a window')

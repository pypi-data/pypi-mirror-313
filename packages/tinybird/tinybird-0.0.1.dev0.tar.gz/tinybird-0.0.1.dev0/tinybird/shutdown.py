class ShutdownApplicationStatus:
    _application_exiting = False

    @classmethod
    def is_application_exiting(cls):
        return cls._application_exiting

    @classmethod
    def mark_application_as_exiting(cls):
        cls._application_exiting = True

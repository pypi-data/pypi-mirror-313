import contextvars

engine_dict = contextvars.ContextVar("engine_dict", default=None)

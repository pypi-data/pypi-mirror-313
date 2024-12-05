class McaiLogsHandler(Handler):
    def __init__(self, level=0):
        super().__init__(level=level)

    def emit(self, record):
        bind_logs_to_rust(record)

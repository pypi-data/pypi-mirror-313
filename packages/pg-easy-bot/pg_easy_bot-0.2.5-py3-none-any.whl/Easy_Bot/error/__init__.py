class NoHandler(Exception):
    def __init__(self, message="No Handlers found , please set handlers to start bot"):
        self.message = message
        super().__init__(self.message)

class UnauthorizedCommandError(Exception):
    def __init__(self, message="Unauthorized command detected! You do not have permission to use this command."):
        self.message = message
        super().__init__(self.message)

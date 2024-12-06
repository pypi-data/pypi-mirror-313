class ConfigurationError(Exception):
    """Exception raised for configuration-related errors.
    
    Attributes:
        message -- explanation of the error
        config -- configuration that caused the error (optional)
    """

    def __init__(self, message: str, config: dict = None) -> None:
        self.message = message
        self.config = config
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.config:
            return f"{self.message} (Config: {self.config})"
        return self.message
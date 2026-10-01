"""Domain errors. main.py maps each one to an HTTP status code."""


class DomainError(Exception):
    pass


class DeviceNotFound(DomainError):
    def __init__(self, device_id: int):
        super().__init__(f"Device {device_id} not found")


class DuplicateDeviceName(DomainError):
    def __init__(self, name: str):
        super().__init__(f"Device name '{name}' already exists")


class InvalidCredentials(DomainError):
    def __init__(self):
        super().__init__("Invalid username or password")


class Unauthorized(DomainError):
    def __init__(self):
        super().__init__("Not authenticated")

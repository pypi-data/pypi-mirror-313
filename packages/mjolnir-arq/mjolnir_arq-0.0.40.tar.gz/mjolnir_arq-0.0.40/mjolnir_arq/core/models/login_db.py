class LoginDB:
    def __init__(
        self, name_db: str, name_user: str, password: str, port: str, host: str, scheme: str
    ) -> None:
        self.name_db = name_db
        self.name_user = name_user
        self.password = password
        self.port = port
        self.host = host
        self.scheme = scheme

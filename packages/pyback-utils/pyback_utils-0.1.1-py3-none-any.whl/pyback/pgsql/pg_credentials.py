from dataclasses import dataclass


@dataclass
class PGCredentials:
    username: str
    password: str
    database: str
    host: str
    port: int

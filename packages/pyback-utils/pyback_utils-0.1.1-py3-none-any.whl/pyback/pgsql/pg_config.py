from dataclasses import asdict, dataclass


@dataclass
class PGConfig:
    pool_size: int = 20
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 18000

    def to_dict(self) -> dict:
        return asdict(self)

from dataclasses import dataclass, asdict


@dataclass
class RecordBase:
    def as_dict(self):
        return asdict(self)

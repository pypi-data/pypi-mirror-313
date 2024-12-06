from dataclasses import dataclass, asdict
import json


@dataclass(kw_only=True)
class ApiBaseModel:
    def to_dict(self):
        return asdict(self)

    def to_json(self, indent=0):
        return json.dumps(self.to_dict(), indent=indent)

    def __str__(self):
        return self.to_json(indent=2)


__all__ = [ApiBaseModel]

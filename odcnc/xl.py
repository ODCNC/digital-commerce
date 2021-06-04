import re
from dataclasses import dataclass

HYPERLINK_EXP = re.compile(r'=HYPERLINK\("(.+)",\s*"(.+)"\)')


@dataclass
class Hyperlink:
    url: str
    label: str

    def __json__(self):
        return self.hyperlink

    def __str__(self) -> str:
        return self.hyperlink

    @property
    def hyperlink(self):
        return f'=HYPERLINK("{self.url}","{self.label}")'

    @staticmethod
    def parse(string):
        match = HYPERLINK_EXP.match(string or '')
        return match and Hyperlink(match.group(1), match.group(2))

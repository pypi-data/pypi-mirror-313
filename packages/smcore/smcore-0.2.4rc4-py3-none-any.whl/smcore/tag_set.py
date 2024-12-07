# TagSet implements our matching logic for message tags
from typing import Iterable


class TagSet:
    def __init__(self, *tags):
        final_tags = set()
        for tag in tags:
            final_tags.add(tag)

        self.tags = final_tags

    def matches(self, incoming) -> bool:
        if len(self.tags) > len(incoming.tags):
            return False

        if len(self.tags) == 0:
            return True

        for tag in self.tags:
            if tag not in incoming.tags:
                return False
        return True

    def __str__(self):
        tag_str = ", ".join(self.tags)

        return "{" + tag_str + "}"

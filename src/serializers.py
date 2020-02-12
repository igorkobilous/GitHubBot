from .inputs import SearchInput
from .core import InputSerializer


class SearchSerializer(InputSerializer):

    @staticmethod
    def load(data):
        return SearchInput(**data)

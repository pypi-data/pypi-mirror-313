from typing import Type, get_type_hints, Any

from buz.query import Query
from buz.query.synchronous.query_handler import QueryHandler


class BaseQueryHandler(QueryHandler):
    @classmethod
    def fqn(cls) -> str:
        return f"query_handler.{cls.__module__}.{cls.__name__}"

    @classmethod
    def handles(cls) -> Type[Query]:
        handle_types = get_type_hints(cls.handle)

        if "query" not in handle_types:
            raise TypeError(
                f"The method 'handle' in '{cls.fqn()}' doesn't have a parameter named 'query'. Found parameters: {cls.__get_method_parameter_names(handle_types)}"
            )

        if not issubclass(handle_types["query"], Query):
            raise TypeError(f"The parameter 'query' in '{cls.fqn()}.handle' is not a 'buz.query.Query' subclass")

        return handle_types["query"]

    @classmethod
    def __get_method_parameter_names(cls, handle_types: dict[str, Any]) -> list[str]:
        handle_types_copy: dict = handle_types.copy()
        handle_types_copy.pop("return", None)
        return list(handle_types_copy.keys())

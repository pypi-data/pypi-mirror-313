from typing import Any


def model_dump(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore[no-untyped-def]  # noqa: ARG001
    kwargs['exclude_none'] = True

    return super().model_dump(**kwargs)  # type: ignore[misc]


def model_dump_json(self, **kwargs: Any) -> str:  # type: ignore[no-untyped-def]  # noqa: ARG001
    kwargs['exclude_none'] = True

    return super().model_dump_json(**kwargs)  # type: ignore[misc]

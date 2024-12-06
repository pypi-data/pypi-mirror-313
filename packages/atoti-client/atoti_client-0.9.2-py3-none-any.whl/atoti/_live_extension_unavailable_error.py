from typing import final


@final
class LiveExtensionUnavailableError(RuntimeError):
    def __init__(self) -> None:
        super().__init__(
            "Live extension is not available on this session. See `Session.connect()`'s documentation for more information.",
        )

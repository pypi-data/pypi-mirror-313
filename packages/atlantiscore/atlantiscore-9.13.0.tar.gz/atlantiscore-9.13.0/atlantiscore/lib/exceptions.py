class InvalidByteEncoding(RuntimeError):
    def __init__(self, invalid_value: any) -> None:
        super().__init__(
            f"{invalid_value} is not transformable to a valid byte sequence."
        )


class InvalidEVMAddress(InvalidByteEncoding):
    def __init__(self, invalid_value: any) -> None:
        super().__init__(invalid_value)
        self.args = (f"{invalid_value} is not transformable to a valid EVM address.",)


class InvalidEVMTransactionHash(InvalidByteEncoding):
    def __init__(self, invalid_value: any) -> None:
        super().__init__(invalid_value)
        self.args = (
            f"{invalid_value} is not transformable to a valid EVM transaction hash.",
        )

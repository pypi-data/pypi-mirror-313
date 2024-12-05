import json
from pathlib import Path

import aiofiles


async def read_abi(name: str, parent_path: Path | None = None) -> dict:
    if not parent_path:
        parent_path = Path(__file__).parent
    path = parent_path / f"{name}.abi"
    async with aiofiles.open(path, mode="r") as file:
        return json.loads(await file.read())

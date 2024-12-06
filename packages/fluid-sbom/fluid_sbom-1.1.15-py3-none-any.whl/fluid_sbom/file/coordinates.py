from pydantic import (
    BaseModel,
)


class Coordinates(BaseModel):
    real_path: str
    file_system_id: str | None = None
    line: int | None = None

    def __str__(self) -> str:
        result = f"RealPath={self.real_path}"
        if self.file_system_id:
            result += f" Layer={self.file_system_id}"
        return f"Location<{result}>"

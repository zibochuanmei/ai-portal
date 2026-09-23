from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.auth.service import UserContext
from app.core.config import get_settings
from app.core.errors import ApiError


@dataclass(frozen=True)
class StoredFile:
    file_id: str
    owner_id: str
    filename: str
    content_type: str
    size: int
    path: Path


class FileService:
    """Safe local development storage; production will swap this for MinIO."""

    def __init__(self) -> None:
        settings = get_settings()
        self.root = Path(settings.file_storage_dir)
        self.root.mkdir(parents=True, exist_ok=True)
        self.max_bytes = settings.file_max_size_mb * 1024 * 1024
        self.allowed_extensions = set(settings.allowed_file_extension_list)
        self._files: dict[str, StoredFile] = {}

    async def store(self, user: UserContext, upload: UploadFile) -> StoredFile:
        filename = Path(upload.filename or "").name
        extension = Path(filename).suffix.lower().lstrip(".")
        if not filename or extension not in self.allowed_extensions:
            raise ApiError(415, "FILE_TYPE_NOT_ALLOWED", "文件类型不在允许范围内")

        content = await upload.read(self.max_bytes + 1)
        if len(content) > self.max_bytes:
            raise ApiError(413, "FILE_TOO_LARGE", "文件超过大小限制")

        file_id = str(uuid4())
        path = self.root / f"{file_id}.{extension}"
        path.write_bytes(content)
        stored = StoredFile(
            file_id=file_id,
            owner_id=user.id,
            filename=filename,
            content_type=upload.content_type or "application/octet-stream",
            size=len(content),
            path=path,
        )
        self._files[file_id] = stored
        return stored

    def require_owned(self, user: UserContext, file_id: str) -> StoredFile:
        stored = self._files.get(file_id)
        if stored is None or stored.owner_id != user.id:
            raise ApiError(404, "FILE_NOT_FOUND", "文件不存在或无权访问")
        return stored


file_service = FileService()

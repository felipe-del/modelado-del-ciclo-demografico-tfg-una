from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from ..errors import ArchiveError


@dataclass(frozen=True)
class ArchiveContent:
    source_file: Path
    member_name: str
    source_sha256: str
    member_sha256: str
    data: bytes

    def lines(self, encoding: str) -> list[str]:
        return self.data.decode(encoding).splitlines()


def open_source(path: Path) -> ArchiveContent:
    if not path.is_file():
        raise ArchiveError("El archivo fuente no existe")
    source_data = path.read_bytes()
    source_digest = sha256(source_data).hexdigest()
    if path.suffix.lower() == ".txt":
        return ArchiveContent(path, path.name, source_digest, source_digest, source_data)
    if path.suffix.lower() != ".zip":
        raise ArchiveError("La fuente debe ser ZIP o TXT")
    try:
        with ZipFile(path) as archive:
            members = [item for item in archive.infolist() if not item.is_dir() and item.filename.lower().endswith(".txt")]
            if not members:
                raise ArchiveError("El ZIP no contiene un archivo TXT")
            member = members[0]
            data = archive.read(member)
    except (BadZipFile, OSError) as exc:
        raise ArchiveError("La fuente ZIP no es valida") from exc
    return ArchiveContent(path, member.filename, source_digest, sha256(data).hexdigest(), data)
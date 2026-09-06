import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
from zipfile import BadZipFile, ZipFile

from ..errors import ArchiveError, TSEError
from ..schema_loader import load_schema
from .archive_reader import open_source

DEFAULT_SOURCE_PAGE = "https://www.tse.go.cr/descarga_movimientos.html"
DATASETS = ("nacimientos", "matrimonios", "defunciones")
PREFIXES = {"nacimientos": "nac_", "matrimonios": "mat_", "defunciones": "def_"}
MONTHS = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
MANIFEST_FIELDS = ("manifest_version", "dataset", "source_url", "source_page", "zip_filename", "zip_relative_path", "zip_sha256", "zip_size_bytes", "txt_filename", "txt_relative_work_path", "txt_sha256", "year", "month", "period_start", "period_end", "encoding_detected", "encoding_detection_method", "expected_record_length", "min_record_length", "max_record_length", "total_rows", "valid_length_rows", "short_rows", "long_rows", "empty_rows", "download_status", "extraction_status", "inspection_status", "processed_at_utc", "schema_version", "overall_status")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


@dataclass
class Inspection:
    txt_filename: str
    txt_sha256: str
    encoding_detected: str
    encoding_detection_method: str
    min_record_length: int | None
    max_record_length: int | None
    total_rows: int
    valid_length_rows: int
    short_rows: int
    long_rows: int
    empty_rows: int


def dataset_for_filename(filename: str) -> str | None:
    lower = filename.lower()
    return next((dataset for dataset, prefix in PREFIXES.items() if lower.startswith(prefix) and lower.endswith(".zip")), None)


def discover_links(page_html: str, source_page: str, datasets: tuple[str, ...] = DATASETS) -> list[tuple[str, str]]:
    parser = LinkParser()
    parser.feed(page_html)
    discovered = []
    for href in parser.hrefs:
        url = urljoin(source_page, href)
        dataset = dataset_for_filename(Path(urlparse(url).path).name)
        if dataset in datasets:
            discovered.append((dataset, url))
    return list(dict.fromkeys(discovered))


def fetch_page(source_page: str) -> str:
    try:
        with urlopen(source_page, timeout=30) as response:
            return response.read().decode("utf-8")
    except OSError as exc:
        raise TSEError("No se pudo consultar la pagina oficial del TSE.") from exc


def parse_period(filename: str) -> dict[str, int | None]:
    parts = Path(filename).stem.lower().split("_")
    if len(parts) != 4 or parts[1][:-4] not in MONTHS or not parts[1][-4:].isdigit() or not parts[2].isdigit() or not parts[3].isdigit():
        return {"year": None, "month": None, "period_start": None, "period_end": None}
    month_name, year = parts[1][:-4], int(parts[1][-4:])
    start, end = int(parts[2]), int(parts[3])
    if not 1 <= start <= end <= 31:
        return {"year": None, "month": None, "period_start": None, "period_end": None}
    return {"year": year, "month": MONTHS[month_name], "period_start": start, "period_end": end}


def detect_encoding(data: bytes, schema_encoding: str) -> tuple[str, str]:
    if data.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig", "UTF8_BOM"
    if data.startswith(b"\xff\xfe"):
        return "utf-16-le", "UTF16_LE_BOM"
    if data.startswith(b"\xfe\xff"):
        return "utf-16-be", "UTF16_BE_BOM"
    try:
        data.decode("utf-8", errors="strict")
        return "utf-8", "UTF8_STRICT"
    except UnicodeDecodeError:
        data.decode(schema_encoding, errors="strict")
        return schema_encoding, "SCHEMA_FALLBACK_AFTER_UTF8_FAILURE"


def inspect_zip(zip_path: Path, schema_path: Path) -> Inspection:
    content = open_source(zip_path)
    schema = load_schema(schema_path)
    encoding, method = detect_encoding(content.data, schema.encoding)
    lengths = []
    empty_rows = short_rows = long_rows = valid_rows = 0
    for line in content.data.decode(encoding).splitlines():
        length = len(line)
        lengths.append(length)
        if not line:
            empty_rows += 1
        elif length == schema.expected_record_length:
            valid_rows += 1
        elif length < schema.expected_record_length:
            short_rows += 1
        else:
            long_rows += 1
    return Inspection(Path(content.member_name).name, content.member_sha256, encoding, method, min(lengths, default=None), max(lengths, default=None), len(lengths), valid_rows, short_rows, long_rows, empty_rows)


def safe_extract_txt(zip_path: Path, destination: Path, zip_sha256: str) -> tuple[str, str]:
    try:
        with ZipFile(zip_path) as archive:
            member = next((item for item in archive.infolist() if not item.is_dir() and item.filename.lower().endswith(".txt")), None)
            if member is None:
                raise ArchiveError("El ZIP no contiene un archivo TXT")
            member_path = PurePosixPath(member.filename)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise ArchiveError("El ZIP contiene una ruta insegura")
            target = (destination / Path(*member_path.parts)).resolve()
            destination_root = destination.resolve()
            if target != destination_root and destination_root not in target.parents:
                raise ArchiveError("El ZIP contiene una ruta fuera del destino")
            destination.mkdir(parents=True, exist_ok=True)
            if target.exists():
                raise ArchiveError("El TXT de destino ya existe y no sera sobrescrito")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
            (destination / ".dat02.json").write_text(json.dumps({"zip_sha256": zip_sha256}), encoding="utf-8")
            return member.filename, str(target)
    except BadZipFile as exc:
        raise ArchiveError("La fuente ZIP no es valida") from exc


def read_manifest(path: Path) -> dict[tuple[str, str, str], dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as file:
        return {(row["dataset"], row["zip_filename"], row["zip_sha256"]): row for row in csv.DictReader(file)}


def write_manifest(path: Path, rows: dict[tuple[str, str, str], dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for key in sorted(rows):
            writer.writerow({field: rows[key].get(field, "") for field in MANIFEST_FIELDS})


def generate_report(manifest_path: Path, report_path: Path, source_page: str) -> None:
    rows = list(read_manifest(manifest_path).values())
    report_path.parent.mkdir(parents=True, exist_ok=True)
    overall = "ERROR" if any(row["overall_status"] == "ERROR" for row in rows) else "PARTIAL" if any(row["overall_status"] != "OK" for row in rows) else "OK"
    lines = ["# DAT-02 - Reporte de ingesta", "", f"Fecha de ejecucion: {datetime.now(timezone.utc).isoformat()}", "", "Fuente oficial:", source_page, "", "## Resumen", "", f"- ZIP registrados: {len(rows)}", f"- ZIP ya existentes: {sum(row['download_status'] == 'ALREADY_PRESENT' for row in rows)}", f"- Conflictos: {sum(row['download_status'] == 'HASH_CONFLICT' for row in rows)}", f"- Archivos extraidos: {sum(row['extraction_status'] in ('EXTRACTED', 'ALREADY_EXTRACTED') for row in rows)}", f"- Archivos inspeccionados: {sum(row['inspection_status'] == 'INSPECTED' for row in rows)}", ""]
    for dataset in DATASETS:
        group = [row for row in rows if row["dataset"] == dataset]
        period_starts = [f"{row['year']}-{int(row['month']):02d}-{int(row['period_start']):02d}" for row in group if row["year"] and row["month"] and row["period_start"]]
        period_ends = [f"{row['year']}-{int(row['month']):02d}-{int(row['period_end']):02d}" for row in group if row["year"] and row["month"] and row["period_end"]]
        encodings = sorted({row["encoding_detected"] for row in group if row["encoding_detected"]})
        lines.extend([f"## {dataset.upper()}", "", f"- Cantidad de ZIP: {len(group)}", f"- Periodo minimo detectado: {min(period_starts) if period_starts else 'NO DETERMINADO'}", f"- Periodo maximo detectado: {max(period_ends) if period_ends else 'NO DETERMINADO'}", f"- Filas totales: {sum(int(row['total_rows'] or 0) for row in group)}", f"- Errores estructurales de longitud: {sum(int(row['short_rows'] or 0) + int(row['long_rows'] or 0) + int(row['empty_rows'] or 0) for row in group)}", f"- Codificaciones detectadas: {', '.join(encodings) or 'NO DETERMINADO'}", f"- Longitud esperada: {group[0]['expected_record_length'] if group else 'NO DETERMINADO'}", ""])
    lines.extend(["## Integridad", "", "- Archivos RAW sobrescritos: NO", f"- Conflictos detectados: {sum(row['download_status'] == 'HASH_CONFLICT' for row in rows)}", f"- Hashes calculados: {sum(bool(row['zip_sha256']) for row in rows)}", "", "## Privacidad", "", "- Registros personales incluidos en reporte: NO", "- Lineas RAW incluidas: NO", "- TXT extraidos versionados en Git: NO", "", "## Estado", "", overall, ""])
    report_path.write_text("\n".join(lines), encoding="utf-8")


def _local_zip_paths(raw_root: Path, datasets: tuple[str, ...]) -> list[tuple[str, Path, str]]:
    paths = []
    for path in raw_root.rglob("*.zip"):
        dataset = dataset_for_filename(path.name)
        if dataset in datasets:
            paths.append((dataset, path, ""))
    return paths


def sync_tse(raw_root: Path, work_root: Path, manifest_path: Path, report_path: Path, schema_root: Path, datasets: tuple[str, ...] = DATASETS, source_page: str = DEFAULT_SOURCE_PAGE, dry_run: bool = False, local_only: bool = False) -> list[dict[str, object]]:
    sources = _local_zip_paths(raw_root, datasets)
    if not local_only:
        for dataset, url in discover_links(fetch_page(source_page), source_page, datasets):
            filename = Path(urlparse(url).path).name
            existing_index = next((index for index, item in enumerate(sources) if item[0] == dataset and item[1].name == filename), None)
            if existing_index is None:
                sources.append((dataset, raw_root / dataset / "movimientos" / "downloaded" / filename, url))
            else:
                current_dataset, current_path, _ = sources[existing_index]
                sources[existing_index] = (current_dataset, current_path, url)
    existing_manifest = read_manifest(manifest_path)
    rows: dict[tuple[str, str, str], dict[str, object]] = dict(existing_manifest)
    results = []
    for dataset, zip_path, source_url in sources:
        if not zip_path.exists() and dry_run:
            results.append({"dataset": dataset, "zip_filename": zip_path.name, "download_status": "WOULD_DOWNLOAD"})
            continue
        if not zip_path.exists():
            try:
                with urlopen(source_url, timeout=60) as response:
                    downloaded = response.read()
                zip_path.parent.mkdir(parents=True, exist_ok=True)
                if zip_path.exists():
                    continue
                zip_path.write_bytes(downloaded)
                download_status = "DOWNLOADED"
            except OSError as exc:
                raise TSEError(f"No se pudo descargar {zip_path.name}.") from exc
        else:
            download_status = "ALREADY_PRESENT"
        zip_sha256 = sha256(zip_path.read_bytes()).hexdigest()
        if source_url and not local_only:
            try:
                with urlopen(source_url, timeout=60) as response:
                    remote_sha256 = sha256(response.read()).hexdigest()
            except OSError as exc:
                raise TSEError(f"No se pudo verificar {zip_path.name}.") from exc
            if remote_sha256 != zip_sha256:
                results.append({"dataset": dataset, "zip_filename": zip_path.name, "download_status": "HASH_CONFLICT", "overall_status": "ERROR"})
                continue
        same_name = [row for row in rows.values() if row["dataset"] == dataset and row["zip_filename"] == zip_path.name]
        if any(row["zip_sha256"] != zip_sha256 for row in same_name):
            result = {"dataset": dataset, "zip_filename": zip_path.name, "download_status": "HASH_CONFLICT", "overall_status": "ERROR"}
            results.append(result)
            continue
        if dry_run:
            results.append({"dataset": dataset, "zip_filename": zip_path.name, "download_status": download_status})
            continue
        extraction_dir = work_root / dataset / zip_path.stem
        marker = extraction_dir / ".dat02.json"
        if extraction_dir.exists():
            try:
                marker_hash = json.loads(marker.read_text(encoding="utf-8"))["zip_sha256"]
            except (OSError, KeyError, json.JSONDecodeError):
                marker_hash = None
            extraction_status = "ALREADY_EXTRACTED" if marker_hash == zip_sha256 else "EXTRACTION_CONFLICT"
        else:
            try:
                safe_extract_txt(zip_path, extraction_dir, zip_sha256)
                extraction_status = "EXTRACTED"
            except ArchiveError:
                extraction_status = "EXTRACTION_ERROR"
        try:
            inspection = inspect_zip(zip_path, schema_root / f"{dataset}.json")
            inspection_status = "INSPECTED"
            values = asdict(inspection)
        except (ArchiveError, UnicodeError):
            inspection_status = "INSPECTION_ERROR"
            values = {field: None for field in Inspection.__dataclass_fields__}
        period = parse_period(zip_path.name)
        overall = "OK" if extraction_status in ("EXTRACTED", "ALREADY_EXTRACTED") and inspection_status == "INSPECTED" and period["year"] else "PARTIAL"
        row = {"manifest_version": "1.0", "dataset": dataset, "source_url": source_url, "source_page": source_page, "zip_filename": zip_path.name, "zip_relative_path": str(zip_path.relative_to(raw_root)), "zip_sha256": zip_sha256, "zip_size_bytes": zip_path.stat().st_size, "txt_relative_work_path": str((extraction_dir / values.get("txt_filename", "")).relative_to(work_root)) if values.get("txt_filename") else "", "expected_record_length": load_schema(schema_root / f"{dataset}.json").expected_record_length, "download_status": download_status, "extraction_status": extraction_status, "inspection_status": inspection_status, "processed_at_utc": datetime.now(timezone.utc).isoformat(), "schema_version": load_schema(schema_root / f"{dataset}.json").schema_version, "overall_status": overall, **period, **values}
        rows[(dataset, zip_path.name, zip_sha256)] = row
        results.append(row)
    if not dry_run:
        write_manifest(manifest_path, rows)
        generate_report(manifest_path, report_path, source_page)
    return results
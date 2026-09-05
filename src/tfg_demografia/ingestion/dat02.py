from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

EVENT_LENGTHS = {
    "NACIMIENTOS": 281,
    "MATRIMONIOS": 328,
    "DEFUNCIONES": 191,
}

MONTHS = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
}


@dataclass
class Dat02Result:
    timestamp_procesamiento: str
    institucion: str
    acontecimiento: str
    archivo_zip: str
    archivo_txt: str
    ruta_zip: str
    ruta_extraccion: str
    periodo_anio: str | None
    periodo_mes: str | None
    periodo_desde: str | None
    periodo_hasta: str | None
    periodo_original: str | None
    sha256_zip: str
    sha256_txt: str
    encoding: str
    longitud_esperada: int
    longitud_minima: int
    longitud_maxima: int
    filas_totales: int
    filas_validas: int
    filas_invalidas: int
    errores_tecnicos: list[str] = field(default_factory=list)
    estado: str = "PROCESADO"
    observaciones: str = ""
    status: str = "PROCESADO"
    file_txt: str = ""
    extraction_dir: Path | None = None
    raw_bytes: bytes = b""
    rows_total: int = 0

    def __post_init__(self):
        self.status = self.estado if self.estado else self.status
        if not self.file_txt and self.archivo_txt:
            self.file_txt = self.archivo_txt
        if self.extraction_dir is None and self.ruta_extraccion:
            self.extraction_dir = Path(self.ruta_extraccion)
        self.rows_total = self.filas_totales

    def to_manifest_record(self) -> dict[str, object]:
        payload = {
            "timestamp_procesamiento": self.timestamp_procesamiento,
            "institucion": self.institucion,
            "acontecimiento": self.acontecimiento,
            "archivo_zip": self.archivo_zip,
            "archivo_txt": self.archivo_txt,
            "ruta_zip": self.ruta_zip,
            "ruta_extraccion": self.ruta_extraccion,
            "periodo_anio": self.periodo_anio,
            "periodo_mes": self.periodo_mes,
            "periodo_desde": self.periodo_desde,
            "periodo_hasta": self.periodo_hasta,
            "periodo_original": self.periodo_original,
            "sha256_zip": self.sha256_zip,
            "sha256_txt": self.sha256_txt,
            "encoding": self.encoding,
            "longitud_esperada": self.longitud_esperada,
            "longitud_minima": self.longitud_minima,
            "longitud_maxima": self.longitud_maxima,
            "filas_totales": self.filas_totales,
            "filas_validas": self.filas_validas,
            "filas_invalidas": self.filas_invalidas,
            "errores_tecnicos": self.errores_tecnicos,
            "estado": self.estado,
            "observaciones": self.observaciones,
            "status": self.status,
            "file_txt": self.file_txt,
            "extraction_dir": str(self.extraction_dir) if self.extraction_dir else "",
            "rows_total": self.rows_total,
        }
        return payload


def detect_event_name(path: str | Path) -> str:
    text = str(path).lower()
    if "nac" in text or "nacimiento" in text:
        return "NACIMIENTOS"
    if "mat" in text or "matrimonio" in text:
        return "MATRIMONIOS"
    if "def" in text or "defuncion" in text:
        return "DEFUNCIONES"
    return "DESCONOCIDO"


def detect_event_from_zip(zip_path: Path) -> str:
    if not zip_path.exists() or zip_path.suffix.lower() != ".zip":
        return detect_event_name(zip_path)
    try:
        with ZipFile(zip_path) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                if info.filename.lower().endswith(".txt"):
                    event = detect_event_name(info.filename)
                    if event != "DESCONOCIDO":
                        return event
    except (BadZipFile, OSError):
        return detect_event_name(zip_path)
    return detect_event_name(zip_path)


def _semantic_period_from_name(name: str) -> dict[str, str | None]:
    stem = Path(name).stem.lower()
    for prefix in ("nac_", "mat_", "def_"):
        if stem.startswith(prefix):
            stem = stem[len(prefix):]
    for month_name, month_num in MONTHS.items():
        pattern = rf"{month_name}(\d{{4}})_(\d{{1,2}})_(\d{{1,2}})"
        match = __import__("re").search(pattern, stem)
        if match:
            year, from_day, to_day = match.groups()
            month_key = month_num
            return {
                "periodo_anio": year,
                "periodo_mes": month_key,
                "periodo_desde": f"{year}-{month_key}-{int(from_day):02d}",
                "periodo_hasta": f"{year}-{month_key}-{int(to_day):02d}",
                "periodo_original": f"{month_name}{year}_{int(from_day):02d}_{int(to_day):02d}",
            }
    for part in stem.split("_"):
        if not part:
            continue
        candidate = part.lower()
        if candidate in MONTHS:
            month_name = candidate
            month_num = MONTHS[candidate]
            rest = stem.split(part, 1)[1].strip("_")
            if rest:
                pieces = rest.split("_")
                if len(pieces) >= 2 and pieces[0].isdigit() and pieces[1].isdigit():
                    from_day, to_day = pieces[0], pieces[1]
                    year = next((segment for segment in pieces if segment.isdigit() and len(segment) == 4), None) or ""
                    if year:
                        return {
                            "periodo_anio": year,
                            "periodo_mes": month_num,
                            "periodo_desde": f"{year}-{month_num}-{int(from_day):02d}",
                            "periodo_hasta": f"{year}-{month_num}-{int(to_day):02d}",
                            "periodo_original": f"{month_name}{year}_{int(from_day):02d}_{int(to_day):02d}",
                        }
    return {
        "periodo_anio": None,
        "periodo_mes": None,
        "periodo_desde": None,
        "periodo_hasta": None,
        "periodo_original": None,
    }


def detect_period(zip_path: Path) -> dict[str, str | None]:
    semantic = _semantic_period_from_name(zip_path.name)
    if semantic["periodo_anio"] is not None:
        return semantic
    path_parts = [part for part in zip_path.parts if part not in {"data", "raw", "tse"}]
    year = next((segment for segment in path_parts if segment.isdigit() and len(segment) == 4), None)
    month = None
    date_block = None
    for segment in path_parts:
        if "_" in segment and any(char.isalpha() for char in segment):
            month = segment
        if "_" in segment and any(char.isdigit() for char in segment):
            if len(segment.split("_")) == 2:
                date_block = segment
    if year is None:
        return {"periodo_anio": None, "periodo_mes": None, "periodo_desde": None, "periodo_hasta": None, "periodo_original": None}
    if month is None:
        month = next((segment for segment in path_parts if segment.lower() in MONTHS), None)
    if date_block is None:
        date_block = next((segment for segment in path_parts if "_" in segment and len(segment.split("_")) == 2), None)
    from_value = None
    to_value = None
    if date_block:
        parts = date_block.split("_")
        if len(parts) == 2:
            from_value, to_value = parts[0], parts[1]
    month_num = MONTHS.get(month.lower().split("_", 1)[-1], MONTHS.get(month.lower(), None)) if isinstance(month, str) else None
    semantic_period = None
    if month and year and from_value and to_value:
        month_name = month.lower().split("_", 1)[-1]
        if month_name in MONTHS:
            semantic_period = f"{month_name}{year}_{int(from_value):02d}_{int(to_value):02d}"
    return {
        "periodo_anio": year,
        "periodo_mes": month_num,
        "periodo_desde": f"{year}-{month_num}-{int(from_value):02d}" if year and month_num and from_value else None,
        "periodo_hasta": f"{year}-{month_num}-{int(to_value):02d}" if year and month_num and to_value else None,
        "periodo_original": semantic_period or zip_path.stem,
    }


def detect_encoding(data: bytes) -> str:
    if data.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    if b"\x00" in data:
        return "utf-16"
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return "latin-1"
    if any(byte > 127 for byte in data):
        return "utf-8"
    return "latin-1"


def validate_zip_members(zip_path: Path) -> list[str]:
    if not zip_path.exists() or not zip_path.is_file():
        raise ValueError(f"ZIP_NO_EXISTE:{zip_path}")
    try:
        with ZipFile(zip_path) as archive:
            members = archive.infolist()
    except (BadZipFile, OSError) as exc:
        raise ValueError(f"ZIP_INVALIDO:{zip_path.name}") from exc
    valid_members: list[str] = []
    for info in members:
        if info.is_dir():
            continue
        normalized = PurePosixPath(info.filename)
        if info.filename.startswith("/") or ".." in normalized.parts or "\\" in info.filename or info.filename.startswith("../"):
            raise ValueError(f"ZIP_SLIP:{info.filename}")
        if info.filename.lower().endswith(".txt"):
            valid_members.append(info.filename)
    if not valid_members:
        raise ValueError(f"TXT_NO_ENCONTRADO:{zip_path.name}")
    return valid_members


def _safe_extraction_directory(zip_path: Path, extraction_root: Path) -> Path:
    event = detect_event_name(zip_path.name)
    period = detect_period(zip_path)
    if event == "DESCONOCIDO":
        event = detect_event_name(str(zip_path.parent))
    year = period["periodo_anio"] or "UNKNOWN"
    month = period["periodo_mes"] or "unknown"
    block = "/".join(filter(None, [period["periodo_desde"], period["periodo_hasta"]])) or "UNKNOWN"
    if block == "UNKNOWN" and "_" in zip_path.stem:
        parts = zip_path.stem.split("_")
        if len(parts) >= 2:
            block = f"{parts[-2]}_{parts[-1]}"
    return extraction_root / event.lower() / "movimientos" / year / month / block / zip_path.stem


def archive_member_bytes(zip_path: Path, member_name: str) -> bytes:
    with ZipFile(zip_path) as archive:
        return archive.read(member_name)


def _manifest_record_for_zip(zip_path: Path, manifest_path: Path | None) -> dict[str, object] | None:
    if manifest_path is None:
        return None
    manifest_path = Path(manifest_path)
    if not manifest_path.exists():
        return None
    zip_hash = sha256(zip_path.read_bytes()).hexdigest()
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if str(payload.get("estado") or "").upper() not in {"PROCESADO", "YA_PROCESADO"}:
            continue
        payload_hash = str(payload.get("sha256_zip") or "")
        payload_path = str(payload.get("ruta_zip") or "")
        if payload_hash and payload_hash == zip_hash:
            return payload
        if payload_path and Path(payload_path).resolve() == zip_path.resolve():
            return payload
    return None


def process_zip(zip_path: Path, extraction_root: Path, manifest_path: Path | None = None) -> Dat02Result:
    zip_path = zip_path.resolve()
    if not zip_path.exists() or not zip_path.is_file():
        raise ValueError(f"ZIP_NO_EXISTE:{zip_path}")
    zip_bytes = zip_path.read_bytes()
    sha_zip = sha256(zip_bytes).hexdigest()
    event = detect_event_from_zip(zip_path)
    period = detect_period(zip_path)
    expected_length = EVENT_LENGTHS.get(event, 0)

    manifest_record = _manifest_record_for_zip(zip_path, manifest_path)
    if manifest_record:
        previous = Dat02Result(
            timestamp_procesamiento=str(manifest_record.get("timestamp_procesamiento") or datetime.now(timezone.utc).isoformat()),
            institucion=str(manifest_record.get("institucion") or "TSE"),
            acontecimiento=str(manifest_record.get("acontecimiento") or event),
            archivo_zip=str(manifest_record.get("archivo_zip") or zip_path.name),
            archivo_txt=str(manifest_record.get("archivo_txt") or ""),
            ruta_zip=str(manifest_record.get("ruta_zip") or zip_path),
            ruta_extraccion=str(manifest_record.get("ruta_extraccion") or extraction_root),
            periodo_anio=manifest_record.get("periodo_anio") if manifest_record.get("periodo_anio") is not None else period["periodo_anio"],
            periodo_mes=manifest_record.get("periodo_mes") if manifest_record.get("periodo_mes") is not None else period["periodo_mes"],
            periodo_desde=manifest_record.get("periodo_desde") if manifest_record.get("periodo_desde") is not None else period["periodo_desde"],
            periodo_hasta=manifest_record.get("periodo_hasta") if manifest_record.get("periodo_hasta") is not None else period["periodo_hasta"],
            periodo_original=manifest_record.get("periodo_original") if manifest_record.get("periodo_original") is not None else period["periodo_original"],
            sha256_zip=str(manifest_record.get("sha256_zip") or sha_zip),
            sha256_txt=str(manifest_record.get("sha256_txt") or ""),
            encoding=str(manifest_record.get("encoding") or "latin-1"),
            longitud_esperada=int(manifest_record.get("longitud_esperada") or expected_length),
            longitud_minima=int(manifest_record.get("longitud_minima") or 0),
            longitud_maxima=int(manifest_record.get("longitud_maxima") or 0),
            filas_totales=int(manifest_record.get("filas_totales") or 0),
            filas_validas=int(manifest_record.get("filas_validas") or 0),
            filas_invalidas=int(manifest_record.get("filas_invalidas") or 0),
            errores_tecnicos=list(manifest_record.get("errores_tecnicos") or []),
            estado="YA_PROCESADO",
            observaciones="El ZIP ya fue procesado; se recuperan las métricas del manifiesto previo para conservar la trazabilidad y evitar reextracción.",
        )
        previous.status = "YA_PROCESADO"
        previous.file_txt = previous.archivo_txt
        previous.extraction_dir = Path(previous.ruta_extraccion) if previous.ruta_extraccion else None
        previous.raw_bytes = zip_bytes
        previous.rows_total = previous.filas_totales
        return previous

    try:
        members = validate_zip_members(zip_path)
    except ValueError as exc:
        result = Dat02Result(
            timestamp_procesamiento=datetime.now(timezone.utc).isoformat(),
            institucion="TSE",
            acontecimiento=event,
            archivo_zip=zip_path.name,
            archivo_txt="",
            ruta_zip=str(zip_path),
            ruta_extraccion=str(extraction_root),
            periodo_anio=period["periodo_anio"],
            periodo_mes=period["periodo_mes"],
            periodo_desde=period["periodo_desde"],
            periodo_hasta=period["periodo_hasta"],
            periodo_original=period["periodo_original"],
            sha256_zip=sha_zip,
            sha256_txt="",
            encoding="ENCODING_NO_DETERMINADO",
            longitud_esperada=expected_length,
            longitud_minima=0,
            longitud_maxima=0,
            filas_totales=0,
            filas_validas=0,
            filas_invalidas=0,
            errores_tecnicos=[str(exc).split(":", 1)[0]],
            estado=str(exc).split(":", 1)[0],
            observaciones="Archivo sin TXT válido o ZIP inválido.",
        )
        result.status = result.estado
        result.raw_bytes = zip_bytes
        result.file_txt = result.archivo_txt
        result.extraction_dir = Path(result.ruta_extraccion) if result.ruta_extraccion else None
        result.rows_total = result.filas_totales
        return result

    selected_name = members[0]
    extraction_dir = _safe_extraction_directory(zip_path, extraction_root)
    extraction_dir.mkdir(parents=True, exist_ok=True)
    member_bytes = archive_member_bytes(zip_path, selected_name)
    txt_path = extraction_dir / Path(selected_name).name

    if txt_path.exists():
        existing_hash = sha256(txt_path.read_bytes()).hexdigest()
        if existing_hash == sha256(member_bytes).hexdigest():
            result = Dat02Result(
                timestamp_procesamiento=datetime.now(timezone.utc).isoformat(),
                institucion="TSE",
                acontecimiento=event,
                archivo_zip=zip_path.name,
                archivo_txt=txt_path.name,
                ruta_zip=str(zip_path),
                ruta_extraccion=str(extraction_dir),
                periodo_anio=period["periodo_anio"],
                periodo_mes=period["periodo_mes"],
                periodo_desde=period["periodo_desde"],
                periodo_hasta=period["periodo_hasta"],
                periodo_original=period["periodo_original"],
                sha256_zip=sha_zip,
                sha256_txt=existing_hash,
                encoding=detect_encoding(txt_path.read_bytes()),
                longitud_esperada=expected_length,
                longitud_minima=0,
                longitud_maxima=0,
                filas_totales=0,
                filas_validas=0,
                filas_invalidas=0,
                estado="YA_PROCESADO",
                observaciones="El ZIP ya fue procesado y el contenido extraído coincide con el hash del RAW.",
            )
            result.status = result.estado
            result.file_txt = result.archivo_txt
            result.extraction_dir = Path(result.ruta_extraccion)
            result.raw_bytes = zip_bytes
            result.rows_total = result.filas_totales
            return result

    selected_txt = extraction_dir / Path(selected_name).name
    if len(members) > 1:
        warnings = ["MULTIPLES_TXT"]
    else:
        warnings = []

    if not selected_txt.exists():
        with ZipFile(zip_path) as archive:
            for info in archive.infolist():
                if info.is_dir() or not info.filename.lower().endswith(".txt"):
                    continue
                normalized = PurePosixPath(info.filename)
                if info.filename.startswith("/") or ".." in normalized.parts or "\\" in info.filename:
                    raise ValueError(f"ZIP_SLIP:{info.filename}")
                target = extraction_dir / Path(info.filename).name
                with archive.open(info) as src, open(target, "wb") as dst:
                    dst.write(src.read())
                selected_txt = target
                break

    if not selected_txt.exists():
        result = Dat02Result(
            timestamp_procesamiento=datetime.now(timezone.utc).isoformat(),
            institucion="TSE",
            acontecimiento=event,
            archivo_zip=zip_path.name,
            archivo_txt="",
            ruta_zip=str(zip_path),
            ruta_extraccion=str(extraction_dir),
            periodo_anio=period["periodo_anio"],
            periodo_mes=period["periodo_mes"],
            periodo_desde=period["periodo_desde"],
            periodo_hasta=period["periodo_hasta"],
            periodo_original=period["periodo_original"],
            sha256_zip=sha_zip,
            sha256_txt="",
            encoding="ENCODING_NO_DETERMINADO",
            longitud_esperada=expected_length,
            longitud_minima=0,
            longitud_maxima=0,
            filas_totales=0,
            filas_validas=0,
            filas_invalidas=0,
            errores_tecnicos=["TXT_NO_ENCONTRADO"],
            estado="TXT_NO_ENCONTRADO",
            observaciones="No se encontró un TXT válido dentro del ZIP.",
        )
        result.status = result.estado
        result.file_txt = result.archivo_txt
        result.extraction_dir = Path(result.ruta_extraccion) if result.ruta_extraccion else None
        result.raw_bytes = zip_bytes
        result.rows_total = result.filas_totales
        return result

    txt_bytes = selected_txt.read_bytes()
    encoding = detect_encoding(txt_bytes)
    text = txt_bytes.decode(encoding)
    lines = [line.rstrip("\r\n") for line in text.splitlines() if line.strip()]
    rows_total = len(lines)
    if expected_length:
        valid_rows = sum(1 for line in lines if len(line) == expected_length)
        invalid_rows = rows_total - valid_rows
    else:
        valid_rows = rows_total
        invalid_rows = 0
    lengths = [len(line) for line in lines]
    length_min = min(lengths) if lengths else 0
    length_max = max(lengths) if lengths else 0
    status = "PROCESADO"
    if expected_length == 0:
        status = "ERROR"
        warnings.append("EVENTO_NO_DETERMINADO")
    if invalid_rows > 0:
        status = "ERROR"
    result = Dat02Result(
        timestamp_procesamiento=datetime.now(timezone.utc).isoformat(),
        institucion="TSE",
        acontecimiento=event,
        archivo_zip=zip_path.name,
        archivo_txt=selected_txt.name,
        ruta_zip=str(zip_path),
        ruta_extraccion=str(extraction_dir),
        periodo_anio=period["periodo_anio"],
        periodo_mes=period["periodo_mes"],
        periodo_desde=period["periodo_desde"],
        periodo_hasta=period["periodo_hasta"],
        periodo_original=period["periodo_original"],
        sha256_zip=sha_zip,
        sha256_txt=sha256(txt_bytes).hexdigest(),
        encoding=encoding,
        longitud_esperada=expected_length,
        longitud_minima=length_min,
        longitud_maxima=length_max,
        filas_totales=rows_total,
        filas_validas=valid_rows,
        filas_invalidas=invalid_rows,
        errores_tecnicos=sorted(set(warnings)),
        estado=status,
        observaciones="Procesamiento realizado sin almacenar registros personales.",
    )
    result.status = result.estado
    result.file_txt = result.archivo_txt
    result.extraction_dir = Path(result.ruta_extraccion)
    result.raw_bytes = zip_bytes
    result.rows_total = result.filas_totales
    return result


def write_manifest(results: list[Dat02Result], manifest_path: Path) -> Path:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[str] = []
    if manifest_path.exists():
        rows = [line for line in manifest_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    seen: set[str] = set()
    for line in rows:
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        sha_value = str(payload.get("sha256_zip", ""))
        if sha_value:
            seen.add(sha_value)
    with manifest_path.open("a", encoding="utf-8") as handle:
        for result in results:
            if result.sha256_zip in seen:
                continue
            handle.write(json.dumps(result.to_manifest_record(), ensure_ascii=False) + "\n")
            seen.add(result.sha256_zip)
    return manifest_path


def generate_report(results: list[Dat02Result], report_path: Path) -> Path:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DAT-02 — Reporte de ingesta TSE",
        "",
        f"Fecha de ejecución: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Resumen global",
        "",
        f"- ZIP procesados: {len(results)}",
        f"- Estados: {', '.join(sorted({item.estado for item in results}))}",
        "",
        "## Detalle por archivo",
        "",
    ]
    for item in results:
        source_kind = "ejecución actual" if item.estado == "PROCESADO" else "manifiesto previo"
        lines.extend([
            f"### {item.acontecimiento} — {item.archivo_zip}",
            "",
            f"- Período semántico: {item.periodo_original or 'PERIODO_NO_DETERMINADO'}",
            f"- Fecha inicio: {item.periodo_desde or 'NO_DETERMINADO'}",
            f"- Fecha fin: {item.periodo_hasta or 'NO_DETERMINADO'}",
            f"- Ruta ZIP: {item.ruta_zip}",
            f"- TXT: {item.archivo_txt or 'NO_DISPONIBLE'}",
            f"- SHA-256 ZIP: {item.sha256_zip}",
            f"- SHA-256 TXT: {item.sha256_txt}",
            f"- Codificación: {item.encoding}",
            f"- Longitud esperada: {item.longitud_esperada}",
            f"- Longitud observada: {item.longitud_minima}..{item.longitud_maxima}",
            f"- Filas: {item.filas_totales} total / {item.filas_validas} válidas / {item.filas_invalidas} inválidas",
            f"- Estado: {item.estado}",
            f"- Fuente de métricas: {source_kind}",
            f"- Errores técnicos: {', '.join(item.errores_tecnicos) if item.errores_tecnicos else 'ninguno'}",
            "",
        ])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def process_batch(source_root: Path, extraction_root: Path, manifest_path: Path | None = None) -> list[Dat02Result]:
    source_root = Path(source_root)
    extraction_root = Path(extraction_root)
    manifest_path = Path(manifest_path) if manifest_path else Path("data/work/dat02_manifest.jsonl")
    results: list[Dat02Result] = []
    for zip_path in sorted(source_root.rglob("*.zip")):
        try:
            results.append(process_zip(zip_path, extraction_root, manifest_path))
        except Exception as exc:  # pragma: no cover - defensive branch for batch robustness
            error_result = Dat02Result(
                timestamp_procesamiento=datetime.now(timezone.utc).isoformat(),
                institucion="TSE",
                acontecimiento=detect_event_name(zip_path),
                archivo_zip=zip_path.name,
                archivo_txt="",
                ruta_zip=str(zip_path),
                ruta_extraccion=str(extraction_root),
                periodo_anio=None,
                periodo_mes=None,
                periodo_desde=None,
                periodo_hasta=None,
                periodo_original=None,
                sha256_zip=sha256(zip_path.read_bytes()).hexdigest() if zip_path.exists() else "",
                sha256_txt="",
                encoding="ENCODING_NO_DETERMINADO",
                longitud_esperada=0,
                longitud_minima=0,
                longitud_maxima=0,
                filas_totales=0,
                filas_validas=0,
                filas_invalidas=0,
                errores_tecnicos=[type(exc).__name__],
                estado="ERROR",
                observaciones=str(exc),
            )
            error_result.status = error_result.estado
            error_result.file_txt = error_result.archivo_txt
            error_result.extraction_dir = Path(error_result.ruta_extraccion) if error_result.ruta_extraccion else None
            error_result.raw_bytes = zip_path.read_bytes() if zip_path.exists() else b""
            error_result.rows_total = error_result.filas_totales
            results.append(error_result)
    write_manifest(results, manifest_path)
    return results


def verify_dat02(source_root: Path = Path("data/raw/tse"), extraction_root: Path = Path("data/extracted/tse"), manifest_path: Path = Path("data/work/dat02_manifest.jsonl"), report_path: Path = Path("docs/evidencias/DAT-02_reporte_ingesta.md")) -> str:
    results = process_batch(source_root, extraction_root, manifest_path)
    generate_report(results, report_path)
    checks = all(result.status in {"PROCESADO", "YA_PROCESADO"} for result in results if result.archivo_zip)
    if manifest_path.exists() and report_path.exists() and checks:
        return "DAT-02 = OK"
    missing = []
    if not manifest_path.exists():
        missing.append("manifiesto")
    if not report_path.exists():
        missing.append("reporte")
    if not checks:
        missing.append("criterios principales")
    return "DAT-02 = NO_LISTA_PARA_CERRAR" + (f" (faltan: {', '.join(missing)})" if missing else "")

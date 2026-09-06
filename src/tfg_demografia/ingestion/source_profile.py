import csv
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ..errors import TSEError
from ..schema_loader import load_schema

DATASETS = ("nacimientos", "matrimonios", "defunciones")


def _date(row: dict[str, str], day_column: str) -> str | None:
    try:
        return f"{int(row['year']):04d}-{int(row['month']):02d}-{int(row[day_column]):02d}"
    except (KeyError, TypeError, ValueError):
        return None


def _apparent_gap_days(rows: list[dict[str, str]]) -> int:
    ranges = sorted((start, end) for row in rows if (start := _date(row, "period_start")) and (end := _date(row, "period_end")))
    gaps = 0
    previous_end = None
    for start, end in ranges:
        start_date = datetime.fromisoformat(start).date()
        end_date = datetime.fromisoformat(end).date()
        if previous_end and start_date > previous_end + timedelta(days=1):
            gaps += (start_date - previous_end).days - 1
        previous_end = max(previous_end, end_date) if previous_end else end_date
    return gaps


def build_profile(manifest_path: Path, schema_root: Path, datasets: tuple[str, ...] = DATASETS) -> dict[str, object]:
    if not manifest_path.exists():
        raise TSEError("No existe el manifiesto DAT-02 requerido para perfilar fuentes.")
    with manifest_path.open(encoding="utf-8", newline="") as file:
        manifest_rows = list(csv.DictReader(file))
    profiles = []
    for dataset in datasets:
        schema = load_schema(schema_root / f"{dataset}.json")
        rows = [row for row in manifest_rows if row.get("dataset") == dataset]
        encodings = Counter(row["encoding_detected"] for row in rows if row.get("encoding_detected"))
        starts = [value for row in rows if (value := _date(row, "period_start"))]
        ends = [value for row in rows if (value := _date(row, "period_end"))]
        total_rows = sum(int(row.get("total_rows") or 0) for row in rows)
        valid_rows = sum(int(row.get("valid_length_rows") or 0) for row in rows)
        short_rows = sum(int(row.get("short_rows") or 0) for row in rows)
        long_rows = sum(int(row.get("long_rows") or 0) for row in rows)
        empty_rows = sum(int(row.get("empty_rows") or 0) for row in rows)
        profiles.append({
            "dataset": dataset,
            "txt_filename": next((row["txt_filename"] for row in rows if row.get("txt_filename")), "NO DETERMINADO"),
            "zip_pattern": {"nacimientos": "nac_*.zip", "matrimonios": "mat_*.zip", "defunciones": "def_*.zip"}[dataset],
            "expected_record_length": schema.expected_record_length,
            "schema_encoding": schema.encoding,
            "encodings_observed": dict(sorted(encodings.items())),
            "publication_period_start": min(starts) if starts else None,
            "publication_period_end": max(ends) if ends else None,
            "file_count": len(rows),
            "total_rows": total_rows,
            "valid_length_rows": valid_rows,
            "short_rows": short_rows,
            "long_rows": long_rows,
            "empty_rows": empty_rows,
            "apparent_gap_days": _apparent_gap_days(rows),
            "configured_fields": [{"name": field.name, "start": field.start, "end": field.end, "length": field.end - field.start + 1, "type": field.type, "required": field.required, "source": "CONFIGURADO TECNICAMENTE", "status": "CONFIGURADO"} for field in schema.fields],
            "movement_configured": bool(schema.movement.get("configured", False)),
            "event_date": "NO DOCUMENTADO EN LA FUENTE CONSULTADA",
            "marginal_date": "NO DOCUMENTADO EN LA FUENTE CONSULTADA",
            "application_date": "NO DOCUMENTADO EN LA FUENTE CONSULTADA; la fecha del nombre ZIP representa el periodo de publicacion del movimiento.",
            "territorial_level": "NO DETERMINADO",
            "potential_identifiers": "NO DOCUMENTADO EN LA FUENTE CONSULTADA",
            "privacy_risk": "ALTO: los TXT registrales pueden contener datos identificables; el perfil no conserva valores ni lineas.",
            "field_missingness": "NO DETERMINADO: no hay campos con posiciones oficialmente documentadas o configuradas.",
        })
    return {"profile_version": "1.0", "generated_at_utc": datetime.now(timezone.utc).isoformat(), "source": "Manifiesto DAT-02 y esquemas tecnicos del proyecto", "profiles": profiles}


def write_profile(profile: dict[str, object], json_path: Path, table_path: Path, narrative_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    profiles = profile["profiles"]
    table_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ("acontecimiento", "archivo_txt", "patron_zip", "longitud_esperada", "codificacion_observada", "periodo_publicacion_inicio", "periodo_publicacion_fin", "archivos_analizados", "filas", "filas_validas_longitud", "filas_cortas", "filas_largas", "filas_vacias", "huecos_aparentes_dias", "periodicidad", "nivel_territorial", "identificadores_potenciales", "fechas_internas", "faltantes_por_campo", "riesgo_privacidad", "limitacion_documental")
    with table_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for item in profiles:
            writer.writerow({"acontecimiento": item["dataset"].upper(), "archivo_txt": item["txt_filename"], "patron_zip": item["zip_pattern"], "longitud_esperada": item["expected_record_length"], "codificacion_observada": "; ".join(item["encodings_observed"]), "periodo_publicacion_inicio": item["publication_period_start"] or "NO DETERMINADO", "periodo_publicacion_fin": item["publication_period_end"] or "NO DETERMINADO", "archivos_analizados": item["file_count"], "filas": item["total_rows"], "filas_validas_longitud": item["valid_length_rows"], "filas_cortas": item["short_rows"], "filas_largas": item["long_rows"], "filas_vacias": item["empty_rows"], "huecos_aparentes_dias": item["apparent_gap_days"], "periodicidad": "Semanal por bloques; bloques parciales posibles", "nivel_territorial": item["territorial_level"], "identificadores_potenciales": item["potential_identifiers"], "fechas_internas": item["event_date"], "faltantes_por_campo": item["field_missingness"], "riesgo_privacidad": "ALTO", "limitacion_documental": "Sin diccionario oficial de campos, fechas ni movimientos"})
    lines = ["# Perfil de datos TSE - FUE-04", "", "Este perfil se genera desde el manifiesto DAT-02 y los esquemas técnicos. No contiene líneas RAW, valores individuales ni identificadores.", "", "## Criterio de interpretación", "", "La cobertura descrita es de publicación de movimientos, no de ocurrencia del acontecimiento. No hay posiciones de fechas internas documentadas oficialmente en el workspace; por tanto, fecha del suceso, fecha marginal y fecha de aplicación se declaran `NO DOCUMENTADO EN LA FUENTE CONSULTADA`.", "", "| Característica | Nacimientos | Matrimonios | Defunciones |", "|---|---|---|---|"]
    labels = {"expected_record_length": "Longitud esperada", "file_count": "Archivos analizados", "total_rows": "Filas", "valid_length_rows": "Filas con longitud válida", "short_rows": "Filas cortas", "long_rows": "Filas largas", "empty_rows": "Filas vacías", "publication_period_start": "Cobertura publicación mínima", "publication_period_end": "Cobertura publicación máxima", "apparent_gap_days": "Huecos aparentes (días)", "territorial_level": "Nivel territorial", "potential_identifiers": "Identificadores potenciales", "field_missingness": "Faltantes por campo"}
    for key, label in labels.items():
        lines.append(f"| {label} | " + " | ".join(str(item[key] if item[key] is not None else "NO DETERMINADO") for item in profiles) + " |")
    for item in profiles:
        lines.extend(["", f"## {item['dataset'].upper()}", "", f"- Archivo TXT: `{item['txt_filename']}`.", f"- Patrón ZIP: `{item['zip_pattern']}`.", f"- Codificación observada: {', '.join(item['encodings_observed']) or 'NO DETERMINADO'}.", f"- Periodicidad: semanal por bloques de fechas; no se presupone que cada bloque tenga siete días.", f"- Movimientos: {'configurados' if item['movement_configured'] else 'NO CONFIGURADOS por ausencia de diccionario oficial'}.", f"- Privacidad: {item['privacy_risk']}", "", "### Campos y variables", "", "| Campo | Posición | Longitud | Tipo | Obligatorio | Fuente de definición | Estado |", "|---|---:|---:|---|---|---|---|"])
        if item["configured_fields"]:
            for field in item["configured_fields"]:
                lines.append(f"| {field['name']} | {field['start']}-{field['end']} | {field['length']} | {field['type'] or 'NO DETERMINADO'} | {field['required']} | {field['source']} | {field['status']} |")
        else:
            lines.append("| NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | Sin diccionario oficial en el workspace | NO DETERMINADO |")
        lines.extend(["", "### Fechas", "", "| Nombre lógico | Significado | Fuente | Formato | Presente en esquema | Uso correcto | Riesgo |", "|---|---|---|---|---|---|---|"])
        for date_name in ("Fecha del suceso", "Fecha marginal", "Fecha de aplicación"):
            lines.append(f"| {date_name} | NO DOCUMENTADO EN LA FUENTE CONSULTADA | Sin diccionario oficial | NO DETERMINADO | No | No inferir desde el nombre ZIP | Confundir periodo de publicación con fecha del acontecimiento |")
        lines.extend(["", "La fecha contenida en el nombre del ZIP se utiliza únicamente como período de publicación del movimiento; no identifica por sí misma ninguna de las fechas internas anteriores."])
    narrative_path.parent.mkdir(parents=True, exist_ok=True)
    narrative_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
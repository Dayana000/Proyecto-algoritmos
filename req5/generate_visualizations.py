#!/usr/bin/env python3
"""
Requerimiento 5: generación de visualizaciones en PDF sin dependencias externas.

Producción:
1. Mapa de calor geográfico (primer autor -> país estimado).
2. Nube de palabras dinámica.
3. Línea temporal de publicaciones por año y revista.

Salida: un único archivo PDF con tres páginas (`req5_visualizations.pdf`)
        y un JSON resumen (`req5_summary.json`).
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from urllib import error, parse, request


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "Data"
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

AUTHOR_COUNTRY_CACHE_PATH = CACHE_DIR / "author_country_cache.json"
COUNTRY_INFO_CACHE_PATH = CACHE_DIR / "country_info_cache.json"
AUTHOR_OVERRIDE_PATH = DATA_DIR / "author_locations_override.json"

PAGE_WIDTH = 842  # A4 landscape (points)
PAGE_HEIGHT = 595

STOPWORDS = {
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un",
    "para", "con", "no", "una", "su", "al", "lo", "como", "más", "pero", "sus",
    "le", "ya", "o", "este", "sí", "porque", "esta", "entre", "cuando", "muy",
    "sin", "sobre", "también", "me", "hasta", "hay", "donde", "quien", "desde",
    "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros",
    "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué",
    "unos", "yo", "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho",
    "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas",
    "algo", "nosotros", "mi", "mis", "tú", "te", "ti", "tu", "tus", "ellas", "nosotras",
    "vosotros", "vosotras", "os", "mío", "mía", "míos", "mías", "tuyo", "tuya",
    "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra",
    "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "esos",
    "esas", "estoy", "estás", "está", "estamos", "estáis", "están", "esté", "estés",
    "estemos", "estéis", "estén", "estaré", "estarás", "estará", "estaremos",
    "estaréis", "estarán", "estaría", "estarías", "estaríamos", "estaríais",
    "estarían", "estaba", "estabas", "estábamos", "estabais", "estaban", "estuve",
    "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron", "estuviera",
    "estuvieras", "estuviéramos", "estuvierais", "estuvieran", "estuviese",
    "estuvieses", "estuviésemos", "estuvieseis", "estuviesen", "estando",
    "estado", "estada", "estados", "estadas", "estad",
    "a", "an", "and", "the", "is", "are", "was", "were", "be", "been", "being",
    "to", "of", "in", "for", "on", "with", "as", "by", "at", "from", "up", "down",
    "out", "about", "into", "over", "after", "before", "between", "but", "if",
    "because", "while", "do", "does", "did", "doing", "this", "that", "these",
    "those", "he", "she", "it", "they", "them", "his", "her", "their", "our", "we",
    "you", "your", "i", "me", "my", "mine", "ours", "yours", "hers", "him",
    "himself", "herself", "yourself", "themselves", "itself", "what", "which",
    "who", "whom", "where", "when", "why", "how", "all", "any", "both", "each",
    "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "can", "will", "just", "don",
    "should", "now"
}


class SimplePDF:
    """Generador mínimo de PDFs vectoriales (texto y formas básicas)."""

    def __init__(self, width: float = PAGE_WIDTH, height: float = PAGE_HEIGHT) -> None:
        self.width = width
        self.height = height
        self.pages: List[List[str]] = []

    def add_page(self) -> None:
        self.pages.append([])

    def _append(self, command: str) -> None:
        if not self.pages:
            self.add_page()
        self.pages[-1].append(command)

    def set_fill_color(self, color: Tuple[float, float, float]) -> None:
        r, g, b = color
        self._append(f"{r:.3f} {g:.3f} {b:.3f} rg")

    def set_stroke_color(self, color: Tuple[float, float, float]) -> None:
        r, g, b = color
        self._append(f"{r:.3f} {g:.3f} {b:.3f} RG")

    def _normalize_text(self, text: str) -> str:
        normalized = unicodedata.normalize("NFKD", text or "")
        stripped = "".join(ch for ch in normalized if not unicodedata.combining(ch))
        stripped = stripped.replace("\r", " ").replace("\n", " ")
        ascii_text = "".join(ch if 32 <= ord(ch) <= 126 else " " for ch in stripped)
        return ascii_text

    def add_text(
        self,
        x: float,
        y: float,
        text: str,
        size: float = 12,
        color: Tuple[float, float, float] = (0, 0, 0),
    ) -> None:
        self.set_fill_color(color)
        clean = self._normalize_text(text)
        escaped = (
            clean.replace("\\", "\\\\")
            .replace("(", "\\(")
            .replace(")", "\\)")
        )
        self._append(f"BT /F1 {size:.2f} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm ({escaped}) Tj ET")

    def draw_rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        fill_color: Optional[Tuple[float, float, float]] = None,
        stroke_color: Optional[Tuple[float, float, float]] = None,
        stroke_width: float = 1.0,
    ) -> None:
        operator = "n"
        if fill_color:
            self.set_fill_color(fill_color)
            operator = "f"
        if stroke_color:
            self.set_stroke_color(stroke_color)
            self._append(f"{stroke_width:.2f} w")
            operator = "S" if operator == "n" else "B"
        self._append(f"{x:.2f} {y:.2f} {width:.2f} {height:.2f} re {operator}")

    def draw_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: Tuple[float, float, float] = (0, 0, 0),
        width: float = 1.0,
    ) -> None:
        self.set_stroke_color(color)
        self._append(f"{width:.2f} w")
        self._append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def write(self, path: Path) -> None:
        objects: List[bytes] = [b""]  # índice 0 reservado
        page_refs: List[int] = []

        # Placeholder para Catalog y Pages
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")  # obj 1
        objects.append(b"<< /Type /Pages >>")  # obj 2 -> se actualizará
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")  # obj3 font

        for page_content in self.pages:
            stream_bytes = "\n".join(page_content).encode("utf-8")
            content_obj = (
                f"<< /Length {len(stream_bytes)} >>\nstream\n".encode("utf-8")
                + stream_bytes
                + b"\nendstream"
            )
            objects.append(content_obj)
            content_obj_num = len(objects) - 1

            page_dict = (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width:.2f} {self.height:.2f}] "
                f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_obj_num} 0 R >>"
            ).encode("utf-8")
            objects.append(page_dict)
            page_obj_num = len(objects) - 1
            page_refs.append(page_obj_num)

        kids = " ".join(f"{num} 0 R" for num in page_refs)
        objects[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_refs)} >>".encode("utf-8")

        with path.open("wb") as fh:
            fh.write(b"%PDF-1.4\n")
            offsets: List[int] = []
            for idx in range(1, len(objects)):
                offsets.append(fh.tell())
                fh.write(f"{idx} 0 obj\n".encode("utf-8"))
                fh.write(objects[idx])
                fh.write(b"\nendobj\n")

            xref_pos = fh.tell()
            fh.write(f"xref\n0 {len(objects)}\n".encode("utf-8"))
            fh.write(b"0000000000 65535 f \n")
            for offset in offsets:
                fh.write(f"{offset:010d} 00000 n \n".encode("utf-8"))
            fh.write(b"trailer\n")
            fh.write(f"<< /Size {len(objects)} /Root 1 0 R >>\n".encode("utf-8"))
            fh.write(b"startxref\n")
            fh.write(f"{xref_pos}\n".encode("utf-8"))
            fh.write(b"%%EOF")


def load_json(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def save_json(path: Path, data: Dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def parse_bibtex(file_path: Path) -> List[Dict[str, str]]:
    articles: List[Dict[str, str]] = []
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo BibTeX: {file_path}")

    current: Dict[str, str] = {}
    inside = False

    with file_path.open("r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if line.startswith("@article"):
                inside = True
                current = {}
            elif inside and line == "}":
                if current:
                    articles.append(current)
                inside = False
            elif inside and "=" in line:
                key, value = line.split("=", 1)
                key = key.strip().lower()
                value = value.strip().rstrip(",").strip("{}").strip()
                current[key] = value

    return articles


def extract_first_author(author_field: str) -> Optional[str]:
    if not author_field:
        return None
    normalized = author_field.replace(" and ", ";")
    parts = [p.strip() for p in normalized.split(";") if p.strip()]
    return parts[0] if parts else None


def sanitize_first_name(author_name: str) -> Optional[str]:
    if not author_name:
        return None
    first_part = re.split(r"[,\s\-]+", author_name.strip())[0]
    first_part = re.sub(r"[^\w]", "", first_part)
    return first_part.lower() if first_part else None


def fetch_json(url: str, params: Optional[Dict[str, str]] = None) -> Optional[Dict]:
    try:
        if params:
            url = f"{url}?{parse.urlencode(params)}"
        req = request.Request(url, headers={"User-Agent": "Req5Visualizer/1.0"})
        with request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = resp.read().decode("utf-8")
                return json.loads(data)
    except (error.URLError, error.HTTPError, TimeoutError, json.JSONDecodeError):
        return None
    return None


def request_country_from_api(first_name: str) -> Optional[str]:
    payload = fetch_json("https://api.nationalize.io/", params={"name": first_name})
    if not payload:
        return None
    countries = payload.get("country")
    if countries:
        best = max(countries, key=lambda item: item.get("probability", 0))
        return best.get("country_id")
    return None


def request_country_info(country_code: str) -> Optional[Dict[str, str]]:
    data = fetch_json(f"https://restcountries.com/v3.1/alpha/{country_code}")
    if not data:
        return None
    if isinstance(data, list) and data:
        entry = data[0]
        name = (
            entry.get("translations", {})
            .get("spa", {})
            .get("common")
            or entry.get("name", {}).get("common")
            or country_code
        )
        latlng = entry.get("latlng") or [0.0, 0.0]
        if len(latlng) >= 2:
            return {
                "name": name,
                "lat": float(latlng[0]),
                "lon": float(latlng[1]),
            }
    return None


def resolve_country_info(
    author: str,
    overrides: Dict[str, str],
    author_cache: Dict[str, str],
    country_cache: Dict[str, Dict[str, str]],
) -> Tuple[str, Optional[float], Optional[float]]:
    if not author:
        return "Desconocido", None, None

    author_key = author.strip().lower()
    if author_key in overrides:
        country_label = overrides[author_key]
        info = country_cache.get(country_label.upper())
        if info:
            return info["name"], info["lat"], info["lon"]
        return country_label, None, None

    if author in author_cache:
        country_code = author_cache[author]
    else:
        first_name = sanitize_first_name(author)
        country_code = request_country_from_api(first_name) if first_name else None
        if country_code:
            author_cache[author] = country_code

    if not country_code:
        return "Desconocido", None, None

    if country_code in country_cache:
        info = country_cache[country_code]
        return info["name"], info["lat"], info["lon"]

    info = request_country_info(country_code)
    if info:
        country_cache[country_code] = info
        return info["name"], info["lat"], info["lon"]

    return "Desconocido", None, None


def preprocess_text(text: str) -> List[str]:
    normalized = text.lower()
    normalized = re.sub(r"[^a-záéíóúüñ\s]", " ", normalized)
    tokens = [token.strip() for token in normalized.split() if token.strip()]
    return [tok for tok in tokens if tok not in STOPWORDS and len(tok) > 3]


def interpolate_color(value: float) -> Tuple[float, float, float]:
    """Devuelve un color interpolado (amarillo -> rojo)."""
    value = max(0.0, min(1.0, value))
    # Amarillo (1,1,0) a rojo (1,0,0)
    return (1.0, 1.0 - value, 0.0)


def draw_geographical_heatmap(
    pdf: SimplePDF,
    country_points: List[Dict[str, float]],
) -> None:
    pdf.add_page()
    pdf.add_text(40, PAGE_HEIGHT - 40, "Mapa de calor geográfico por país (primer autor)", size=18)
    pdf.add_text(40, PAGE_HEIGHT - 60, "Estimación basada en nationalize.io + restcountries.com ", size=10, color=(0.3, 0.3, 0.3))

    map_left = 60
    map_bottom = 140
    map_width = PAGE_WIDTH - 120
    map_height = PAGE_HEIGHT - 220

    pdf.draw_rect(map_left, map_bottom, map_width, map_height, stroke_color=(0.7, 0.7, 0.7))

    # Líneas guía de latitud y longitud
    for lat in range(-60, 70, 30):
        y = map_bottom + ((lat + 90) / 180) * map_height
        pdf.draw_line(map_left, y, map_left + map_width, y, color=(0.85, 0.85, 0.85))
        pdf.add_text(map_left - 45, y - 5, f"{lat}°", size=9)

    for lon in range(-150, 210, 60):
        x = map_left + ((lon + 180) / 360) * map_width
        pdf.draw_line(x, map_bottom, x, map_bottom + map_height, color=(0.85, 0.85, 0.85))
        pdf.add_text(x - 15, map_bottom - 25, f"{lon}°", size=9)

    if not country_points:
        pdf.add_text(map_left + map_width / 2 - 120, map_bottom + map_height / 2, "Sin datos geográficos suficientes.", size=14)
        return

    max_count = max(point["count"] for point in country_points)

    for point in country_points:
        lon = point["lon"]
        lat = point["lat"]
        count = point["count"]
        x = map_left + ((lon + 180) / 360) * map_width
        y = map_bottom + ((lat + 90) / 180) * map_height
        intensity = count / max_count
        size = 8 + 18 * math.sqrt(intensity)
        color = interpolate_color(intensity)
        pdf.draw_rect(x - size / 2, y - size / 2, size, size, fill_color=color, stroke_color=(0.6, 0.6, 0.6), stroke_width=0.5)

    top_countries = sorted(country_points, key=lambda item: item["count"], reverse=True)[:3]
    for point in top_countries:
        lon = point["lon"]
        lat = point["lat"]
        x = map_left + ((lon + 180) / 360) * map_width
        y = map_bottom + ((lat + 90) / 180) * map_height
        pdf.add_text(
            x + 6,
            y + 10,
            f"{point['name']} ({point['count']})",
            size=10,
            color=(0.15, 0.15, 0.15),
        )


def draw_word_cloud(pdf: SimplePDF, word_counter: Counter, max_words: int = 120) -> None:
    pdf.add_page()
    pdf.add_text(40, PAGE_HEIGHT - 40, "Nube de palabras", size=18)
    pdf.add_text(40, PAGE_HEIGHT - 60, "Frecuencia relativa en abstracts y keywords (dynamic)", size=10, color=(0.3, 0.3, 0.3))

    area_left = 40
    area_bottom = 80
    area_width = PAGE_WIDTH - 80
    area_height = PAGE_HEIGHT - 140

    pdf.draw_rect(area_left, area_bottom, area_width, area_height, stroke_color=(0.8, 0.8, 0.8))

    if not word_counter:
        pdf.add_text(area_left + area_width / 2 - 100, area_bottom + area_height / 2, "Sin términos suficientes.", size=14)
        return

    top_words = word_counter.most_common(max_words)
    num_cols = max(10, int(math.sqrt(len(top_words)) * 1.5))
    num_rows = math.ceil(len(top_words) / num_cols)

    for idx, (word, count) in enumerate(top_words):
        row = idx // num_cols
        col = idx % num_cols
        x = area_left + ((col + random.uniform(0.2, 0.8)) / num_cols) * area_width
        y = area_bottom + area_height - ((row + random.uniform(0.2, 0.8)) / num_rows) * area_height
        size = 10 + (count / top_words[0][1]) * 26
        color = (random.uniform(0.1, 0.4), random.uniform(0.1, 0.4), random.uniform(0.1, 0.4))
        pdf.add_text(x, y, word, size=size, color=color)


def draw_publication_timeline(
    pdf: SimplePDF,
    timeline_data: Dict[str, Dict[int, int]],
    top_n_journals: int = 5,
) -> None:
    pdf.add_page()
    pdf.add_text(40, PAGE_HEIGHT - 40, "Línea temporal de publicaciones por año y revista", size=18)

    chart_left = 80
    chart_bottom = 80
    chart_width = PAGE_WIDTH - 160
    chart_height = PAGE_HEIGHT - 160

    pdf.draw_rect(chart_left, chart_bottom, chart_width, chart_height, stroke_color=(0.8, 0.8, 0.8))

    if not timeline_data:
        pdf.add_text(chart_left + chart_width / 2 - 100, chart_bottom + chart_height / 2, "Sin datos temporales disponibles.", size=14)
        return

    journal_totals = sorted(
        timeline_data.items(),
        key=lambda item: sum(item[1].values()),
        reverse=True,
    )[:top_n_journals]

    all_years = sorted({year for _, data in journal_totals for year in data.keys()})
    if not all_years:
        pdf.add_text(chart_left + chart_width / 2 - 100, chart_bottom + chart_height / 2, "Sin años válidos.", size=14)
        return

    min_year, max_year = min(all_years), max(all_years)
    year_span = max_year - min_year or 1

    max_count = max(sum(data.values()) for _, data in journal_totals) or 1
    color_palette = [
        (0.86, 0.21, 0.25),
        (0.12, 0.47, 0.71),
        (0.17, 0.63, 0.17),
        (0.58, 0.40, 0.74),
        (0.89, 0.47, 0.20),
    ]

    # Ejes y ticks
    for year in all_years:
        x = chart_left + ((year - min_year) / year_span) * chart_width
        pdf.draw_line(x, chart_bottom, x, chart_bottom - 6, color=(0, 0, 0))
        pdf.add_text(x - 10, chart_bottom - 20, str(year), size=9)

    max_y_tick = max(
        max(data.values()) if data else 0
        for _, data in journal_totals
    )
    max_y_tick = max(max_y_tick, 1)

    for tick in range(0, max_y_tick + 1):
        y = chart_bottom + (tick / max_y_tick) * chart_height if max_y_tick else chart_bottom
        pdf.draw_line(chart_left - 6, y, chart_left, y, color=(0, 0, 0))
        pdf.add_text(chart_left - 40, y - 4, str(tick), size=9)

    legend_x = chart_left + chart_width + 10
    legend_y = chart_bottom + chart_height

    for idx, (journal, year_counts) in enumerate(journal_totals):
        color = color_palette[idx % len(color_palette)]
        sorted_years = sorted(year_counts.keys())
        previous_point = None
        for year in sorted_years:
            count = year_counts[year]
            x = chart_left + ((year - min_year) / year_span) * chart_width
            y = chart_bottom + (count / max_y_tick) * chart_height if max_y_tick else chart_bottom
            if previous_point:
                pdf.draw_line(previous_point[0], previous_point[1], x, y, color=color, width=1.5)
            pdf.draw_rect(x - 2, y - 2, 4, 4, fill_color=color, stroke_color=color)
            previous_point = (x, y)

        pdf.draw_rect(legend_x, legend_y - 10, 10, 10, fill_color=color, stroke_color=color)
        pdf.add_text(legend_x + 14, legend_y - 8, f"{journal} ({sum(year_counts.values())})", size=9)
        legend_y -= 18


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera visualizaciones PDF para el requerimiento 5.")
    parser.add_argument(
        "--entrada",
        default=str(DATA_DIR / "unificados.bib"),
        help="Ruta del archivo BibTeX unificado.",
    )
    parser.add_argument(
        "--salida",
        default=str(DATA_DIR / "visualizations" / "req5"),
        help="Directorio de salida para el PDF y el resumen.",
    )
    parser.add_argument(
        "--max-articulos",
        type=int,
        default=None,
        help="Número máximo de artículos a procesar (útil para pruebas rápidas).",
    )
    args = parser.parse_args()

    bibtex_path = Path(args.entrada)
    output_dir = Path(args.salida)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        articles = parse_bibtex(bibtex_path)
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(1)

    if args.max_articulos:
        articles = articles[: args.max_articulos]

    overrides = {k.lower(): v for k, v in load_json(AUTHOR_OVERRIDE_PATH).items()}
    author_country_cache = load_json(AUTHOR_COUNTRY_CACHE_PATH)
    country_info_cache = load_json(COUNTRY_INFO_CACHE_PATH)

    country_counts: Dict[str, int] = defaultdict(int)
    country_points: Dict[str, Dict[str, float]] = {}

    word_counter: Counter = Counter()
    timeline: Dict[str, Dict[int, int]] = defaultdict(lambda: defaultdict(int))

    for article in articles:
        first_author = extract_first_author(article.get("author", ""))
        country_name, lat, lon = resolve_country_info(
            first_author,
            overrides,
            author_country_cache,
            country_info_cache,
        )
        country_counts[country_name] += 1

        if lat is not None and lon is not None:
            entry = country_points.setdefault(
                country_name,
                {"name": country_name, "lat_sum": 0.0, "lon_sum": 0.0, "count": 0},
            )
            entry["lat_sum"] += lat
            entry["lon_sum"] += lon
            entry["count"] += 1

        abstract_text = article.get("abstract", "")
        keywords_text = article.get("keywords", "")
        tokens = preprocess_text(abstract_text + " " + keywords_text)
        word_counter.update(tokens)

        journal = article.get("journal", "Desconocido")
        year_value = article.get("year", "")
        try:
            year = int(re.findall(r"\d{4}", year_value)[0])
        except (IndexError, ValueError):
            continue
        timeline[journal][year] += 1

    save_json(AUTHOR_COUNTRY_CACHE_PATH, author_country_cache)
    save_json(COUNTRY_INFO_CACHE_PATH, country_info_cache)

    points_for_map: List[Dict[str, float]] = []
    for country_name, info in country_points.items():
        if info["count"] == 0:
            continue
        points_for_map.append(
            {
                "name": country_name,
                "count": country_counts.get(country_name, info["count"]),
                "lat": info["lat_sum"] / info["count"],
                "lon": info["lon_sum"] / info["count"],
            }
        )

    pdf = SimplePDF()
    draw_geographical_heatmap(pdf, points_for_map)
    draw_word_cloud(pdf, word_counter)
    draw_publication_timeline(pdf, timeline)

    pdf_path = output_dir / "req5_visualizations.pdf"
    pdf.write(pdf_path)

    summary = {
        "total_articulos": len(articles),
        "paises": country_counts,
        "palabras_principales": dict(word_counter.most_common(50)),
        "revistas_top": {
            journal: dict(sorted(years.items()))
            for journal, years in sorted(
                timeline.items(),
                key=lambda item: sum(item[1].values()),
                reverse=True,
            )[:5]
        },
    }

    summary_path = output_dir / "req5_summary.json"
    save_json(summary_path, summary)

    print("Visualizaciones PDF generadas en:", pdf_path)
    print("Resumen JSON:", summary_path)


if __name__ == "__main__":
    main()


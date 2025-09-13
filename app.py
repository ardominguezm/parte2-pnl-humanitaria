import os
import zipfile
import re
import pandas as pd
import spacy
from PyPDF2 import PdfReader
import streamlit as st
import subprocess

# ================================
# Cargar modelo spaCy (se instala si no existe)
# ================================
@st.cache_resource
def load_spacy_model():
    return spacy.load("es_core_news_sm")

nlp = load_spacy_model()


# ================================
# Leer PDFs (incluye subcarpetas)
# ================================
def read_reports(path="data"):
    reports = {}
    for root, dirs, files in os.walk(path):
        for fname in files:
            if fname.endswith(".pdf"):
                fpath = os.path.join(root, fname)
                pdf = PdfReader(fpath)
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                reports[fname] = text
    return reports

# ================================
# Extraer información
# ================================
def extraer_info_pregunta1(text, nombre_reporte="reporte.pdf"):
    doc = nlp(text)

    # Ubicaciones
    ubicaciones = [ent.text.strip() for ent in doc.ents if ent.label_ in ["LOC", "GPE"]]
    ubicaciones_limpias = []
    for loc in ubicaciones:
        loc = re.sub(r"\n", " ", loc)
        loc = re.sub(r"([a-z])([A-Z])", r"\1, \2", loc)
        ubicaciones_limpias.extend([l.strip() for l in loc.split(",") if len(l.strip()) > 2])
    ubicaciones_final = list(set(ubicaciones_limpias))

    # Fechas
    regex_patterns = [
        r"\b\d{1,2}\s+de\s+(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+\d{4}\b",
        r"\b(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+\d{4}\b",
        r"\b(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s*[-–]\s*(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+\d{4}\b",
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
    ]
    fechas_regex = []
    for pattern in regex_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        fechas_regex.extend(matches)
    fechas_final = list(set(fechas_regex))

    # Tipos de incidente
    keywords_incidentes = {
        "Inundación": ["inundación", "lluvia", "río", "desbordamiento"],
        "Desplazamiento": ["desplazamiento", "huida", "migración"],
        "Salud": ["epidemia", "enfermedad", "hospital", "salud"],
        "Seguridad": ["conflicto", "violencia", "ataque", "amenaza"]
    }
    tipos_detectados = []
    for tipo, palabras in keywords_incidentes.items():
        if any(palabra.lower() in text.lower() for palabra in palabras):
            tipos_detectados.append(tipo)

    return {
        "Reporte": nombre_reporte,
        "Ubicaciones": ", ".join(ubicaciones_final[:15]) if ubicaciones_final else "No detectadas",
        "Fechas": ", ".join(fechas_final) if fechas_final else "No detectadas",
        "Tipos de incidente": ", ".join(tipos_detectados) if tipos_detectados else "No detectados"
    }

# ================================
# Interfaz Streamlit
# ================================
st.title("📑 Analizador de Reportes Humanitarios")
st.write("Sube tus reportes en PDF o un archivo ZIP, y obtén un resumen automático con ubicaciones, fechas y tipos de incidentes.")

uploaded_file = st.file_uploader("Subir archivo", type=["pdf", "zip"])

if uploaded_file:
    os.makedirs("data", exist_ok=True)

    # Guardar archivo subido
    with open(os.path.join("data", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Descomprimir si es ZIP
    if uploaded_file.name.endswith(".zip"):
        with zipfile.ZipFile(os.path.join("data", uploaded_file.name), 'r') as zip_ref:
            zip_ref.extractall("data")

    # Procesar reportes
    reports = read_reports("data")
    resultados = []
    for fname, contenido in reports.items():
        resultados.append(extraer_info_pregunta1(contenido, nombre_reporte=fname))

    # Mostrar tabla
    df_resultados = pd.DataFrame(resultados)
    st.subheader("📊 Resultados extraídos")
    st.dataframe(df_resultados)

    # Botón de descarga
    csv = df_resultados.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar CSV", csv, "resultados_reportes.csv", "text/csv")

    # Resumen en lenguaje natural
    st.subheader("📝 Resumen automático")
    resumen = f"Se identificaron incidentes de {', '.join(set(', '.join(df_resultados['Tipos de incidente']).split(', ')))} en ubicaciones como {', '.join(df_resultados['Ubicaciones'].head(5))}. Los reportes incluyen fechas como {', '.join(df_resultados['Fechas'].head(3))}."
    st.write(resumen)

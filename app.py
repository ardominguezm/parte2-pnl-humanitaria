import gradio as gr
import pandas as pd
from PyPDF2 import PdfReader
import zipfile, os, re
import spacy

# ================================
# Cargar spaCy (modelo español)
# ================================
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"])
    nlp = spacy.load("es_core_news_sm")

# ================================
# Función de extracción
# ================================
def extraer_info_pregunta1(text, nombre_reporte="reporte.pdf"):
    doc = nlp(text)

    # Ubicaciones
    ubicaciones = [ent.text.strip() for ent in doc.ents if ent.label_ in ["LOC", "GPE"]]
    ubicaciones_final = list(set([re.sub(r"\n", " ", u) for u in ubicaciones]))

    # Fechas
    regex_patterns = [
        r"\b\d{1,2}\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+\d{4}\b",
        r"\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+\d{4}\b",
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
    ]
    fechas_final = []
    for pattern in regex_patterns:
        fechas_final.extend(re.findall(pattern, text, flags=re.IGNORECASE))

    # Tipos de incidente
    keywords_incidentes = {
        "Inundación": ["inundación", "lluvia", "río", "desbordamiento"],
        "Desplazamiento": ["desplazamiento", "huida", "migración"],
        "Salud": ["epidemia", "enfermedad", "hospital", "salud"],
        "Seguridad": ["conflicto", "violencia", "ataque", "amenaza"]
    }
    tipos_detectados = []
    for tipo, palabras in keywords_incidentes.items():
        if any(p in text.lower() for p in palabras):
            tipos_detectados.append(tipo)

    return {
        "Reporte": nombre_reporte,
        "Ubicaciones": ", ".join(ubicaciones_final) if ubicaciones_final else "No detectadas",
        "Fechas": ", ".join(set(fechas_final)) if fechas_final else "No detectadas",
        "Tipos de incidente": ", ".join(tipos_detectados) if tipos_detectados else "No detectados"
    }

# ================================
# Procesar PDFs o ZIP
# ================================
def analizar_reportes(file):
    resultados = []

    # ZIP
    if file.name.endswith(".zip"):
        with zipfile.ZipFile(file.name, 'r') as zip_ref:
            zip_ref.extractall("tmp")
        for fname in os.listdir("tmp"):
            if fname.endswith(".pdf"):
                pdf = PdfReader(os.path.join("tmp", fname))
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                resultados.append(extraer_info_pregunta1(text, nombre_reporte=fname))
    else:
        pdf = PdfReader(file.name)
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        resultados.append(extraer_info_pregunta1(text, nombre_reporte=os.path.basename(file.name)))

    df = pd.DataFrame(resultados)
    csv_path = "resultados.csv"
    df.to_csv(csv_path, index=False)
    return df, csv_path

# ================================
# Interfaz Gradio
# ================================
iface = gr.Interface(
    fn=analizar_reportes,
    inputs=gr.File(type="file", label="Sube un PDF o ZIP"),
    outputs=[
        gr.Dataframe(headers=["Reporte", "Ubicaciones", "Fechas", "Tipos de incidente"], label="Resultados"),
        gr.File(label="📥 Descargar CSV")
    ],
    title="📑 Analizador de Reportes Humanitarios",
    description="Sube tus reportes en PDF o ZIP y obtén una tabla con Ubicaciones, Fechas y Tipos de incidente."
)

iface.launch()

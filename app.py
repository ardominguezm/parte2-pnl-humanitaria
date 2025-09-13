import gradio as gr
import spacy
import pandas as pd
import zipfile, os, re
from PyPDF2 import PdfReader

# =========================
# Lazy load del modelo spaCy
# =========================
_nlp = None
def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("es_core_news_sm")
    return _nlp

# =========================
# Funciones auxiliares
# =========================
def extraer_info(texto, nombre_reporte=""):
    """Extrae ubicaciones, fechas y clasifica incidentes en categorías predefinidas."""

    nlp = get_nlp()
    doc = nlp(texto)

    # === 1. Ubicaciones (con filtros) ===
    ubicaciones_raw = [ent.text.strip() for ent in doc.ents if ent.label_ in ["LOC", "GPE"]]

    ubicaciones_filtradas = []
    for u in ubicaciones_raw:
        if len(u) < 3:  # muy cortas
            continue
        if re.search(r"[@•:]", u):  # caracteres no deseados
            continue
        if u.lower() in ["además", "histórico", "educación", "género", "alimentaria", "seguridad"]:
            continue
        ubicaciones_filtradas.append(u)

    ubicaciones = list(set(ubicaciones_filtradas))

    # === 2. Fechas (más patrones relevantes) ===
    patrones_fecha = [
        r"\b\d{1,2} de [a-zA-Z]+ de \d{4}\b",   # 10 de mayo de 2025
        r"\b[a-zA-Z]+ de \d{4}\b",              # mayo de 2025
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",           # 21/02/2020
        r"Fecha de publicación\s*\((.*?)\)",    # Fecha de publicación (29/07/2025)
        r"\bsemestre de \d{4}\b",               # semestre de 2025
        r"\bperiodo de \d{4}\b",                # periodo de 2024
        r"\bhuracanes de \d{4}\b"               # huracanes de 2025
    ]
    fechas = []
    for patron in patrones_fecha:
        fechas += re.findall(patron, texto, flags=re.IGNORECASE)
    fechas = list(set(fechas))

    # === 3. Clasificación en categorías predefinidas ===
    categorias = {
        "Desplazamiento": ["desplazamiento", "desplazados", "migración forzada"],
        "Seguridad alimentaria": ["seguridad alimentaria", "alimentación", "hambruna", "nutrición"],
        "Salud": ["salud", "hospital", "epidemia", "enfermedad", "atención médica"],
        "Protección": ["protección", "violencia", "riesgo", "seguridad", "conflicto"]
    }
    incidentes_detectados = []
    for categoria, keywords in categorias.items():
        for kw in keywords:
            if re.search(kw, texto, flags=re.IGNORECASE):
                incidentes_detectados.append(categoria)
                break

    return {
        "Reporte": nombre_reporte,
        "Ubicaciones": ", ".join(ubicaciones) if ubicaciones else "No detectadas",
        "Fechas": ", ".join(fechas) if fechas else "No detectadas",
        "Categorías de incidente": ", ".join(incidentes_detectados) if incidentes_detectados else "No clasificadas"
    }

def procesar_archivo(file_path):
    """Procesa PDF o ZIP y devuelve resumen + tabla exportable."""
    resultados = []

    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, "r") as z:
            for fname in z.namelist():
                if fname.endswith(".pdf"):
                    with z.open(fname) as f:
                        reader = PdfReader(f)
                        texto = "\n".join([p.extract_text() or "" for p in reader.pages])
                        resultados.append(extraer_info(texto, nombre_reporte=fname))
    elif file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        texto = "\n".join([p.extract_text() or "" for p in reader.pages])
        resultados.append(extraer_info(texto, nombre_reporte=os.path.basename(file_path)))
    else:
        return "❌ Formato no soportado", pd.DataFrame([{"Error": "Formato no soportado"}])

    df = pd.DataFrame(resultados)

    # === Resumen amigable ===
    resumenes = []
    for _, row in df.iterrows():
        resumen = f"""
📑 **Reporte:** {row['Reporte']}

📍 **Ubicaciones afectadas:** {row['Ubicaciones']}

📅 **Fechas relevantes:** {row['Fechas']}

⚠️ **Categorías de incidente:** {row['Categorías de incidente']}

En este reporte se identifican las ubicaciones más afectadas, el marco temporal y las principales categorías de incidente
para orientar la toma de decisiones de actores humanitarios no técnicos.
        """.strip()
        resumenes.append(resumen)

    resumen_final = "\n\n---\n\n".join(resumenes)
    return resumen_final, df

# =========================
# Interfaz Gradio
# =========================
with gr.Blocks() as demo:
    gr.Markdown("# 📑 Parte 2: Análisis Automático de Reportes Humanitarios")
    gr.Markdown("# Realizada por: Andy Domínguez(ardominguezm@gmail.com)")
    gr.Markdown("""
Esta aplicación cumple tres objetivos:
1. **Extraer automáticamente** ubicaciones, fechas y tipo de incidente de cada reporte.
2. **Clasificar incidentes** en categorías predefinidas: *Desplazamiento, Seguridad alimentaria, Salud, Protección*.
3. **Generar un resumen ejecutivo** listo para compartir con actores no técnicos.
""")

    file_input = gr.File(type="filepath", label="Sube un PDF o ZIP con varios reportes")
    output_text = gr.Markdown(label="Resumen Ejecutivo")
    output_table = gr.Dataframe(label="Resultados Detallados")

    file_input.change(
        fn=procesar_archivo,
        inputs=file_input,
        outputs=[output_text, output_table]
    )

if __name__ == "__main__":
    demo.launch()


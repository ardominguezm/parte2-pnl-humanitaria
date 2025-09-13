# 📑 Parte 2 – Prueba Técnica de PLN Humanitaria

Este repositorio contiene el desarrollo de la **parte 2 de la prueba técnica**, en la cual se procesan reportes humanitarios en PDF/ZIP para **extraer automáticamente**:

- 📍 **Ubicaciones**
- 📅 **Fechas**
- ⚠️ **Tipos de incidentes**

Se incluyen dos formas de uso:

1. Una **aplicación web en Streamlit** (para usuarios no técnicos).  
2. Un **script demo (`demo-ready.py`) con outputs reproducibles** (para revisión técnica).

---

## 🚀 1. Aplicación en Streamlit Cloud

La app permite a cualquier usuario subir reportes en PDF o ZIP y obtener:

- Una tabla interactiva con resultados.
- Descarga de CSV.
- Un resumen en lenguaje natural listo para compartir.

🔗 **Acceso a la app (Streamlit Cloud):**  
👉 [https://share.streamlit.io/](https://share.streamlit.io/) *(al desplegar tu app se generará aquí el link con tu usuario/repositorio)*

### Ejemplo de salida
| Reporte                                     | Ubicaciones                       | Fechas                       | Tipos de incidente                       |
|---------------------------------------------|-----------------------------------|-------------------------------|------------------------------------------|
| Acceso Hum. Cauca_Guaviare. 12.08.pdf        | Corinto, Miraflores, Argelia...   | 11 de agosto 2025, agosto 2025 | Inundación, Desplazamiento, Seguridad    |
| SitRep Emergencia por Inundaciones Amazonia | Cubarral, Miraflores, Colombia... | 21/02/2020, 29/07/2025        | Inundación, Desplazamiento, Salud, Seguridad |
| _BriefingHumanitario_La Guajira...           | La Guajira, Comité Departamental… | junio 2025                    | Inundación, Desplazamiento, Salud, Seguridad |

---

## 🖥️ 2. Script demo (`demo-ready.py`)

Este script reproduce el flujo de trabajo paso a paso con comentarios y muestra cómo se extrae la información.

### 📂 Ejecución local
```bash
git clone https://github.com/ardominguezm/parte2-pnl-humanitaria.git
cd parte2-pnl-humanitaria

# Instalar dependencias
pip install -r requirements.txt
python -m spacy download es_core_news_sm

# Ejecutar el demo
python demo-ready.py


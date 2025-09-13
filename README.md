# 📑 Parte 2 – Prueba Técnica de PLN Humanitaria

Este repositorio contiene el desarrollo de la **parte 2 de la prueba técnica**, en la cual se procesan reportes humanitarios en PDF/ZIP para **extraer automáticamente**:

- 📍 **Ubicaciones**
- 📅 **Fechas**
- ⚠️ **Tipos de incidentes**

Se incluyen dos formas de uso:

1. Una **aplicación web en Streamlit** (para usuarios no técnicos).  
2. Un **script demo (`demo-ready.py`) con outputs reproducibles** (para revisión técnica).

---

# 📑 Analizador de Reportes Humanitarios (Gradio + HF Spaces)

Este demo permite a usuarios no técnicos subir reportes en PDF o ZIP y obtener automáticamente:

- 📍 Ubicaciones
- 📅 Fechas
- ⚠️ Tipos de incidente
- 📊 Exportación a CSV

---

## 🚀 Cómo usar

1. Ve a Hugging Face → [https://huggingface.co/spaces](https://huggingface.co/spaces)  
2. Crea un nuevo **Space** → selecciona **Gradio** como framework.  
3. Sube los archivos:
   - `app_gradio.py`
   - `requirements.txt`
   - (opcional) `README.md`
4. Haz clic en **Deploy**.

En pocos minutos tendrás tu app online en un link tipo:



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


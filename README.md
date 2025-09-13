# 📑 Parte 2 – Procesamiento de Lenguaje Natural en Reportes Humanitarios

Este proyecto implementa una aplicación interactiva que procesa **reportes humanitarios en PDF o ZIP** para extraer información clave y presentarla en un formato accesible para **actores no técnicos**.

La solución está desarrollada en **Python + spaCy + Gradio** y se puede ejecutar tanto de manera local como en la nube mediante **Hugging Face Spaces**.

---

## 🎯 Objetivos del entregable

1. **Extraer automáticamente** de cada reporte:
   - 📍 Ubicaciones
   - 📅 Fechas
   - ⚠️ Tipos de incidente

2. **Clasificar incidentes** en categorías predefinidas:
   - Desplazamiento  
   - Seguridad alimentaria  
   - Salud  
   - Protección  

3. **Generar un resumen automatizado** en lenguaje sencillo, listo para compartir con actores no técnicos.

---

## 🚀 Demo en Hugging Face

👉 [Ver aplicación en Hugging Face Spaces](https://huggingface.co/spaces/ardominguezm/part2-test)  

Sube un **PDF** individual o un **ZIP con múltiples PDFs** y obtén:

- Un **resumen ejecutivo** en lenguaje claro.  
- Una **tabla detallada** con la información estructurada.  

---
📑 Reporte: _BriefingHumanitario_La Guajira_Enero-Junio2025.pdf
📍 Ubicaciones afectadas: La Guajira, Maicao, Uribia, Riohacha, Manaure, Barrancas
📅 Fechas relevantes: 5 de mayo de 2025, mayo de 2025, semestre de 2025
⚠️ Categorías de incidente: Desplazamiento, Seguridad alimentaria, Salud, Protección

En este reporte se identifican las ubicaciones más afectadas, el marco temporal y las principales categorías de incidente
para orientar la toma de decisiones de actores humanitarios no técnicos.

## 🛠 Uso local

### 1. Clonar el repositorio
```bash
git clone https://github.com/ardominguezm/parte2-pnl-humanitaria.git
cd parte2-pnl-humanitaria




---

📑 Reporte: _BriefingHumanitario_La Guajira_Enero-Junio2025.pdf
📍 Ubicaciones afectadas: La Guajira, Maicao, Uribia, Riohacha, Manaure, Barrancas
📅 Fechas relevantes: 5 de mayo de 2025, mayo de 2025, semestre de 2025
⚠️ Categorías de incidente: Desplazamiento, Seguridad alimentaria, Salud, Protección

En este reporte se identifican las ubicaciones más afectadas, el marco temporal y las principales categorías de incidente
para orientar la toma de decisiones de actores humanitarios no técnicos.


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

### Ejemplo de salida
| Reporte                                     | Ubicaciones                       | Fechas                       | Tipos de incidente                       |
|---------------------------------------------|-----------------------------------|-------------------------------|------------------------------------------|
| Acceso Hum. Cauca_Guaviare. 12.08.pdf        | Corinto, Miraflores, Argelia...   | 11 de agosto 2025, agosto 2025 | Inundación, Desplazamiento, Seguridad    |
| SitRep Emergencia por Inundaciones Amazonia | Cubarral, Miraflores, Colombia... | 21/02/2020, 29/07/2025        | Inundación, Desplazamiento, Salud, Seguridad |
| _BriefingHumanitario_La Guajira...           | La Guajira, Comité Departamental… | junio 2025                    | Inundación, Desplazamiento, Salud, Seguridad |




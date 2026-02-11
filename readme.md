# 🗺️ SUR DAO: El Atlas de Haroldo Horta
### *Preservación Digital y Cartografía Narrativa / Digital Preservation & Narrative Cartography*

---

## 🇪🇸 Resumen del Proyecto
**SUR DAO** es un atlas interactivo diseñado para rescatar y organizar el inmenso legado fotográfico de **Haroldo Horta**. A través de una interfaz geoespacial, el proyecto conecta décadas de registros —desde corresponsalías de guerra en Nicaragua hasta la travesía del Buque Escuela Esmeralda— con sus coordenadas exactas y las anécdotas humanas que les dieron vida.

Este proyecto no es solo una galería; es un **sistema de preservación activa** que transforma archivos maestros (TIFF) y metadatos de Adobe en una experiencia de exploración global.

### 🚀 Características Técnicas
- **Sincronización Automática:** Motor en Python que escanea la estructura de carpetas y genera la base de datos JSON.
- **Aspirador de Metadatos:** Integración con Adobe Bridge/Lightroom para extraer relatos y calificaciones (ratings) directamente de los archivos.
- **Optimización WebP:** Flujo de trabajo preparado para visualización de alta velocidad.
- **Interfaz Interactiva:** Mapas con Leaflet.js y clusters inteligentes de imágenes.

---

## 🇺🇸 Project Overview
**SUR DAO** is an interactive digital atlas created to preserve and organize the vast photographic legacy of **Haroldo Horta**. Using a geospatial interface, the project connects decades of records—ranging from war correspondence in Nicaragua to the world voyage of the Buque Escuela Esmeralda—with their precise coordinates and the human anecdotes behind them.

This project is not just a gallery; it is an **active preservation system** that transforms master files (TIFF) and Adobe metadata into a global exploration experience.

### 🚀 Technical Features
- **Automatic Sync:** Python-based engine that scans folder structures and generates the JSON database.
- **Metadata Ingestion:** Direct integration with Adobe Bridge/Lightroom to extract stories and ratings from the files.
- **WebP Optimization:** High-speed visualization workflow.
- **Interactive Interface:** Mapping with Leaflet.js and smart image clustering.

---

## 📂 Estructura de Archivos / Folder Structure
El sistema utiliza prefijos inteligentes para categorizar el contenido automáticamente:
* `pub_`: Crónica & Etnografía / Chronicles & Ethnography.
* `nomad_`: Bitácora Nómada / Nomad Logbook.
* `fly_`: Registro Aéreo / Aerial Records.
* `nav_`: Travesías & Flota Naval / Naval Voyages.
* `far_`: Faros del Fin del Mundo / Lighthouses.

---

## 🛠️ Cómo Actualizar el Atlas / How to Update
1.  **Organizar:** Coloca las nuevas fotos en `fotos/` usando los prefijos indicados.
2.  **Sincronizar:** Ejecuta el motor desde la raíz:
    ```bash
    python Scripts/unificar_atlas.py
    ```
3.  **Desplegar:**
    ```bash
    git add .
    git commit -m "Add new chronicles"
    git push
    ```

---

> *"No es solo una foto, es el testimonio de un zurdo que hizo volar gorras en el Ecuador y subió cámaras panorámicas donde nadie más se atrevió."* > 
> **Desarrollado con ❤️ en medio de una tormenta en Junín.**

# CursosUC Scraper & Dataset 📚

Este repositorio contiene un script en Python diseñado para extraer el catálogo de ramos desde la plataforma oficial de la universidad, junto con el *dataset* resultante listo para ser analizado.

# 📂 Contenido del Repositorio

* `scrapping.py`: Script automatizado que utiliza `curl_cffi` y `BeautifulSoup` para extraer los datos, utilizando un método de búsqueda recursiva.
* `cursos_uc_2026-2.txt`: Dataset (archivo plano TSV) con los cursos consolidados correspondientes al segundo semestre de 2026, separados por tabulaciones.

## 🚀 Cómo usar el script

Para ejecutar el scraper por tu cuenta, necesitas instalar las dependencias en tu entorno virtual:

```bash
pip install curl_cffi beautifulsoup4
```

Luego solo debes ejecutar el archivo sin argumentos:

```bash
python scrapping.py
```

## Aviso:

* **Uso Ético:** Este proyecto fue creado con fines estrictamente educativos y de apoyo a la comunidad estudiantil para facilitar el análisis de datos académicos como remplazo de la API OFICIAL DE BUSCACURSOS. Si decides usar o modificar el script, te pedimos encarecidamente que **mantengas las pausas en el código (`time.sleep`)** y lo ejecutes en horarios de baja demanda. No satures la infraestructura de la universidad.
* **Takedown Policy:** Este es un proyecto independiente y NO ES OFICIAL. En caso de existir cualquier requerimiento, queja o solicitud oficial por parte de la Dirección de Informática o cualquier otra entidad de la **Pontificia Universidad Católica de Chile (UC)** , este repositorio y todos los datos contenidos en él serán dados de baja y eliminados inmediatamente.

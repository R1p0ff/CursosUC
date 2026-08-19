import os
import time
import shutil
from curl_cffi import requests
from bs4 import BeautifulSoup

base_url = "https://buscacursos.uc.cl/"
temp_dir = "temp"
final_file = "cursos_uc_2026-2.txt"

payload = {
    "cxml_semestre": "2026-2",
    "cxml_sigla": "",
    "cxml_nrc": "",
    "cxml_nombre": "",
    "cxml_categoria": "TODOS",
    "cxml_area_fg": "TODOS",
    "cxml_formato_cur": "TODOS",
    "cxml_profesor": "",
    "cxml_campus": "San Joaquín",
    "cxml_unidad_academica": "TODOS",
    "cxml_horario_tipo_busqueda": "si_tenga",
    "cxml_horario_tipo_busqueda_actividad": "TODOS",
    "cxml_periodo": "TODOS",
    "cxml_escuela": "TODOS",
    "cxml_nivel": "TODOS"
}

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"

#! ==== FUNCIONES ====
def explorar_sigla(prefijo, cursos_set):
    payload["cxml_sigla"] = prefijo
    
    try:
        response = requests.get(base_url, params=payload, impersonate="chrome", timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        filas_cursos = soup.find_all('tr', attrs={"class": ["resultadosRowImpar", "resultadosRowPar"]})
        cantidad = len(filas_cursos)
        
        for fila in filas_cursos:
            texto_limpio = fila.get_text(separator="||", strip=True)
            lista_campos = texto_limpio.split("||")
            cursos_set.add(tuple(lista_campos))
            
        print(f"[{prefijo}] Encontrados: {cantidad} | Acumulados en esta letra: {len(cursos_set)}")
        
        if cantidad == 50:
            largo = len(prefijo)
            if largo < 3:
                print(f"    -> [!] Límite para '{prefijo}'. Expandiendo con letras...")
                for char in letters:
                    time.sleep(1)
                    explorar_sigla(prefijo + char, cursos_set)
            elif 3 <= largo < 6:
                print(f"    -> [!] Límite para '{prefijo}'. Expandiendo con números...")
                for num in numbers:
                    time.sleep(1)
                    explorar_sigla(prefijo + num, cursos_set)
            else:
                print(f"    -> [!] Límite para '{prefijo}', deteniendo expansión.")
                
    except Exception as e:
        print(f"[!] Error en la petición para sigla '{prefijo}': {e}")


def extraer_sigla(linea):
    columnas = linea.split('\t')
    if len(columnas) > 1:
        return columnas[1]
    return linea


if __name__ == "__main__":
    sys('clear') if 'sys' in globals() else os.system('clear' if os.name == 'posix' else 'cls')
    print("  /$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$        /$$   /$$  /$$$$$$ ")
    print(" /$$__  $$| $$  | $$| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$      | $$  | $$ /$$__  $$")
    print("| $$  \__/| $$  | $$| $$  \ $$| $$  \__/| $$  \ $$| $$  \__/      | $$  | $$| $$  \__/")
    print("| $$      | $$  | $$| $$$$$$$/|  $$$$$$ | $$  | $$|  $$$$$$       | $$  | $$| $$      ")
    print("| $$      | $$  | $$| $$__  $$ \____  $$| $$  | $$ \____  $$      | $$  | $$| $$      ")
    print("| $$    $$| $$  | $$| $$  \ $$ /$$  \ $$| $$  | $$ /$$  \ $$      | $$  | $$| $$    $$")
    print("|  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$/|  $$$$$$/|  $$$$$$/      |  $$$$$$/|  $$$$$$/")
    print(" \______/  \______/ |__/  |__/ \______/  \______/  \______/        \______/  \______/ ")
                                                                                      
                                                                                      
                                                                                      

    letra_inicio = input("\n\n¿Desde qué letra deseas empezar? (A-Z, presiona Enter para solo hacer merge a los archivos ya generados): ").strip().upper()
    if letra_inicio and letra_inicio in letters:
        indice_inicio = letters.find(letra_inicio)
        letras_a_procesar = letters[indice_inicio:]

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        print("\n=== INICIANDO EXTRACCIÓN ===")
        for char in letras_a_procesar:
            print(f"\n>> Procesando árbol de búsqueda para la letra: {char}")
            cursos_letra_actual = set()
            
            explorar_sigla(char, cursos_letra_actual)
            
            if cursos_letra_actual:
                temp_file = os.path.join(temp_dir, f"cursos_{char}.txt")
                try:
                    with open(temp_file, "w", encoding="utf-8") as f:
                        for curso in cursos_letra_actual:
                            f.write("\t".join(curso) + "\n")
                    print(f"[*] Progreso guardado temporalmente: '{temp_file}'")
                except Exception as e:
                    print(f"[!] Error al guardar archivo temporal {temp_file}: {e}")
            
            time.sleep(1)


    if not os.path.exists(temp_dir):
        print(f"\n[!] Error: La carpeta '{temp_dir}' no existe. No hay datos para consolidar.")
        exit()

    letras_faltantes = []
    for char in letters:
        temp_file = os.path.join(temp_dir, f"cursos_{char}.txt")
        if not os.path.exists(temp_file):
            letras_faltantes.append(char)
    
    if letras_faltantes:
        print(f"\n[!] ADVERTENCIA: Faltan los archivos de las siguientes letras:")
        print(f"    -> {', '.join(letras_faltantes)}")
        print("    Esto significa que la extracción no cubrió el abecedario completo.")
        
        respuesta = input("\n¿Deseas consolidar los archivos existentes de todas formas? (S/N): ").strip().upper()
        if respuesta != 'S':
            print("[!] Proceso cancelado por el usuario. La carpeta temporal se mantendrá intacta.")
            exit()


    print("\n=== INICIANDO CONSOLIDACIÓN ===")
    cursos_unicos = set()
    
    for char in letters:
        temp_file = os.path.join(temp_dir, f"cursos_{char}.txt")
        if os.path.exists(temp_file):
            try:
                with open(temp_file, "r", encoding="utf-8") as f:
                    for linea in f.readlines():
                        linea_limpia = linea.strip()
                        if linea_limpia:
                            cursos_unicos.add(linea_limpia)
                print(f"[Merge] Leído correctamente: {temp_file}")
            except Exception as e:
                print(f"[!] Error al leer {temp_file}: {e}")

    try:
        with open(final_file, "w", encoding="utf-8") as f:
            for curso in sorted(cursos_unicos, key=extraer_sigla):
                f.write(curso + "\n")
        print(f"\n¡Éxito! {len(cursos_unicos)} cursos únicos guardados en '{final_file}'")
    except Exception as e:
        print(f"[!] Error al intentar escribir el archivo final: {e}")

    print("\n=== LIMPIEZA ===")
    try:
        shutil.rmtree(temp_dir)
        print(f"Carpeta temporal '{temp_dir}' eliminada correctamente.")
    except Exception as e:
        print(f"[!] Error al intentar eliminar la carpeta temporal: {e}")
        
    print("=== PROCESO FINALIZADO ===")
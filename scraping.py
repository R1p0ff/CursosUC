import time
from curl_cffi import requests
from bs4 import BeautifulSoup

base_url = "https://buscacursos.uc.cl/"

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
                print(f"    -> [!] Límite alcanzado para '{prefijo}'. Expandiendo con letras...")
                for char in letters:
                    nuevo_prefijo = prefijo + char
                    time.sleep(1)
                    explorar_sigla(nuevo_prefijo, cursos_set)
                    
            elif 3 <= largo < 6:
                print(f"    -> [!] Límite alcanzado para '{prefijo}'. Expandiendo con números...")
                for num in numbers:
                    nuevo_prefijo = prefijo + num
                    time.sleep(1)
                    explorar_sigla(nuevo_prefijo, cursos_set)
                    
            else:
                print(f"    -> [!] Límite alcanzado para '{prefijo}', deteniendo expansión (máximo alcanzado).")
                
    except Exception as e:
        print(f"Error en la petición para sigla '{prefijo}': {e}")


print("Iniciando escaneo profundo del catálogo por bloques de letras...")

total_cursos_global = 0

for char in letters:
    print(f"\n========================================")
    print(f"Iniciando árbol de búsqueda para la: {char}")
    print(f"========================================")
    
    cursos_letra_actual = set()
    
    explorar_sigla(char, cursos_letra_actual)
    
    if len(cursos_letra_actual) > 0:
        file_name = f"cursos_uc_2026-2_{char}.txt"
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                for curso in cursos_letra_actual:
                    linea = "\t".join(curso)
                    f.write(linea + "\n")
            print(f"\n[*] PROGRESO GUARDADO: {len(cursos_letra_actual)} cursos escritos en '{file_name}'")
        except Exception as e:
            print(f"\n[!] Error al intentar escribir el archivo {file_name}: {e}")
            
    total_cursos_global += len(cursos_letra_actual)
    time.sleep(1)

print("\n=== PROCESO FINALIZADO ===")
print(f"Cantidad total de cursos únicos extraídos en todas las letras: {total_cursos_global}")
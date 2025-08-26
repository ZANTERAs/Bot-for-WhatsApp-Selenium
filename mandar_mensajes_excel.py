
import time
import urllib.parse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# =================== CONFIG ===================
EXCEL_PATH   = r"contactos.xlsx"     # Ruta a tu Excel
SHEET_NAME   = 0                     # Nombre de hoja o índice (0 = primera)
NAME_COL     = "A"                   # Columna con NOMBRE (por letra "A" o por nombre exacto)
PHONE_COL    = "B"                   # Columna con TELÉFONO (por letra "B" o por nombre exacto)

MENSAJE_BASE = "¡Hola {nombre}! Te escribimos de *La Tregua*. ¿Cómo estás?"

MAX_WAIT   = 30   # segundos para esperar carga de chat
PAUSA_ENTRE_MENSAJES = 5
# (Opcional) Mantener sesión de WhatsApp sin escanear QR cada vez:
USER_DATA_DIR = None   # e.g. r"C:\Users\TUUSUARIO\AppData\Local\Google\Chrome\User Data"
PROFILE_DIR   = None   # e.g. "Default"
# =============================================

def read_excel_contacts(path, sheet, name_col, phone_col):
    # Permitir referir a columnas por letra (A,B,...) o por encabezado
    df = pd.read_excel(path, sheet_name=sheet, header=None)
    # Si son letras, mapear A->0, B->1, ...
    def col_index(c):
        if isinstance(c, str) and c.isalpha():
            return ord(c.upper()) - ord('A')
        return c  # ya sería índice o nombre
    n_idx = col_index(name_col)
    p_idx = col_index(phone_col)
    # Extraer columnas
    names = df.iloc[:, n_idx].astype(str).fillna("").str.strip()
    phones = df.iloc[:, p_idx].astype(str).str.replace(r"\D", "", regex=True).str.strip()
    # Filtrar filas vacías o sin teléfono
    out = pd.DataFrame({"nombre": names, "telefono": phones})
    # Mantener sólo números no vacíos
    out = out[out["telefono"].str.len() >= 10].copy()
    # El Excel ya está en formato internacional (E.164) según el usuario, así que no normalizamos
    out.drop_duplicates(subset=["telefono"], inplace=True)
    return out.reset_index(drop=True)

def build_driver():
    chrome_options = Options()
    if USER_DATA_DIR:
        chrome_options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
    if PROFILE_DIR:
        chrome_options.add_argument(f"--profile-directory={PROFILE_DIR}")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def esperar_chat(driver, timeout):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//*[@contenteditable="true"]'))
    )

def enviar_mensaje(driver, numero: str, texto: str, timeout: int = 30) -> bool:
    try:
        url = f"https://web.whatsapp.com/send?phone={numero}&text={urllib.parse.quote(texto)}&type=phone_number&app_absent=0"
        driver.get(url)
        esperar_chat(driver, timeout)
        box = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//*[@contenteditable="true"]'))
        )
        box.send_keys(Keys.ENTER)
        time.sleep(2)
        return True
    except Exception as e:
        print(f"❌ Error con {numero}: {e}")
        return False

def main():
    contactos = read_excel_contacts(EXCEL_PATH, SHEET_NAME, NAME_COL, PHONE_COL)
    print(f"[INFO] Contactos cargados: {len(contactos)}")
    contactos.to_csv("contactos_leidos_desde_excel.csv", index=False, encoding="utf-8-sig")

    driver = build_driver()
    driver.get("https://web.whatsapp.com")
    print("🔒 Escaneá el código QR en WhatsApp Web y luego presioná ENTER...")
    input()

    ok, err = 0, 0
    resultados = []
    for i, row in contactos.iterrows():
        nombre = row.get("nombre", "").strip()
        numero = row["telefono"].strip()
        # Personalización simple
        mensaje = MENSAJE_BASE.format(nombre=nombre if nombre else "👋")
        print(f"\n➡️ [{i+1}/{len(contactos)}] Enviando a {numero} ({nombre})...")
        if enviar_mensaje(driver, numero, mensaje, timeout=MAX_WAIT):
            print("✅ Enviado")
            ok += 1
            resultados.append({"telefono": numero, "nombre": nombre, "status": "ENVIADO"})
        else:
            print("⚠️ Falló")
            err += 1
            resultados.append({"telefono": numero, "nombre": nombre, "status": "ERROR"})
        time.sleep(PAUSA_ENTRE_MENSAJES)

    driver.quit()
    pd.DataFrame(resultados).to_csv("resultado_envios_desde_excel.csv", index=False, encoding="utf-8-sig")
    print(f"\n🏁 Listo. OK: {ok} | Errores: {err}")

if __name__ == "__main__":
    main()

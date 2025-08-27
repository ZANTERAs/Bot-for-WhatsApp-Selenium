import json
import time
import urllib.parse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Leer configuración desde config.json
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

EXCEL_PATH   = cfg["EXCEL_PATH"]
SHEET_NAME   = cfg["SHEET_NAME"]
NAME_COL     = cfg["NAME_COL"]
PHONE_COL    = cfg["PHONE_COL"]
MENSAJE_BASE = cfg["MENSAJE_BASE"]

MAX_WAIT   = 30                     # segundos para esperar carga de chat
PAUSA_ENTRE_MENSAJES = 2            # segundos entre envíos
PREFILL_TEXT_PARAM = True           # True: usa ?text=... en la URL; False: tipea luego en la caja
# (Opcional) Mantener sesión:
USER_DATA_DIR = None   # e.g. r"C:\\Users\\TUUSUARIO\\AppData\\Local\\Google\\Chrome\\User Data"
PROFILE_DIR   = None   # e.g. "Default"
# =============================================

SEND_ARIA_LABELS = [
    "Send", "Enviar", "Enviar mensaje", "Enviar mensagem", "Kirim", "Invia", "Send message"
]

def read_excel_contacts(path, sheet, name_col, phone_col):
    df = pd.read_excel(path, sheet_name=sheet, header=None)
    def col_index(c):
        if isinstance(c, str) and c.isalpha():
            return ord(c.upper()) - ord('A')
        return c
    n_idx = col_index(name_col)
    p_idx = col_index(phone_col)
    names = df.iloc[:, n_idx].astype(str).fillna("").str.strip()
    phones = df.iloc[:, p_idx].astype(str).str.replace(r"\\D", "", regex=True).str.strip()
    out = pd.DataFrame({"nombre": names, "telefono": phones})
    out = out[out["telefono"].str.len() >= 10].copy()
    out.drop_duplicates(subset=["telefono"], inplace=True)
    return out.reset_index(drop=True)

def build_driver():
    chrome_options = Options()
    if USER_DATA_DIR:
        chrome_options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
    if PROFILE_DIR:
        chrome_options.add_argument(f"--profile-directory={PROFILE_DIR}")
    chrome_options.add_argument("--start-maximized")
    return webdriver.Chrome(options=chrome_options)

def wait_chat_ready(driver, timeout):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//footer//div[@contenteditable='true']"))
    )

def find_message_box(driver, timeout):
    candidates = [
        (By.XPATH, "//footer//div[@contenteditable='true']"),
        (By.XPATH, "(//div[@contenteditable='true'])[last()]"),
        (By.CSS_SELECTOR, "footer div[contenteditable='true']"),
        (By.CSS_SELECTOR, "div[contenteditable='true'][data-tab]"),
    ]
    for by, sel in candidates:
        try:
            el = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, sel)))
            return el
        except Exception:
            continue
    return driver.switch_to.active_element

def find_send_button(driver, timeout):
    selectors = [
        (By.CSS_SELECTOR, "footer [data-icon='send']"),
        (By.XPATH, "//footer//span[@data-icon='send']/ancestor::button[1]"),
        (By.XPATH, "//button[.//span[@data-icon='send']]"),
    ]
    for label in SEND_ARIA_LABELS:
        selectors.append((By.XPATH, f"//footer//button[@aria-label='{label}']"))
    for by, sel in selectors:
        try:
            btn = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, sel)))
            return btn
        except Exception:
            continue
    return None

def ensure_text_and_send(driver, message, timeout):
    box = find_message_box(driver, timeout)
    try:
        box.click()
    except Exception:
        pass
    if not PREFILL_TEXT_PARAM:
        box.send_keys(Keys.CONTROL, "a")
        box.send_keys(Keys.BACKSPACE)
        box.send_keys(message)
        time.sleep(0.5)
    btn = find_send_button(driver, timeout=5)
    if btn:
        try:
            btn.click()
            return True
        except Exception:
            pass
    try:
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        return True
    except Exception:
        try:
            box.send_keys(Keys.ENTER)
            return True
        except Exception:
            return False

def enviar_mensaje(driver, numero: str, texto: str, timeout: int = 30) -> bool:
    try:
        if PREFILL_TEXT_PARAM:
            url = f"https://web.whatsapp.com/send?phone={numero}&text={urllib.parse.quote(texto)}&type=phone_number&app_absent=0"
        else:
            url = f"https://web.whatsapp.com/send?phone={numero}&type=phone_number&app_absent=0"
        driver.get(url)
        wait_chat_ready(driver, timeout)
        ok = ensure_text_and_send(driver, texto, timeout)
        time.sleep(1)
        return ok
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
        mensaje = MENSAJE_BASE.format(nombre=nombre if nombre else "👋")
        print(f"\\n➡️ [{i+1}/{len(contactos)}] Enviando a {numero} ({nombre})...")
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
    print(f"\\n🏁 Listo. OK: {ok} | Errores: {err}")

if __name__ == "__main__":
    main()

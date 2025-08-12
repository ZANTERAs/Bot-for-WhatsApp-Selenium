from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Cargar números desde archivo
with open("contactos.txt", "r", encoding="utf-8") as f:
    numeros = [line.strip() for line in f.readlines() if line.strip()]

mensaje = "¡Hola! Este es un mensaje automático con imagen 📷"
ruta_imagen = os.path.abspath("imagen.jpg")

# Inicializar el navegador
driver = webdriver.Chrome()  # Asegurate de tener chromedriver en el mismo directorio o en el PATH
driver.get("https://web.whatsapp.com")

print("🔒 Escaneá el código QR en WhatsApp Web y luego presioná ENTER...")
input()  # Esperar al usuario

# WebDriverWait
wait = WebDriverWait(driver, 30)

for numero in numeros:
    try:
        print(f"\n➡️ Enviando a {numero}...")
        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensaje}"
        driver.get(url)
        time.sleep(8)  # Esperar que cargue el chat

        # Verificar si el chat cargó (número válido)
        if "send?phone=" in driver.current_url and "app" not in driver.current_url:
            print(f"⚠️ {numero} no tiene WhatsApp o no está registrado.")
            continue

        # Adjuntar imagen
        clip_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[2]/div/div[1]/button/span')))
        clip_btn.click()
        time.sleep(3)

        # Input de archivo
        img_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@type="file"]')))
        
        img_input.send_keys(ruta_imagen)
        time.sleep(5)

        enviar_img_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div/span')
        ))
        enviar_img_btn.click()
        print("🖼️ Imagen enviada.")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error con {numero}: {e}")
        continue

print("\n🏁 Proceso finalizado.")
driver.quit()


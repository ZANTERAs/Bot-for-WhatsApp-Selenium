# 📲 Bot de WhatsApp con Selenium / WhatsApp Bot with Selenium

Este script automatiza el envío de mensajes de texto e imágenes a múltiples contactos de WhatsApp Web usando **Python** y **Selenium**.

This script automates sending text messages and images to multiple WhatsApp Web contacts using **Python** and **Selenium**.

---

## 🚀 Características / Features

- 📩 Envío de mensajes de texto / Send text messages
- 🖼️ Envío de imágenes / Send images
- 📂 Lectura de contactos desde `contactos.txt` / Read contacts from `contactos.txt`
- ⏳ Esperas dinámicas para evitar errores / Dynamic waits to prevent errors
- 🛡️ Manejo básico de errores / Basic error handling

---

## 📦 Requisitos / Requirements

- **Python 3.7+**
- **Google Chrome**
- **ChromeDriver** (versión compatible con tu Chrome / matching your Chrome version)  
  👉 [Descargar ChromeDriver / Download ChromeDriver](https://chromedriver.chromium.org/downloads)
- Paquetes Python / Python packages:
  ```bash
  pip install selenium

📁 Estructura del Proyecto / Project Structure

📂 proyecto / project
 ├── enviar_whatsapp.py     # Script principal / Main script
 ├── contactos.txt          # Lista de contactos / Contact list
 ├── imagen.jpg             # Imagen a enviar / Image to send
 └── chromedriver.exe       # Driver de Chrome / Chrome driver

📝 Formato de contactos.txt / contactos.txt Format

Cada número debe estar en formato internacional sin el símbolo +.
Each number must be in international format without the + symbol.

Ejemplo / Example:

5491123456789
5491167890123

⚠️ Advertencias / Warnings
❌ No uses este script para spam masivo o WhatsApp puede bloquear tu cuenta.
❌ Do not use this script for mass spam or WhatsApp may block your account.

📶 Requiere conexión estable a internet.
📶 Requires a stable internet connection.

🛠 Los selectores de elementos pueden cambiar si WhatsApp Web actualiza su interfaz.
🛠 Element selectors may change if WhatsApp Web updates its interface.

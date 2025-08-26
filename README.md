
# 📌 README – WhatsApp Bulk Sender desde Excel  

## 🇪🇸 Español  

### Descripción  
Este script permite enviar **mensajes personalizados de WhatsApp** a una lista de contactos guardados en un archivo **Excel**.  
- La **columna A** contiene los **nombres**.  
- La **columna B** contiene los **números de teléfono** en formato internacional (ejemplo para Argentina: `54911XXXXXXXX`).  
- El mensaje se personaliza automáticamente con el nombre de cada persona.  

### Requisitos  
- Python 3.9 o superior  
- Google Chrome instalado  
- Librerías:  
  ```bash
  pip install -r requirements_mensajes_excel.txt
  ```  

### Configuración  
En el archivo `mandar_mensajes_excel.py`, editar:  
```python
EXCEL_PATH   = r"C:\ruta\a\contactos.xlsx"   # ruta a tu archivo
SHEET_NAME   = 0                                # nombre o índice de hoja
NAME_COL     = "A"                              # columna con nombres
PHONE_COL    = "B"                              # columna con teléfonos
MENSAJE_BASE = "¡Hola {nombre}! Te escribimos de *La Tregua*. ¿Cómo estás?"
```

⚙️ Opciones extra:  
- Guardar sesión de Chrome (no volver a escanear QR):  
  ```python
  USER_DATA_DIR = r"C:\Users\TUUSUARIO\AppData\Local\Google\Chrome\User Data"
  PROFILE_DIR   = "Default"
  ```  

### Uso  
1. Ejecutar el script:  
   ```bash
   python mandar_mensajes_excel.py
   ```  
2. Se abrirá WhatsApp Web.  
3. Escanear el código QR (si no está la sesión guardada).  
4. Presionar **ENTER** en la consola.  
5. El programa enviará los mensajes uno por uno.  

### Salidas  
- `contactos_leidos_desde_excel.csv` → vista previa de los contactos leídos.  
- `resultado_envios_desde_excel.csv` → log con estado de cada envío (ENVIADO/ERROR).  


---

## 🇬🇧 English  

### Description  
This script allows you to send **personalized WhatsApp messages** to a list of contacts stored in an **Excel file**.  
- **Column A** contains the **names**.  
- **Column B** contains the **phone numbers** in international format (for Argentina: `54911XXXXXXXX`).  
- The message is automatically customized with each contact’s name.  

### Requirements  
- Python 3.9 or higher  
- Google Chrome installed  
- Libraries:  
  ```bash
  pip install -r requirements_mensajes_excel.txt
  ```  

### Configuration  
In the `mandar_mensajes_excel.py` file, edit:  
```python
EXCEL_PATH   = r"C:\path\to\contacts.xlsx"   # path to your Excel file
SHEET_NAME   = 0                                # sheet name or index
NAME_COL     = "A"                              # column with names
PHONE_COL    = "B"                              # column with phone numbers
MENSAJE_BASE = "Hello {nombre}! This is a message from *La Tregua*. How are you?"
```

⚙️ Extra options:  
- Keep Chrome session (no need to scan QR every time):  
  ```python
  USER_DATA_DIR = r"C:\Users\YOURUSER\AppData\Local\Google\Chrome\User Data"
  PROFILE_DIR   = "Default"
  ```  

### Usage  
1. Run the script:  
   ```bash
   python mandar_mensajes_excel.py
   ```  
2. WhatsApp Web will open.  
3. Scan the QR code (if not already logged in).  
4. Press **ENTER** in the console.  
5. The program will send the messages one by one.  

### Outputs  
- `contactos_leidos_desde_excel.csv` → preview of contacts read.  
- `resultado_envios_desde_excel.csv` → log with status of each send (SENT/ERROR).  

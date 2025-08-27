
# 📌 README – WhatsApp Bulk Sender desde Excel con Configuración Externa  

## 🇪🇸 Español  

### Descripción  
Este script permite enviar **mensajes personalizados o masivos de WhatsApp** a una lista de contactos guardados en un archivo **Excel**.  
La configuración (ruta del Excel, columnas, texto del mensaje, etc.) se guarda en un archivo externo `config.json`, lo que hace más fácil modificarla sin tocar el código.  

### Requisitos  
- Python 3.9 o superior  
- Google Chrome instalado  
- Librerías necesarias:  
  ```bash
  pip install selenium pandas openpyxl
  ```  

### Archivos principales  
- `mandar_mensajes_excel.py` → Script principal en Python.  
- `config.json` → Archivo de configuración editable por el usuario.  

### Configuración (`config.json`)  
Ejemplo de archivo:  
```json
{
  "EXCEL_PATH": "C:/Users/santi/La Tregua/Hoja de cálculo sin título.xlsx",
  "SHEET_NAME": 0,
  "NAME_COL": "A",
  "PHONE_COL": "B",
  "MENSAJE_BASE": "Hola soy Adrián de La Tregua - Balneario Marisol…\nTe quería informar el costo de la Temporada 2026.\nLa misma será desarrollada del 11 al 31/01\nAlojamiento con Pensión Completa\nMonto por persona por día Mayor 3 años $ 45.000.-\nDescuentos: Socio Adherente 10% / Flia más 5 personas 5%\nDatos de CONTACTO:\nCarina 1169570313\nFacebook LaTregua.org.ar / Instagram latregua.ofical"
}
```

- `EXCEL_PATH` → Ruta del archivo Excel con contactos.  
- `SHEET_NAME` → Nombre o índice de la hoja (0 = primera hoja).  
- `NAME_COL` → Columna con nombres (ej. `"A"`).  
- `PHONE_COL` → Columna con teléfonos (ej. `"B"`) en formato internacional E.164 (`54911XXXXXXXX`).  
- `MENSAJE_BASE` → Texto del mensaje a enviar (puede incluir saltos de línea con `\n`).  

### Uso  
1. Editar el archivo `config.json` con tu ruta de Excel y mensaje deseado.  
2. Ejecutar el script:  
   ```bash
   python mandar_mensajes_excel.py
   ```  
3. Se abrirá WhatsApp Web en Chrome.  
4. Escanear el código QR (si no está guardada la sesión).  
5. Presionar **ENTER** en la consola.  
6. El programa enviará el mensaje a todos los contactos listados.  

### Resultados  
- `contactos_leidos_desde_excel.csv` → vista previa de los contactos leídos.  
- `resultado_envios_desde_excel.csv` → log con estado de cada envío (ENVIADO/ERROR).  

---

## 🇬🇧 English  

### Description  
This script allows you to send **personalized or bulk WhatsApp messages** to a list of contacts stored in an **Excel file**.  
The configuration (Excel path, sheet, columns, message text, etc.) is stored in an external file `config.json`, so you can change it without modifying the code.  

### Requirements  
- Python 3.9 or higher  
- Google Chrome installed  
- Required libraries:  
  ```bash
  pip install selenium pandas openpyxl
  ```  

### Main files  
- `mandar_mensajes_excel.py` → Main Python script.  
- `config.json` → User-editable configuration file.  

### Configuration (`config.json`)  
Example:  
```json
{
  "EXCEL_PATH": "C:/Users/santi/La Tregua/Hoja de cálculo sin título.xlsx",
  "SHEET_NAME": 0,
  "NAME_COL": "A",
  "PHONE_COL": "B",
  "MENSAJE_BASE": "Hello, I’m Adrián from La Tregua - Balneario Marisol…\nI wanted to inform you about the cost of the 2026 Season.\nIt will take place from Jan 11 to Jan 31\nAccommodation with Full Board\nPrice per person per day (3+ years): $45,000\nDiscounts: 10% for Members / 5% for families of 5+\nContact:\nCarina 1169570313\nFacebook LaTregua.org.ar / Instagram latregua.ofical"
}
```

- `EXCEL_PATH` → Path to the Excel file with contacts.  
- `SHEET_NAME` → Sheet name or index (0 = first).  
- `NAME_COL` → Column with names (e.g. `"A"`).  
- `PHONE_COL` → Column with phone numbers (international E.164 format: `54911XXXXXXXX`).  
- `MENSAJE_BASE` → Message text (may include line breaks with `\n`).  

### Usage  
1. Edit `config.json` with your Excel path and desired message.  
2. Run the script:  
   ```bash
   python mandar_mensajes_excel.py
   ```  
3. WhatsApp Web will open in Chrome.  
4. Scan the QR code (if not already logged in).  
5. Press **ENTER** in the console.  
6. The program will send the message to all listed contacts.  

### Outputs  
- `contactos_leidos_desde_excel.csv` → preview of contacts read.  
- `resultado_envios_desde_excel.csv` → log with each send status (SENT/ERROR).  

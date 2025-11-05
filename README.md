# PDFVault
A secure PDF management tool that scans, sanitizes, and protects your documents. Upload your PDFs, and PDFVault ensures they’re virus-free, free of hidden scripts or attachments, stripped of sensitive metadata, and even generates a preview thumbnail for quick browsing. Perfect for safe sharing and storage of sensitive documents.

# Installation

```bash
sudo apt update
sudo apt install -y qpdf clamav clamav-daemon exiftool poppler-utils libqpdf-dev libmagic1
```

```bash
python3 -m pip install -r requirements.txt
```

```bash
python3 pdfVault.PY
```

# Output 

```bash
$ python3 pdfVault.PY
[*] Starting Flask app on http://0.0.0.0:8080
 * Serving Flask app 'pdfVault'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://IP:8080
Press CTRL+C to quit
IP - - [05/Nov/2025 11:25:46] "GET / HTTP/1.1" 200 -
IP - - [05/Nov/2025 11:25:46] "GET /favicon.ico HTTP/1.1" 404 -
IP - - [05/Nov/2025 11:25:54] "GET / HTTP/1.1" 200 -

[UPLOAD] Received file: 1738421237842.pdf
[TEMP] Saved temporarily at: /tmp/tmpob45w22q/1738421237842.pdf
[MIME] MIME type valid
[ClamAV] /tmp/tmpob45w22q/1738421237842.pdf: OK
[ClamAV] 
[ClamAV] ----------- SCAN SUMMARY -----------
[ClamAV] Known viruses: 8708684
[ClamAV] Engine version: 1.4.3
[ClamAV] Scanned directories: 0
[ClamAV] Scanned files: 1
[ClamAV] Infected files: 0
[ClamAV] Data scanned: 76.50 MB
[ClamAV] Data read: 5.73 MB (ratio 13.34:1)
[ClamAV] Time: 14.863 sec (0 m 14 s)
[ClamAV] Start Date: 2025:11:05 11:25:58
[ClamAV] End Date:   2025:11:05 11:26:13
[ClamAV] ClamAV scan clean
[StaticCheck] No embedded JavaScript detected
[Attachments] No embedded attachments detected
[ExifTool] Warning: [minor] ExifTool PDF edits are reversible. Deleted tags may be recovered! - /tmp/tmpob45w22q/1738421237842.pdf
[ExifTool] 1 image files updated
[Sanitize] PDF sanitized successfully
[UPLOAD] Clean file saved to: uploads/1738421237842.pdf
[Thumbnail] Saved thumbnail to: thumbnails/1738421237842.png
```

### **1\. Upload**

-   You select a PDF and upload it via the web form.

-   The file is first **saved temporarily** in a secure temp folder, so nothing is immediately moved into the main storage.

-   The app logs the filename and the temporary path in the terminal.

* * * * *

### **2\. MIME type check**

-   PDFVault uses `python-magic` to detect the **true file type**.

-   If the file isn't a PDF (`application/pdf`), it's **rejected immediately**.

-   This prevents attackers from uploading disguised malware like `.exe` or `.js` files renamed as `.pdf`.

* * * * *

### **3\. ClamAV scan**

-   The temporary PDF is scanned with **ClamAV**, a popular antivirus tool.

-   It runs a **full virus scan** and logs the process in real-time to your terminal.

-   If ClamAV finds malware, the file is **rejected**.

-   If clean, it moves to the next step.

* * * * *

### **4\. Static PDF inspection**

-   Using `pikepdf`, PDFVault inspects the PDF's internal objects.

-   It looks for **embedded JavaScript**, `/JS` objects, or `/JavaScript` actions.

-   JavaScript in PDFs is a common way attackers try to exploit readers.

-   If suspicious scripts are detected, the PDF is **rejected**.

* * * * *

### **5\. Embedded attachments check**

-   PDFVault checks the PDF catalog for **embedded files** using `pikepdf`.

-   Attachments can contain malware, so PDFs with embedded files are **rejected**.

* * * * *

### **6\. Metadata stripping**

-   Using `exiftool`, PDFVault removes all **metadata**: author info, edit history, timestamps, and anything else that could leak sensitive info.

-   It logs minor warnings, but continues if stripping is successful.

* * * * *

### **7\. PDF sanitization**

-   `qpdf` is used to **sanitize and linearize the PDF**, which:

    -   Fixes malformed objects

    -   Ensures a standard structure

    -   Removes potential hidden threats in the file structure

-   If qpdf fails, the PDF is **rejected**.

* * * * *

### **8\. Thumbnail generation**

-   After the PDF is clean, `pdf2image` converts the **first page into a PNG thumbnail**.

-   This thumbnail is saved in a `thumbnails` folder and used to visually display the PDF in the web interface.

* * * * *

### **9\. Move to storage**

-   The clean PDF is moved from the temp folder to the main `uploads` folder.

-   Now it's safe to browse, download, or share.

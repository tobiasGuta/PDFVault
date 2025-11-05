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

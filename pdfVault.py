from flask import Flask, request, send_from_directory
import os
import subprocess
import tempfile
import shutil
import magic
import pikepdf
from pdf2image import convert_from_path

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
THUMB_FOLDER = 'thumbnails'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMB_FOLDER, exist_ok=True)

def stream_process(cmd, prefix="[process]"):
    """Run a subprocess and stream its output live to the terminal."""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    for line in process.stdout:
        print(f"{prefix} {line.strip()}")
    process.wait()
    return process.returncode

def validate_mime(filepath):
    mime = magic.from_file(filepath, mime=True)
    if mime != 'application/pdf':
        return False, f"Invalid MIME type: {mime}"
    return True, "MIME type valid"

def static_check_pdf(filepath):
    try:
        pdf = pikepdf.open(filepath)
        for obj in pdf.pages:
            for key, val in obj.obj.items():
                if "/JS" in str(key) or "/JavaScript" in str(key):
                    return False, f"Suspicious JavaScript found in object: {key}"
        return True, "No embedded JavaScript detected"
    except Exception as e:
        return False, f"Error inspecting PDF: {e}"

def check_attachments(filepath):
    try:
        pdf = pikepdf.open(filepath)
        root = pdf.trailer['/Root']
        if '/Names' in root:
            names = root['/Names']
            if '/EmbeddedFiles' in names:
                return False, "PDF contains embedded attachments"
        return True, "No embedded attachments detected"
    except KeyError:
        return True, "No embedded attachments detected"
    except Exception as e:
        return False, f"Error checking attachments: {e}"

def strip_metadata(filepath):
    stream_process(['exiftool', '-all=', '-overwrite_original', filepath], prefix="[ExifTool]")

def scan_with_clamav(filepath):
    exit_code = stream_process(['clamscan', filepath], prefix="[ClamAV]")
    if exit_code == 0:
        return True, "ClamAV scan clean"
    else:
        return False, "ClamAV detected a virus"

def sanitize_pdf(filepath):
    clean_path = filepath + "_clean.pdf"
    exit_code = stream_process(['qpdf', '--linearize', filepath, clean_path], prefix="[qpdf]")
    if exit_code != 0:
        return None, "qpdf encountered an issue"
    return clean_path, "PDF sanitized successfully"

def generate_thumbnail(pdf_path, thumb_path):
    """Generate a thumbnail (first page) from a PDF."""
    try:
        pages = convert_from_path(pdf_path, dpi=100, first_page=1, last_page=1)
        if pages:
            pages[0].save(thumb_path, 'PNG')
            print(f"[Thumbnail] Saved thumbnail to: {thumb_path}")
            return True
    except Exception as e:
        print(f"[Thumbnail] Error generating thumbnail: {e}")
    return False

@app.route('/')
def home():
    files = os.listdir(UPLOAD_FOLDER)
    links = ""
    for f in files:
        thumb_name = f.rsplit('.', 1)[0] + '.png'
        thumb_path = os.path.join(THUMB_FOLDER, thumb_name)
        if os.path.exists(thumb_path):
            links += f'<li><img src="/thumb/{thumb_name}" width="100"><br><a href="/pdf/{f}">{f}</a></li>'
        else:
            links += f'<li>{f}</li>'
    return f'''
    <h2>PDF Safe Vault</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="pdf" accept=".pdf">
        <input type="submit" value="Upload">
    </form>
    <ul>{links}</ul>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['pdf']
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = os.path.join(tmpdir, file.filename)
        file.save(temp_path)
        print(f"\n[UPLOAD] Received file: {file.filename}")
        print(f"[TEMP] Saved temporarily at: {temp_path}")

        valid, msg = validate_mime(temp_path)
        print(f"[MIME] {msg}")
        if not valid:
            return f"File rejected: {msg}"

        valid, msg = scan_with_clamav(temp_path)
        print(f"[ClamAV] {msg}")
        if not valid:
            return f"File rejected: {msg}"

        valid, msg = static_check_pdf(temp_path)
        print(f"[StaticCheck] {msg}")
        if not valid:
            return f"File rejected: {msg}"

        valid, msg = check_attachments(temp_path)
        print(f"[Attachments] {msg}")
        if not valid:
            return f"File rejected: {msg}"

        strip_metadata(temp_path)

        clean_path, msg = sanitize_pdf(temp_path)
        print(f"[Sanitize] {msg}")
        if clean_path is None:
            return f"File rejected: {msg}"

        safe_name = os.path.basename(file.filename)
        final_path = os.path.join(UPLOAD_FOLDER, safe_name)
        shutil.move(clean_path, final_path)
        print(f"[UPLOAD] Clean file saved to: {final_path}")

        # Generate thumbnail
        thumb_name = safe_name.rsplit('.', 1)[0] + '.png'
        thumb_path = os.path.join(THUMB_FOLDER, thumb_name)
        generate_thumbnail(final_path, thumb_path)

    return f"File uploaded, scanned, sanitized, and thumbnail created. <a href='/'>Go back</a>"

@app.route('/pdf/<filename>')
def serve_pdf(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/thumb/<filename>')
def serve_thumbnail(filename):
    return send_from_directory(THUMB_FOLDER, filename)

if __name__ == '__main__':
    print("[*] Starting Flask app on http://0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080)

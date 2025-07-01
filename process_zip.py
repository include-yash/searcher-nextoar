import os
import zipfile
import re
import shutil
from datetime import datetime

LOG_TO_FILE = False  # Set to True if you want to save logs to a .txt file

log_lines = []

def log(msg):
    print(msg)
    log_lines.append(msg)

def extract_fail_ids_from_txt(txt_path):
    fail_ids = []
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        log(f"❌ Error reading TXT file: {e}")
        return []

    board_fail_line = any(re.search(r"#\s*Board\s+fail\s*=\s*\d+", line) for line in lines)
    if not board_fail_line:
        log("⚠️ No '# Board fail = <number>' line found.")
        return []

    count = 1
    for line in lines:
        if re.search(r'\bFail\b', line) or 'Fail' in line:
            match = re.match(r"^\s*(\S+)", line)
            if match:
                full_id = match.group(1)
                if ':' in full_id:
                    parts = full_id.split(':')
                    fail_ids.append(f"{count}:{parts[1].strip()}")
                    count += 1
    return fail_ids

def process_zip(zip_path, results_dir):
    zip_name = os.path.basename(zip_path).replace('.zip', '')
    log(f"\n🔄 Processing ZIP: {zip_name}")
    log("-" * 56)

    extract_folder = os.path.join("temp", zip_name)
    os.makedirs(extract_folder, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
    except Exception as e:
        log(f"❌ Failed to extract ZIP: {e}")
        return

    # Find repairTicket_post.txt
    txt_path = None
    for root, _, files in os.walk(extract_folder):
        for file in files:
            if file == "repairTicket_post.txt":
                txt_path = os.path.join(root, file)
                break

    if not txt_path:
        log(f"❌ 'repairTicket_post.txt' not found in {zip_name}")
        shutil.rmtree(extract_folder, ignore_errors=True)
        return

    log("✅ Found repairTicket_post.txt")

    # Extract Fail IDs
    fail_ids = extract_fail_ids_from_txt(txt_path)
    if not fail_ids:
        log("⚠️ No fail IDs extracted.")
        shutil.rmtree(extract_folder, ignore_errors=True)
        return

    log("✅ Fail IDs Extracted:")
    for fid in fail_ids:
        log(f"   - {fid}")

    # Prepare output directory
    output_folder = os.path.join(results_dir, zip_name)
    os.makedirs(output_folder, exist_ok=True)

    # Search and copy matching images
    for fid in fail_ids:
        _, short_id = fid.split(":")
        found_jpg = found_pgm = False
        for root, _, files in os.walk(extract_folder):
            for file in files:
                if file.startswith("a3dr") and file.endswith(short_id + ".jpg"):
                    shutil.copy2(os.path.join(root, file), os.path.join(output_folder, file))
                    log(f"📁 Copied: {file}")
                    found_jpg = True
                if file.startswith("a3dr") and file.endswith(short_id + ".pgm"):
                    shutil.copy2(os.path.join(root, file), os.path.join(output_folder, file))
                    log(f"📁 Copied: {file}")
                    found_pgm = True

        if not found_jpg:
            log(f"⚠️ Image not found for ID: {short_id} (.jpg)")
        if not found_pgm:
            log(f"⚠️ Image not found for ID: {short_id} (.pgm)")

    log(f"✅ Finished processing: {zip_name}")
    shutil.rmtree(extract_folder, ignore_errors=True)

def write_log_file():
    if LOG_TO_FILE:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = f"process_log_{timestamp}.txt"
        with open(log_file, "w", encoding='utf-8') as f:
            f.write("\n".join(log_lines))
        print(f"\n📝 Log saved to {log_file}")

if __name__ == "__main__":
    input_folder = "input_zips"
    results_folder = "results"
    os.makedirs(results_folder, exist_ok=True)

    zip_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".zip")]
    if not zip_files:
        log("⚠️ No ZIP files found in input_zips/")
    else:
        for file in zip_files:
            zip_path = os.path.join(input_folder, file)
            process_zip(zip_path, results_folder)

    write_log_file()

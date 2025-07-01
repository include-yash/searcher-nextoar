import os
import re
import shutil

def extract_fail_ids_from_txt(txt_path, log):
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

    for line in lines:
        if 'Fail' in line:
            match = re.match(r"^\s*(\S+)", line)
            if match:
                full_id = match.group(1)
                if ':' in full_id:
                    fail_ids.append(full_id)  # store full form like '2:u1601-2'
    return fail_ids

def process_folder(folder_path, destination_root_path):
    log_lines = []
    def log(msg):
        print(msg)
        log_lines.append(msg)

    folder_name = os.path.basename(folder_path.rstrip('/\\'))
    log(f"\n🔄 Processing Folder: {folder_name}")
    log("-" * 56)

    txt_path = None
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file == "repairTicket_post.txt":
                txt_path = os.path.join(root, file)
                break

    if not txt_path:
        log(f"❌ 'repairTicket_post.txt' not found in {folder_name}")
        return "\n".join(log_lines)

    log(f"✅ Found repairTicket_post.txt at: {txt_path}")
    fail_ids = extract_fail_ids_from_txt(txt_path, log)
    if not fail_ids:
        log("⚠️ No fail IDs extracted.")
        return "\n".join(log_lines)

    log("✅ Fail IDs Extracted:")
    for fid in fail_ids:
        log(f"   - {fid}")

    # Only create the output folder if we have valid fail IDs
    output_folder = os.path.join(destination_root_path, folder_name)
    os.makedirs(output_folder, exist_ok=True)
    log(f"📂 Output folder created: {output_folder}")

    for fid in fail_ids:
        prefix, short_id = fid.split(":")
        found_jpg = found_pgm = False
        for root, _, files in os.walk(folder_path):
            for file in files:
                src_path = os.path.join(root, file)
                if file.startswith("a3dr") and file.endswith(short_id + ".jpg"):
                    shutil.copy2(src_path, os.path.join(output_folder, file))
                    log(f"📁 Copied: {file}")
                    found_jpg = True
                if file.startswith("a3dr") and file.endswith(short_id + ".pgm"):
                    shutil.copy2(src_path, os.path.join(output_folder, file))
                    log(f"📁 Copied: {file}")
                    found_pgm = True

        if not found_jpg:
            log(f"⚠️ Image not found for ID: {short_id} (.jpg)")
        if not found_pgm:
            log(f"⚠️ Image not found for ID: {short_id} (.pgm)")

    log(f"✅ Finished processing: {folder_name}")
    log(f"📍 Final output folder: {output_folder}")
    return "\n".join(log_lines)

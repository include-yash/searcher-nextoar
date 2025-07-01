# 🔍 Searcher Nextoar

Automated extraction of failed image entries from `repairTicket_post.txt` inside ZIP archives.

---

## 🚀 Features

- ✅ Supports **multiple ZIP files**
- ✅ Extracts IDs from `repairTicket_post.txt` only if `# Board fail = <number>` is present
- ✅ Finds lines containing the word `Fail` and extracts IDs like `1:u1601-2`
- ✅ Copies only images that:
  - Start with `a3dr`
  - End with the extracted ID
  - Have `.jpg` or `.pgm` extension
- ✅ Saves results in structured folders inside `/results/`
- ✅ Detailed logs for:
  - Fail IDs found
  - Copied image files
  - Missing image warnings
- ✅ Robust error handling

---

## 📁 Folder Structure

```
searcher-nextoar/
├── input_zips/
│   ├── example1.zip
│   ├── example2.zip
├── results/
│   └── <zip_name>/
│       ├── a3dr_543_2-<id>.jpg
│       └── a3dr_543_2-<id>.pgm
├── temp/
├── process_zip.py
├── .gitignore
├── README.md
```

---

## 🛠️ Requirements

- Python 3.7 or higher

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# or
source venv/bin/activate   # macOS/Linux
```

---

## ▶️ How to Use

1. Clone the repo:

```bash
git clone https://github.com/include-yash/searcher-nextoar.git
cd searcher-nextoar
```

2. Place `.zip` files in the `input_zips/` folder.

3. Run the script:

```bash
python process_zip.py
```

---

## ✅ What Happens

* Extracts each ZIP to a temp folder
* Looks for `repairTicket_post.txt`
* If `# Board fail = <number>` is found, it:
  * Parses lines with the keyword `Fail`
  * Extracts IDs like `2:u1601-2`, `3:q1003-2`, etc.
* Searches for files matching:
  * Starts with `a3dr`
  * Ends with the extracted ID
  * Has `.jpg` or `.pgm` extension
* Copies them into: `results/<zip_name>/`

---

## 🧾 Sample Output

```
🔄 Processing ZIP: BSMWAOI01[@$@]2025-06-05-03-42-26
--------------------------------------------------------
✅ Found repairTicket_post.txt
✅ Fail IDs Extracted:
   - 1:u1601-2
   - 2:q1003-2
📁 Copied: a3dr_543_2-u1601-2.jpg
📁 Copied: a3dr_543_2-u1601-2.pgm
📁 Copied: a3dr_543_2-q1003-2.jpg
⚠️ Image not found for ID: q1003-2 (.pgm)
✅ Finished processing: BSMWAOI01[@$@]2025-06-05-03-42-26
```

---

## ⚠️ Notes

* Only images starting with `a3dr` are copied
* If no `# Board fail =` line is found, nothing is processed
* `temp/` is cleaned automatically after each ZIP
* To save logs to a file, set `LOG_TO_FILE = True` in `process_zip.py`

---

## 📌 Optional Enhancements (coming soon)

* [ ] CSV summary report
* [ ] Subfolder per fail ID
* [ ] CLI arguments
* [ ] GUI version

---

## 👤 Author

**Yash Singh**  
📧
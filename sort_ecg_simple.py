import pandas as pd
import shutil
from pathlib import Path

# ==== EDIT THESE PATHS ====
excel_path = r"D:\ECG_model\Y.xls"
image_folder = Path(r"D:\ECG_model\ECG")
output_folder = Path(r"D:\ECG_model\sorted_ecg")
# ===========================

# Read Excel
df = pd.read_excel(excel_path)

# Rename columns to simple names
df.columns = ["file", "class"]

# Convert numeric file names → IMG#
df["file"] = df["file"].astype(str).str.strip()
df["file"] = "IMG" + df["file"]

# Add common extensions because images may be .jpg or .png
possible_exts = [".jpg", ".jpeg", ".png"]

# Create output folder
output_folder.mkdir(exist_ok=True)

missing = []

# Process each row
for _, row in df.iterrows():
    img_name = row["file"]
    cls = str(row["class"])

    # Create class folder
    class_path = output_folder / cls
    class_path.mkdir(exist_ok=True)

    # Try each extension
    found = None
    for ext in possible_exts:
        p = image_folder / (img_name + ext)
        if p.exists():
            found = p
            break

    if found is None:
        missing.append(img_name)
        continue

    # Copy file
    shutil.copy2(found, class_path / found.name)
    print(f"Copied {found} → class {cls}")

# Save missing images list
with open(output_folder / "missing.txt", "w") as f:
    for m in missing:
        f.write(m + "\n")

print("Done!")

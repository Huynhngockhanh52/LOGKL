# import json
# from pathlib import Path

# DATA_FILE = Path("./settings/log.json")                 # Hard_code path

# def load_json():
#     """Đọc dữ liệu từ file log.json"""
#     if not DATA_FILE.exists():
#         return []
#     with open(DATA_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# def save_json(data):
#     """Ghi dữ liệu vào file log.json"""
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)
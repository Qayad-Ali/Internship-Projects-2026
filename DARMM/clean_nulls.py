import os

count_total = 0
for filename in os.listdir("."):
    if filename.endswith(".py"):
        with open(filename, "rb") as f:
            data = f.read()
        cleaned = data.replace(b"\x00", b"")
        removed = len(data) - len(cleaned)
        if removed > 0:
            with open(filename, "wb") as f:
                f.write(cleaned)
            print(f"{filename}: stripped {removed} null bytes")
            count_total += removed
        else:
            print(f"{filename}: clean")
print(f"\nTotal null bytes removed: {count_total}")
import os
from bs4 import BeautifulSoup

TARGET_DOMAIN = "verdantis-logo"

# Address 1 (India)
OLD_ADDRESS_1_KEY = "Andheri Kurla Road"
NEW_ADDRESS_1 = """Times Square, 3rd Floor, “B” Wing,<br>
Andheri Kurla Road,<br>
Andheri East, Mumbai – 400059"""

# Address 2 (USA)
OLD_ADDRESS_2_KEY = "Princeton, NJ"
NEW_ADDRESS_2 = """500 Alexander Park,<br>
Suite 101,<br>
Princeton, NJ 08540, USA"""

def clean_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")

    modified = False

    # Replace logo image sources
    for tag in soup.find_all(["img", "figure"]):
        tag_text = str(tag)
        if TARGET_DOMAIN in tag_text:
            if tag.name == "img":
                tag["src"] = "assets/logo.png"
                tag.attrs.pop("srcset", None)
                modified = True
            elif tag.name == "figure":
                img = tag.find("img")
                if img and TARGET_DOMAIN in str(img):
                    img["src"] = "assets/logo.png"
                    img.attrs.pop("srcset", None)
                    modified = True

    # Replace address paragraphs
    for p in soup.find_all("p"):
        content = p.decode_contents()

        if OLD_ADDRESS_1_KEY in content:
            p.clear()
            for line in NEW_ADDRESS_1.split("<br>"):
                p.append(line.strip())
                p.append(soup.new_tag("br"))
            p.contents.pop()  # remove last <br>
            modified = True

        elif OLD_ADDRESS_2_KEY in content:
            p.clear()
            for line in NEW_ADDRESS_2.split("<br>"):
                p.append(line.strip())
                p.append(soup.new_tag("br"))
            p.contents.pop()  # remove last <br>
            modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Updated HTML: {filepath}")

def scan_and_clean(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".html"):
                filepath = os.path.join(dirpath, filename)
                clean_html_file(filepath)

if __name__ == "__main__":
    scan_and_clean(".")
    print("Done.")

import fitz
import os
import phonenumbers
import argparse
import json
import re
import sys
import os


########################################################################################################################################################################################################################

image_extensions = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".ico",
    ".jfif", ".webp", ".heif", ".bat", ".raw", ".indd", ".ai",
    ".eps", ".svg"
]

video_extensions = [
    ".mp4", ".mkv", ".flv", ".avi", ".wmv", ".mov", ".webm",
    ".mpeg", ".mpg", ".m4v", ".3gp", ".3g2", ".ogv", ".vob",
    ".qt", ".f4v", ".f4p", ".f4a", ".f4b", ".h264", ".h265",
    ".rm", ".rmvb", ".asf", ".amv", ".m2v", ".svi", ".mxf"
]

audio_extensions = [
    ".mp3", ".wav", ".ogg", ".flac", ".aac", ".wma", ".m4a",
    ".alac", ".aiff", ".caf", ".ac3", ".amr", ".dts", ".ra",
    ".gsm", ".mka", ".opus", ".tta", ".au", ".m4b", ".m4r",
    ".mpc", ".voc", ".qcp"
]

compression_extensions = [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".lz", ".lzma", ".lzo", ".z", ".tgz", ".tbz", ".tar.gz",
                          ".tar.bz2", ".tar.xz", ".s7z", ".ace", ".cab", ".arj", ".jar", ".apk", ".sitx", ".hqx", ".lha", ".lzh", ".alz", ".arc", ".isz", ]

other_bad_extensions = [".exe"]

default_ignore_list = [
    "env",
    ".DS_Store",
    ".git",
    ".env",
    "node_modules",
    "yarn.lock",
    "package-lock.json"
]

phone_country_extension = "US"

########################################################################################################################################################################################################################


def replace_multiple_spaces(text):
    return re.sub(r'\s+', ' ', text)


def find_phone_numbers(text):
    output = []
    for match in phonenumbers.PhoneNumberMatcher(text, phone_country_extension):
        content = str(match.number).split(" ")
        try:
            output.append({
                "code": content[2],
                "number": content[5],
                "raw": str(match.number)
            })
        except Exception as err:
            output.append({
                "raw": str(match.number)
            })
    return output


def find_addresses(text):
    number = r'\d{1,5}'
    street = r'[\w\s\.\-]+'
    city = r'[\w\s\.\-]+'
    state = r'[A-Z]{2}'
    zip_code = r'\d{5}(?:-\d{4})?'
    country = r'(?:[A-Za-z\s\.\-]+)?'
    suite = r'(?:[\w\s\.\-#,]+)?'

    address_pattern = re.compile(
        rf'\b{number}\s{street}(?:\s{suite})?,\s*{city},\s*{state}\s*{country}\s*{zip_code}\b'
    )

    return re.findall(address_pattern, text)


def find_emails(text):
    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    result = re.findall(pattern, text)
    return result


def read_file(path):
    try:
        with open(str(path)) as file:
            content = file.readlines()
        content = [i.strip() for i in content]
        return content
    except Exception as e:
        return path


def read_pdf(pdf_path):
    try:
        output = ""

        doc = fitz.open(str(pdf_path))
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            output = output + "\n" + text

        doc.close()
        return output
    except Exception as e:
        return pdf_path


def has_ext(s, extensions):
    return any(s.lower().endswith(ext.lower()) for ext in extensions)


def not_img_vid_aud(value):
    if has_ext(value, image_extensions):
        return False
    if has_ext(value, video_extensions):
        return False
    if has_ext(value, audio_extensions):
        return False
    if has_ext(value, compression_extensions):
        return False
    if has_ext(value, other_bad_extensions):
        return False
    return True


def main(base_path, ignore_list):
    for root, dirs, files in os.walk(base_path):

        # Ignore specified directories
        dirs[:] = [d for d in dirs if d not in ignore_list]

        for file in files:
            if file in ignore_list:
                continue

            file_path = os.path.join(root, file)

            file_content = []
            if not_img_vid_aud(file_path):
                if has_ext(file_path, [".pdf"]):
                    content = read_pdf(file_path)
                    if (type(file_content) != str):
                        file_content = content.splitlines()
                else:
                    file_content = read_file(file_path)

            entry = {
                "file_path": file_path,
                "numbers": [],
                "emails": [],
                "addresses": [],
                "used": False
            }

            for line in file_content:
                pn = find_phone_numbers(line)
                ea = find_emails(line)
                ha = find_addresses(line)
                
                if len(pn) + len(ea) + len(ha) > 0:
                    entry["used"] = True
                if len(pn) > 0:
                    entry["numbers"] += [f"+{p['code']} {p['number'][:3]}-{p['number'][3:6]}-{p['number'][6:]}" for p in pn]
                if len(ea) > 0:
                    entry["emails"] += [e for e in ea]
                if len(ha) > 0:
                    entry["addresses"] += [a for a in ha]

            # remove duplicates
            entry["numbers"] = list(set(entry["numbers"]))
            entry["emails"] = list(set(entry["emails"]))
            entry["addresses"] = list(set(entry["addresses"]))
            
            # print results, cleanly...
            if entry["used"]:
                for i, (key, value) in enumerate(entry.items()):
                    if key != "used" and value:
                        print(f"{key}: {value}")
                print()


if __name__ == "__main__":
    # define CLI settings
    parser = argparse.ArgumentParser(description="CLI tool to check if any personal information is in a directory")
    parser.add_argument("base_path", type=str, help="Base path for the operation")
    parser.add_argument("--ignore", "--i", type=str, nargs='*', default=default_ignore_list, help="Optional: List of items to ignore")

    args = parser.parse_args()

    if not os.path.exists(args.base_path):
        print(f"The path '{args.base_path}' does not exist.")
        exit(1)

    if args.ignore != default_ignore_list:
        ignores = replace_multiple_spaces(' '.join(args.ignore))
        args.ignore = ignores.split(',')

    main(args.base_path, args.ignore)


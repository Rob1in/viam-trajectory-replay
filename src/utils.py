import re

def sort_jpeg_names(jpeg_files):
    def extract_numeric_part(filename):
        match = re.match(r'image(\d+)\.jpg', filename)
        if match:
            return int(match.group(1))
        
        return -1  # Return 0 if the format doesn't match

    return sorted(jpeg_files, key=extract_numeric_part)
import base64
import zlib
import urllib.parse

def decode_diagram(encoded_data):
    try:
        # Draw.io data is often URI encoded, then Base64 encoded, then Deflate compressed (raw, no header)
        # 1. URI Decode (sometimes needed, sometimes not, let's try raw first)
        # 2. Base64 Decode
        compressed_data = base64.b64decode(encoded_data)
        # 3. Inflate (raw deflate, so negative window size)
        xml_data = zlib.decompress(compressed_data, -15)
        return xml_data.decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

# Content from aws-simple-architecture.drawio
with open("/Users/vinayakpawar/Desktop/Work/Projects/Github_Projects/Arcgen-Natural Language (NL) into System Design Architecture/Study-Material/drawio-diagrams-dev/examples/aws-simple-architecture.drawio", "r") as f:
    # Read the file, extract the base64 part (it's usually inside <diagram>...</diagram>)
    content = f.read()
    import re
    match = re.search(r'<diagram[^>]*>(.*?)</diagram>', content, re.DOTALL)
    if match:
        blob = match.group(1)
        print(decode_diagram(blob))
    else:
        print("No diagram tag found")

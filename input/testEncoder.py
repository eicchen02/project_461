import base64
import zipfile
import sys
import json
import os

def main():
    input = sys.argv[1]
    data = open(input, 'rb').read()
    data_encoded = base64.b64encode(data)
    filename = input.strip('.zip')
    with open(f'{filename}', 'wb') as result:
        result.write(data_encoded)
    result.close()

if __name__ == "__main__":
    main()
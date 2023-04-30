import sys
import os


input = sys.argv[1]

url = os.path.basename(input.strip("\n"))

print(f'Input: {input}')
print(f'URL: {url}')
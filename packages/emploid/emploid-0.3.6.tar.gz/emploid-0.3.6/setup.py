from setuptools import setup
from charset_normalizer import detect

from charset_normalizer import detect

def parse_requirements(filename):
   with open(filename, "rb") as f:
      byte_content = f.read()
      detected = detect(byte_content)  # Detect encoding
      encoding = detected['encoding']  # Get detected encoding
      
      # Decode using the detected encoding
      content = byte_content.decode(encoding)
    
   # Split the content into lines, remove empty lines, and lines starting with #
   return [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]

# Use this function to read requirements.txt
requirements = parse_requirements("requirements.txt")

setup(
   name='emploid',
   version='0.3.6',
   description='A simple to use automation tool for automating web, android and windows proccesses.',
   long_description='A simple to use automation tool for automating web, android and windows proccesses.',
   author='PixQuilly',
   author_email='pixquilly@gmail.com',
   packages=['emploid'],  #same as name
   install_requires=requirements, #external packages as dependencies
)
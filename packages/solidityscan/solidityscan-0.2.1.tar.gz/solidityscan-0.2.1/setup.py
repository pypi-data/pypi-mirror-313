from setuptools import setup, find_packages
import os

def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
        return f.read()

setup(name="solidityscan",
      version="0.2.1",
      description="Get your smart contracts audited by a smarter tool",
      long_description=readme(),
      long_description_content_type='text/markdown',
      url="https://solidityscan.com",
      entry_points={
        'console_scripts': [
            'solidityscan=solidityscan_agent.__init__:solidityscan',
        ],
      },
      python_requires=">=3.6",
      packages=find_packages(),
      install_requires=[
        "anyio==3.6.2",
        "beautifulsoup4==4.12.2",
        "certifi==2023.5.7",
        "chardet==5.1.0",
        "charset-normalizer==2.1.1",
        "click==8.1.3",
        "deep-translator==1.10.1",
        "h11==0.14.0",
        "h2==4.1.0",
        "hpack==4.0.0",
        "hstspreload==2023.1.1",
        "httpcore==0.17.0",
        "httpx==0.24.0",
        "hyperframe==6.0.1",
        "idna==3.4",
        "loguru==0.7.0",
        "requests==2.30.0",
        "rfc3986==2.0.0",
        "ruamel.yaml==0.18.6",
        "ruamel.yaml.clib==0.2.12",
        "sniffio==1.3.0",
        "soupsieve==2.4.1",
        "urllib3==1.26.4",
    ]
)

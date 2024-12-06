from setuptools import setup, find_packages

setup(
    name="jina-segmenter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    author="WSY",
    author_email="wangshuyue@gmail.com",
    description="A text segmentation tool using Jina AI API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wsy/jina-segmenter",
    project_urls={
        "Bug Tracker": "https://github.com/wsy/jina-segmenter/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: General",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="jina, text segmentation, nlp, ai",
)

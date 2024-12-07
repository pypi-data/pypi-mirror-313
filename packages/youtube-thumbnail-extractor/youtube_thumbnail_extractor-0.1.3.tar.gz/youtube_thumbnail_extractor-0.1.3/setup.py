from setuptools import setup, find_packages

setup(
    name="youtube_thumbnail_extractor",
    version="0.1.3",
    description="A Python library to extract thumbnails from YouTube videos without downloading and at required.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Quaxguy/youtube-thumbnail-extractor",
    author="Siddharth Lalwani",
    author_email="connectwithsid95@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "yt-dlp",
        "moviepy",
        "Pillow"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

from setuptools import setup, find_packages

setup(
    name="closed-caption",
    version="1.0.0",
    description="Tạo phụ đề từ video sử dụng OpenAI Whisper.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ngọc Hải Phạm",
    author_email="ngochai285nd@gmail.com",
    url="https://github.com/haiphamcoder/closed-caption",
    packages=find_packages(),
    install_requires=[
        "pysrt>=1.1.2",
        "openai-whisper>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "closed_caption=closed_caption.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

from setuptools import setup, find_packages

setup(
    name="mal_package2",  # 패키지 이름
    version="0.1.0",    # 버전
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",  # GitHub 등 저장소 URL
    packages=find_packages(),  # 패키지 자동 탐지
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

from setuptools import setup, find_packages

setup(
    name="Total_Game",  # 패키지 이름
    version="0.1.0",  # 패키지 버전
    author="HongKiBum",  # 작성자
    author_email="hgb9720@hanyang.ac.kr",  # 이메일
    description="A collection of mini-games and utilities.",  # 간단한 설명
    long_description=open("README.md", encoding="utf-8").read(),  # 긴 설명 (README 파일 내용)
    long_description_content_type="text/markdown",  # 긴 설명 형식
    url="https://github.com/HongKiBum/Total_Game",  # GitHub URL
    packages=find_packages(),  # 패키지 자동 탐색
    install_requires=[  # 필요한 라이브러리
        "pygame",
        "kivy",
        "ultralytics",
        "mediapipe",
        "opencv-python-headless",
        "pytesseract",
        "Pillow",
        "SpeechRecognition",
    ],
    classifiers=[  # 분류
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 라이센스 정보
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # 요구되는 Python 버전
    license="MIT",  # 라이센스 추가
)

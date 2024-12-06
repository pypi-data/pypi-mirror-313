# 🍻 술게임 라이브러리 (Total_Game) 

**DrunkFunLib**는 술자리에서 즐길 수 있는 다양한 게임들을 손쉽게 구현할 수 있도록 도와주는 Python 라이브러리입니다!

---

## 🚀 주요 기능

1. **비용 계산**  
   - 영수증 사진과 인원 수를 입력하면, 총 비용을 계산하여 1인당 부담해야 할 금액을 정산해 줍니다.

2. **취한 정도 파악 게임**  
   - 음성 파일을 입력하면 문장 정확도를 기반으로 사용자의 취한 정도를 측정합니다.

3. **사진 벌칙 게임**  
   - 사용자가 업로드한 사진 속 손 모양을 분석하고 랜덤하게 벌칙 대상을 선택합니다.

4. **사진 기반 인물 퀴즈**  
   - 사용자 지정 사진을 입력해 인물 퀴즈를 진행할 수 있습니다.

5. **룰렛 벌칙 게임**  
   - 사용자가 입력한 벌칙 리스트로 룰렛을 돌려 랜덤하게 벌칙을 선정합니다.

---

## 사용방법

--

## 📦 설치

### Prerequisites
- Python 3.8 이상이 필요합니다

### 🛠️ Tesseract OCR 설치 방법

이 프로젝트의 OCR 기능은 **Tesseract OCR**에 의존합니다. 운영 체제에 따라 아래의 설치 방법을 참고하세요.

---

#### macOS
1. Homebrew를 사용하여 Tesseract를 설치합니다.
   - `brew install tesseract`
2. 설치 확인:
   - 터미널에서 `tesseract --version` 명령어를 실행해 Tesseract 버전이 출력되는지 확인하세요.

---

#### Ubuntu/Linux
1. APT 패키지 관리자를 사용하여 Tesseract를 설치합니다.
   - `sudo apt-get update`
   - `sudo apt-get install tesseract-ocr`
2. 설치 확인:
   - 터미널에서 `tesseract --version` 명령어를 실행해 Tesseract 버전이 출력되는지 확인하세요.

---

#### Windows
1. [Tesseract 다운로드 페이지](https://github.com/UB-Mannheim/tesseract/wiki)에서 설치 파일(.exe)을 다운로드합니다.
2. 설치 중 "Add Tesseract to PATH" 옵션을 선택하세요.
3. 설치가 완료된 후 Tesseract 경로를 확인합니다.
   - 기본 경로: `C:\Program Files\Tesseract-OCR\tesseract.exe`
4. 환경 변수 설정이 필요한 경우:
   - "내 PC" → "속성" → "고급 시스템 설정" → "환경 변수"로 이동합니다.
   - "Path" 변수에 Tesseract 설치 경로를 추가하세요.

---

#### 설치 확인
- Tesseract가 정상적으로 설치되었는지 확인하려면, 명령어 `tesseract --version`을 실행하세요.
- 설치가 정상적으로 완료되었을 경우, Tesseract 버전 정보가 출력됩니다.

---

#### Python에서 사용하기 위한 추가 설치
1. Python 패키지 `pytesseract`를 설치해야 합니다.
   - `pip install pytesseract`
2. 설치 후, Python 코드에서 아래와 같이 Tesseract 경로를 설정합니다:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


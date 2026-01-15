# 💿 CDbri
CDbri is a lightweight utility designed to generate virtual audio CD files required for ```play with my own my choice of CD``` mode in the Vib-Ribbon.

This tool allows you to easily convert your own music files into ```.cue / .bin``` for play custom stages on emulators.

# ✨ Features
 * Seamless Conversion: Convert various audio formats ```MP3, WAV, etc.``` into a pair of .bin and .cue files.

 * Standalone Executable: No Python installation required.

 * User-Friendly GUI: Simple and intuitive interface built with Tkinter.

 * Modern Compatibility: Fully optimized for Python 3.13+ environments.

# 🚀 How to Use

 1. Run CDbri.exe.

 2. Select the audio file you want to use for your custom stage.

 3. Click the "GO" button. The .bin and .cue files will be generated in the folder that named as Export.

 4. While playing Vib-Ribbon on an emulator (e.g., DuckStation, ePSXe), wait for the "Play with my own choice of CD" prompt.

 5. Use the emulator's 'Change Disc' or 'Swap Disc' feature to insert the generated .cue file.

# 📦 Build from Source

If you want to build the executable yourself, you need this:

**Requirements**

 * Python 3.12+ (3.13 recommended)

 * pydub-lts, audioop-copy packages

 * FFmpeg must be installed on your syste

**Build Command (Nuitka)**

To create a compact, single-file executable:
```PowerShell
python -m nuitka --standalone --onefile --windows-console-mode=disable --enable-plugin=tk-inter --include-windows-runtime-dlls=no --remove-output cdbri.py
```

# ⚠️ Important Notes

 * **Antivirus False Positives** - Some antivirus software may flag the .exe as a "Trojan" or "Dropper" (e.g., Wacatac). This is a common false positive with Nuitka/PyInstaller executables because they extract files to a temporary folder during execution. The source code is 100% safe.
 * **Copyright** - Please use this tool only for music files that you legally own.
---
Developed by Resi-le, Enjoy your custom level!

# 💿 CDbri
CDbri는 PlayStation의 **비브리본(Vib-Ribbon)**에서 커스텀 곡을 즐기기 위해 필요한 가상 오디오 CD 파일```.cue / .bin```을 쉽고 빠르게 생성해 주는 도구입니다.

# ✨ 주요 기능 (Features)

 * **간편한 변환** - MP3, WAV 등 다양한 오디오 파일을 비브리본용 ```.bin / .cue``` 세트로 변환
 
 * **쉬운 설치** - 파이썬 설치 없이 파일 하나로 동작
 
 * **직관적인 GUI** - Tkinter 기반의 인터페이스로 누구나 쉽게 사용
 
 * **3.13 호환성** - 최신 파이썬 환경에서도 안정적으로 동작

🚀 사용 방법 (Usage)

 1. CDbri.exe를 실행
 2. 변환하고자 하는 음악 파일을 선택
 3. **GO** 버튼을 클릭해서 ```.bin```과 ```.cue``` 파일 생성 (Export 폴더에 생성됩니다.)
 4. ```Play with my own choice of CD```모드에서 생성된 .cue 파일을 **디스크 교체** 기능을 통해 삽입

# 📦 설치 및 빌드 (Installation)

이미 빌드된 파일을 사용하거나, 직접 빌드할 수 있습니다.
**직접 빌드할 경우**
 * Python 3.12+ (3.13 권장)
 * ```pydub-lts```, ```audioop-copy``` 패키지
 * FFmpeg 설치

**빌드 명령어**
```PowerShell
python -m nuitka --standalone --onefile --windows-console-mode=disable --enable-plugin=tk-inter --include-windows-runtime-dlls=no --remove-output cdbri.py
```

# ⚠️ 주의 사항 (Notice)
 * Nuitka 컴파일러 특성상 일부 백신에서 트로이목마 등으로 오진할 수 있습니다. 이는 실행 시 파일을 임시 폴더에 압축 해제하는 방식 때문이며, 소스 코드는 완전히 안전합니다.
 * 반드시 본인이 소유한 음악 파일을 변환하는 용도로만 사용해 주세요.
---
Developed by Resi-le, Enjoy your custom level!

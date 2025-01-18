# DICOM to MP4 Converter

DICOM 의료 영상을 MP4 비디오로 변환하는 간단한 GUI 프로그램입니다.

## 기능
- DICOM 파일을 MP4로 변환
- 다중 프레임 DICOM 지원
- 압축된 DICOM 파일 지원
- 하위 폴더 자동 검색
- 진행 상황 표시
- 그레이스케일 출력

## 설치 방법

1. Python 설치 (3.8 이상)
   - [Python 공식 웹사이트](https://www.python.org/downloads/)에서 다운로드

2. 프로젝트 클론
```bash
git clone https://github.com/[your-username]/dcm-to-mp4-converter.git
cd dcm-to-mp4-converter
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 사용 방법

1. 프로그램 실행:
```bash
python dcm_to_mp4.py
```

2. "찾아보기" 버튼을 클릭하여 DICOM 파일이 있는 폴더를 선택

3. "변환 시작" 버튼을 클릭하여 변환 시작

4. 변환된 MP4 파일은 원본 DICOM 파일이 있는 폴더 내의 'mp4' 하위 폴더에 저장됩니다.

## 주의사항
- 대용량 DICOM 파일의 경우 충분한 메모리가 필요할 수 있습니다.
- 변환 시간은 파일 크기와 컴퓨터 성능에 따라 달라질 수 있습니다.

## 라이센스
MIT License

## 문의사항
문제나 제안사항이 있으시면 Issues에 등록해주세요.

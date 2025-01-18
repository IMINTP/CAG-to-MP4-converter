import SimpleITK as sitk
import numpy as np
import cv2
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk
import threading

class DcmToMp4Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("DICOM to MP4 Converter")
        
        # 기본 설정
        self.fps = 15
        self.selected_directory = ""
        
        # GUI 구성
        self.create_widgets()
        
    def create_widgets(self):
        # 디렉토리 선택
        dir_frame = ttk.Frame(self.root, padding="5")
        dir_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(dir_frame, text="DICOM 디렉토리:").pack(side=tk.LEFT)
        self.dir_entry = ttk.Entry(dir_frame, width=50)
        self.dir_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(dir_frame, text="찾아보기", command=self.browse_directory).pack(side=tk.LEFT)
        
        # 진행 상황
        progress_frame = ttk.Frame(self.root, padding="5")
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.progress_var = tk.StringVar(value="준비됨")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(side=tk.LEFT)
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=5)
        
        # 변환 버튼
        button_frame = ttk.Frame(self.root, padding="5")
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="변환 시작", command=self.start_conversion).pack(side=tk.LEFT)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory = directory
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def normalize_frame(self, frame):
        """단일 프레임을 정규화하여 0-255 범위의 uint8로 변환"""
        if frame.dtype != np.uint8:
            frame_min = frame.min()
            frame_max = frame.max()
            if frame_max - frame_min > 0:
                frame_normalized = ((frame - frame_min) / (frame_max - frame_min) * 255).astype(np.uint8)
            else:
                frame_normalized = np.zeros_like(frame, dtype=np.uint8)
            return frame_normalized
        return frame
    
    def dcm_to_mp4(self, input_file, output_file):
        """단일 DICOM 파일을 MP4로 변환"""
        try:
            # DICOM 파일 읽기
            reader = sitk.ImageFileReader()
            reader.SetFileName(str(input_file))
            image = reader.Execute()
            
            # numpy 배열로 변환
            array = sitk.GetArrayFromImage(image)
            
            # 차원 처리
            if len(array.shape) == 2:  # 단일 2D 이미지
                frames = [self.normalize_frame(array)]
            elif len(array.shape) == 3:  # 여러 프레임 또는 컬러 이미지
                if array.shape[0] == 3:  # RGB 이미지
                    gray = cv2.cvtColor(np.transpose(array, (1, 2, 0)), cv2.COLOR_RGB2GRAY)
                    frames = [self.normalize_frame(gray)]
                else:  # 여러 프레임
                    frames = [self.normalize_frame(array[i]) for i in range(array.shape[0])]
            else:
                raise ValueError(f"Unexpected image shape: {array.shape}")
            
            if not frames:
                raise ValueError("No frames extracted from DICOM file")
            
            # 첫 프레임으로 비디오 크기 결정
            height, width = frames[0].shape
            
            # VideoWriter 객체 생성
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(str(output_file), fourcc, self.fps, (width, height), isColor=False)
            
            # 모든 프레임 저장
            for frame in frames:
                video_writer.write(frame)
            
            video_writer.release()
            return True
            
        except Exception as e:
            print(f"Error processing {input_file.name}: {str(e)}")
            return False
            
    def find_dcm_files(self, directory):
        """디렉토리와 모든 하위 디렉토리에서 DCM 파일 찾기"""
        dcm_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.dcm'):
                    dcm_files.append(Path(root) / file)
        return sorted(dcm_files)  # 파일 이름순으로 정렬
    
    def convert_files(self):
        """모든 파일 변환 처리"""
        if not self.selected_directory:
            self.progress_var.set("디렉토리를 선택해주세요.")
            return
            
        # DCM 파일 목록 생성
        dcm_files = self.find_dcm_files(self.selected_directory)
        if not dcm_files:
            self.progress_var.set("변환할 DICOM 파일이 없습니다.")
            return
            
        total_files = len(dcm_files)
        processed_files = 0
        successful_files = 0
        
        # 진행바 초기화
        self.progress_bar['maximum'] = total_files
        self.progress_bar['value'] = 0
        
        for dcm_file in dcm_files:
            # 출력 파일 경로
            output_file = dcm_file.parent / f"{dcm_file.stem}.mp4"
            
            # 파일 변환
            if self.dcm_to_mp4(dcm_file, output_file):
                successful_files += 1
            
            processed_files += 1
            self.progress_bar['value'] = processed_files
            self.progress_var.set(f"처리 중: {processed_files}/{total_files} (성공: {successful_files})")
            self.root.update()
        
        self.progress_var.set(f"완료! {successful_files}/{total_files}개 파일 변환 성공")
    
    def start_conversion(self):
        """변환 프로세스를 별도 스레드로 시작"""
        conversion_thread = threading.Thread(target=self.convert_files)
        conversion_thread.start()

def main():
    root = tk.Tk()
    app = DcmToMp4Converter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
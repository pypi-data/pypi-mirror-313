from fer import FER
import cv2
import os
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import pathlib
import numpy as np 

class ImageFilterLibrary:
    def __init__(self, image_path):
        # 유니코드 경로 변환
        unicode_path = str(pathlib.Path(image_path).resolve(strict=True))
        self.image_path = unicode_path

        # Pillow로 이미지 불러오기
        self.image = Image.open(unicode_path)

        # OpenCV로 이미지 불러오기
        self.cv_image = cv2.imdecode(
            np.fromfile(unicode_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED
        )
        
        self.filters = {
            "blur": self.apply_blur,
            "sharpen": self.apply_sharpen,
            "brighten": self.apply_brighten,  # 밝은 필터 추가
            "darken": self.apply_darken,  # 어두운 필터 추가
        }
        

    def apply_filter(self, filter_name, intensity):
        """사용자 정의 필터"""

        if filter_name not in self.filters and (intensity < 1 or intensity > 50):
            print("filter name and intensity error. retry")
            return False
        
        elif filter_name not in self.filters:
            print(f"Filter '{filter_name}' is not available. retry")
            
            return False
        
        elif (intensity < 1 or intensity > 50):
            print("Error: invalid value. Please use a value between 1 and 50. retry ")
            return False
        
        
        else:
            if filter_name == "blur":
                filtered_image = self.apply_blur(intensity)
            elif filter_name == "sharpen":
                filtered_image = self.apply_sharpen(intensity)
            elif filter_name == "brighten":
                filtered_image = self.apply_brighten(intensity)
            elif filter_name == "darken":
                filtered_image = self.apply_darken(intensity)

            
            return filtered_image
                       

    def apply_blur(self, intensity=1):
        """블러 필터 강도 적용"""
        return self.image.filter(ImageFilter.GaussianBlur(radius=intensity))

    def apply_sharpen(self, intensity=1):
        """샤프 필터 강도 적용"""
        enhancer = ImageEnhance.Sharpness(self.image)
        return enhancer.enhance(intensity)

    def apply_brighten(self, intensity=1):
        """밝기 필터 강도 적용"""
        enhancer = ImageEnhance.Brightness(self.image)
        return enhancer.enhance(intensity)

    def apply_darken(self, intensity=1):
        """어두운 필터 강도 적용"""
        enhancer = ImageEnhance.Brightness(self.image)
        return enhancer.enhance(1 / intensity)  # 강도에 반비례하여 어두워짐

    def apply_blue_tint(self):
        """파란 계열 필터 적용"""
        return ImageOps.colorize(ImageOps.grayscale(self.image), black="black", white="blue")

    def apply_red_tint(self):
        """붉은 계열 필터 적용"""
        return ImageOps.colorize(ImageOps.grayscale(self.image), black="black", white="red")

    def apply_yellow_tint(self):
        """노란 계열 필터 적용"""
        return ImageOps.colorize(ImageOps.grayscale(self.image), black="black", white="yellow")

    def apply_pink_tint(self):
        """분홍 계열 필터 적용"""
        return ImageOps.colorize(ImageOps.grayscale(self.image), black="black", white="pink")

    def apply_purple_tint(self):
        """보라 계열 필터 적용"""
        return ImageOps.colorize(ImageOps.grayscale(self.image), black="black", white="purple")

    def save_image(self, save_path, image_to_save=None):
        if image_to_save is None:
            image_to_save = self.image  # 기본적으로 원본 이미지 저장

        image_to_save.save(save_path)
        print(f"Image saved to {save_path}")

    

    def analyze_and_apply_filter(self):
        """FER를 사용하여 감정을 분석하고 필터를 적용"""
        detector = FER(mtcnn=True)

        try:
            results = detector.detect_emotions(self.cv_image)

        except Exception as e:
            print(f"Error: {e}")
            return False
        
        try :
            if not results:
                raise 

            dominant_emotion = results[0]["emotions"]
            emotion = max(dominant_emotion, key=dominant_emotion.get)

            emotion_to_filter = {
                "happy": "yellow_tint",
                "sad": "blue_tint",
                "angry": "red_tint",
                "neutral": "purple_tint",
                "surprise": "pink_tint",
                "fear": "darken",
            }

            filter_name = emotion_to_filter.get(emotion,"false")

            if filter_name == "false":
                print("Error: Can't analyze emotion")
                return False
            
            print(f"Detected dominant emotion: {emotion}")
            print(f"Applying filter: {filter_name}")

            # 필터링된 이미지 생성
            filtered_image = getattr(self, f"apply_{filter_name}")()
            print(f"Filter '{filter_name}' applied successfully.")
            return filtered_image  # 필터링된 이미지를 반환

        except :
            print("Error: No faces detected.")
            return False
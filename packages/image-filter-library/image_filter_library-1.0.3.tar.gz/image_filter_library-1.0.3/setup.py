from setuptools import setup, find_packages

setup(
    name="image_filter_library",
    version="1.0.3",
    description="A library for applying image filters with emotion detection using FER.",
    author="nanayeong",
    author_email="na22384593@gmail.com",
    packages=["image_filter_library"],
    install_requires=[
        "Pillow",
        "fer",
        "opencv-python-headless",
        "tensorflow",
        "moviepy==1.0.3",
        "numpy>=1.19.3,<1.26",
        "decorator>=4.0.0,<5.0",
        "imageio[ffmpeg]>=2.4.1",
        "tqdm>=4.11.2",
        "proglog>=0.1.9",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

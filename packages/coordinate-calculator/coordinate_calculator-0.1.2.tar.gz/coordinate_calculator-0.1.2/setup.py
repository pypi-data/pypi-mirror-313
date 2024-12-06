from setuptools import setup, find_packages

setup(
    name="coordinate-calculator",
    version="0.1.2",
    description="Drone YOLO client for object detection and server communication.",
    author="ittipat jitrada",
    author_email="ittipatjitrada@gmail.com",
    packages=find_packages(),
    install_requires=[
        "python-socketio",
        "opencv-python",
        "pillow",
        "ultralytics",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "drone-yolo-client=drone_yolo_client.client:main",
        ],
    },
)

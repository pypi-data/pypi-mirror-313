from setuptools import setup, find_packages

setup(
    name="drone-yolo-client",
    version="0.1.0",
    description="Drone YOLO client for object detection and server communication.",
    author="Your Name",
    author_email="your.email@example.com",
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

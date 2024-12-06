from setuptools import setup, find_packages

setup(
    name="coordinate-estimate",
    version="0.1.1",
    description="Drone YOLO client for object detection and server communication.",
    author="ittipat jitrada",
    author_email="ittipatjitrada@gmail.com",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        'object_position_calculator': ['best.pt'],
    },
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

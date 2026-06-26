from setuptools import setup

package_name = "robot_controller"

setup(
    name=package_name,
    version="0.1.0",
    packages=["robot_controller_ros2"],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/config", ["config/default.yaml"]),
        (f"share/{package_name}/launch", ["launch/demo.launch.py"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="KITTIYOJIANG",
    maintainer_email="support@example.com",
    description="ROS2 integration for the STM32 robot controller kit.",
    license="TODO",
    entry_points={
        "console_scripts": [
            "robot_controller_node = robot_controller_ros2.node:main",
        ],
    },
)

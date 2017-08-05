from setuptools import setup, find_packages

setup(
    name='webRTCserver',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'python-socketio',
        'eventlet'
    ],
)

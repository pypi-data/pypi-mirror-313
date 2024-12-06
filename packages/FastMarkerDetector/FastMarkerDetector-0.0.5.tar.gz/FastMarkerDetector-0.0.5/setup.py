from setuptools import setup


setup(
    name='FastMarkerDetector',
    version='0.0.5',
    packages=['FastMarkerDetector'],
    package_data={
        'FastMarkerDetector': ['*.so'], 			  #pyd
    }
)

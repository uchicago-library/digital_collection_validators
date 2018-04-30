from setuptools import setup

setup(
    name="digital_collection_validator",
    author="Amanda Wong",
    author_email="wongamanda@uchicago.edu",
    version="1.0.0",
    license="LGPL3.0",
    description="A tool to validate structure of OCR directories", 
    keywords="python3.5 iiif-presentation manifests",
    scripts=['dcv/proj1.py'],
    classifiers=["License :: OSI Approved :: GNU Library or Lesser " +
        "General Public License (LGPL)",
        "Development Status :: 5 - Alpha/Prototype",
        "Intended Audience :: Education",
        "Operating System :: POSIX :: Linux",
        "Topic :: Text Processing :: Markup :: XML"]
)
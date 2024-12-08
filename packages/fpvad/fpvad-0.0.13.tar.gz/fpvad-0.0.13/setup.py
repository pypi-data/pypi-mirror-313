from setuptools import setup, find_packages

setup (
    name="fpvad",
    version="0.0.13",
    packages=find_packages(),
    install_requires=[
        "asteroid-filterbanks==0.4.0",
        # "librosa==0.10.2.post1",
        # "numpy==1.26.4",
        # "soundfile==0.12.1",
        # "torch==2.3.1",
        # "torchaudio==2.3.1",
    ],
    include_package_data=True,
    author="FanPars",
    description="Detects voice activity in audio files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)
from setuptools import setup, find_packages

setup(
    name="zohencel-ai",
    version="0.2.8",
    description="A Python package for voice assistant, chatbot development, and analysis tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vishnu K",
    author_email="vishnuknandanam@gmail.com",
    url="https://zohencelai.github.io/",
    packages=find_packages(),
    install_requires=[
        "numpy",            # For numerical processing
        "requests",         # For making API calls
        "assemblyai"
        ,"playsound"
        ,"PyAudio"
        ,"pyttsx3"
        ,"SpeechRecognition"
        ,"groq"
        ,"pillow"
        ,"matplotlib"
        ,"streamlit"
        ,"pandas"
        ,"seaborn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)


# py -m pip install --upgrade build
# py -m build
# py -m pip install --upgrade twine
# py -m twine upload dist/*

# update wheel incase of error
# python setup.py sdist bdist_wheel


from setuptools import setup, find_packages

setup(
    name='pdice',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'undetected-chromedriver',
        'asyncio',
        'tqdm',
        'pytesseract',
        'spacy',
        'pymupdf',
        'google-generativeai',
        'mistralai',
        'imblearn',
        'requests',
        'fastapi',
        'uvicorn',
        'pyautgui',
        'crewai',
        'pywebio',
        'pywebio-battery',
    ],
    author='Prophet Dice Bot',
    author_email='support@prophetdice.com',
    description='ProphetDice Functions',
    long_description=open('README.md').read(),  # Reads the long description from a README file
    long_description_content_type='text/markdown',  # If your README is in Markdown
    url='https://prophetdice.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # You can change this to whatever license applies
        'Programming Language :: Python :: 3.8',  # Adjust to the version(s) your package supports
        'Intended Audience :: Developers',  # Adjust based on the target audience for your package
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',  # Specify the minimum Python version required
)

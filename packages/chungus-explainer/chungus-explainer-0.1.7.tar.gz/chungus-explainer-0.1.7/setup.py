from setuptools import setup, find_packages

setup(
    name='chungus-explainer',  # The name of your library
    version='0.1.7',  # Initial version
    author='Yap Hong Jun',
    author_email='yaphongjun@gmail.com',
    description='A library that incorportates ChatGPT to help users read Shap values.',
    long_description=open('README.md').read(),  # Include a detailed description
    long_description_content_type='text/markdown',
    packages=['chungus_explainer'],  # Automatically find the package (`chungus` folder)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
import setuptools

with open("README.md", 'r') as fp:
    long_description = fp.read()

setuptools.setup(
    name = "jigsaw",
    version = "0.0.1",
    author="Abolfazl Farahani, Jonathan Myers, Saed Rezayi",
    author_email="a.farahani@uga.edu, submyers@uga.edu, saedr@uga.edu",
    license='MIT',
    description="A package for toxicity classification.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsp-uga/team-jigsaw-final",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['keras', 're', 'pandas', 'numpy', 'bs4', 'sklearn', 'nltk'],
)

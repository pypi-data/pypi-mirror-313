from setuptools import setup, find_packages

setup(
    name="SentinelLogAnalyzer",  
    version="1.0.1",
    author="Vidit Pandey",
    author_email="viditpandey06@gmail.com",
    description="A log analysis tool supporting multiple log formats like Nginx, AWS, and more.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/viditpandey06/SentinelLogAnalyzer",  
    packages=find_packages(),  # Automatically finds packages in the directory
    install_requires=[
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
   entry_points={
    'console_scripts': [
        'log-analysis=SentinelLogAnalyzer.log_analysis:main',
    ],
},
)

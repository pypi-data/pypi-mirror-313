from setuptools import setup, find_packages

setup(
    name="model_community",  # 包名
    version="0.1",  # 版本号
    packages=find_packages(),
    install_requires=[
        'requests',
        'tqdm',
    ],
    description="A tool for downloading and extracting machine learning models from Model Community, the world's largest Chinese model website.",
    long_description=open('README.md', encoding='utf-8').read(),  
    long_description_content_type='text/markdown',  
    author="LSA1234",  
    author_email="anan15919991635@163.com",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)

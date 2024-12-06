import setuptools

setuptools.setup(
    name='coolbg',
    version='3.177',
    author="Thanh Hoa",
    author_email="thanhhoakhmt1@gmail.com",
    description="A Des of coolbg",
    long_description="Des",
    long_description_content_type="text/markdown",
    url="https://github.com/vtandroid/dokr",
    packages=setuptools.find_packages(),
    py_modules=['bgeditor'],
    install_requires=[
        'requests==2.25.1', 'numpy', 'moviepy', 'Pillow==9.5.0', 'youtube_dl', 'gbak','yt_dlp'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )
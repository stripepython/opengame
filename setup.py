from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='opengame',
    packages=find_packages(where='.', exclude=(), include=('*', )),
    author='stripe-python',
    author_email='stripe-python@139.com',
    maintainer='stripe-python',
    maintainer_email='stripe-python@139.com',
    license='MIT License',
    install_requires=[
        'pygame~=2.1.2',
        'requests~=2.28.1',
        'PyExecJS~=1.5.1',
        'opencv-python~=3.4.11.45',
    ],
    extras_require={
        'record': ['pyaudio'],
        'glwindow': ['PyOpenGL'],
        'windows': ['pypiwin32', 'pythonnet'],
    },
    version='1.0.2beta',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/stripepython/opengame/',
)

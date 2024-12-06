from setuptools import setup, find_packages

setup(
    name='localstorage-flask',
    version='0.1',
    description='A Flask extension for local storage',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Bobby',
    author_email='info@bobby-shop.com',
    url='https://github.com/bobbyshop-vui/localstorage-flask.git',  # Thay bằng URL dự án GitHub của bạn (nếu có)
    packages=find_packages(),
    install_requires=[
        'Flask',  # Ví dụ về một thư viện phụ thuộc
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

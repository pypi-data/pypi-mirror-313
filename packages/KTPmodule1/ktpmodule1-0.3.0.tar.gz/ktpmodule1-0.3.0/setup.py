from setuptools import setup, find_packages

setup(
    name='KTPmodule1',  # Tên package của bạn
    version='0.3.0',  # Phiên bản của package
    description='A brief description of your package',  # Mô tả ngắn gọn
    long_description=open('README.md').read(),  # Đọc mô tả dài từ file README
    long_description_content_type='text/markdown',  # Định dạng markdown cho README
    author='Your Name',  # Tên tác giả
    author_email='your.email@example.com',  # Email tác giả
    url='https://github.com/yourusername/my_package',  # Địa chỉ repository
    packages=find_packages(),  # Tự động tìm các package trong thư mục my_package
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Phiên bản Python tối thiểu
)
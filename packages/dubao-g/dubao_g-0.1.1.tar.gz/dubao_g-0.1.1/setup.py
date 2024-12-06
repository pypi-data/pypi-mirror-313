from setuptools import setup, find_packages  

setup(  
    name='dubao_g',  # Tên package  
    version='0.1.1',  # Phiên bản  
    author='Hungpc',  # Tên tác giả  
    author_email='your.email@example.com',  # Email tác giả  
    description='A brief description of your package',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/yourusername/my_package',  # Trang của project (nếu có)  
    packages=find_packages(),  # Tìm kiếm package trong thư mục  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],  
    python_requires='>=3.6',  # Yêu cầu phiên bản Python  
)  
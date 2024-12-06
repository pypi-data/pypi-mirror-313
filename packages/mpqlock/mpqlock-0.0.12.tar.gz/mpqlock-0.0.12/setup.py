from setuptools import find_packages, setup
setup(
    name='mpqlock',
    version='0.0.12',
    description='lock for MPQ_code',
    author='MPQ',#作者
    author_email='miaopeiqi@163.com',
    url='https://github.com/miaopeiqi',
    #packages=find_packages(),
    packages=['mpqlock'],  #这里是所有代码所在的文件夹名称
    package_data={
    '':['*.pyd'],
    },
    install_requires=['numpy>=1.14.0','matplotlib>=2.0','pandas>=0.22.0','PyWavelets>=1.2.0','six>=1.16.0','opencv-python>=3.9.0','spectral>=0.22.4','scikit-learn>=0.24.2'],
)

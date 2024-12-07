from setuptools import setup, find_packages


# 读取 requirements.txt 中的依赖包
def parse_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line and not line.startswith('#')]

setup(
    name='xh-advanced-task-runner',
    version='0.1',
    description='An advanced package to run tasks concurrently with retries and support for thread and process pools.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='HuiMob',
    author_email='a1817802964@gmail.com',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
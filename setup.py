from setuptools import setup, find_packages

setup(
    name='tocmanuscript',
    version='0.2',
    packages=find_packages(),
    author='Marko T. Manninen',
    author_email='elonmedia@gmail.com',
    description='Manuscript Content Generation and Management in ChatGPT using Noteable Plugin',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)

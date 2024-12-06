from setuptools import setup, find_packages

setup(
    name='qmdx',
    version="0.0.3",
    description="Pipe and diff files: execute shell pipelines against multiple inputs, diff/compare/join results.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=open("requirements.txt").read(),
    entry_points={
        'console_scripts': [
            'diff-x = qmdx.diff_x:main',
            'comm-x = qmdx.comm_x:main',
            'git-diff-x = qmdx.git_diff_x:main',
        ],
    },
    license="MIT",
    author="Ryan Williams",
    author_email="ryan@runsascoded.com",
    author_url="https://github.com/ryan-williams",
    url="https://github.com/runsascoded/qmdx",
)

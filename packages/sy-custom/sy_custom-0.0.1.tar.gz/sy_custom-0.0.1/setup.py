from setuptools import find_packages, setup

setup(
    name="sy_custom",
    version="0.0.1",
    description="utilities for AI models with Pytorch by SY",
    author="sy.noh",
    author_email="nshinyeong@gmail.com",
    url="https://github.com/dneirfi/sy_custom.git",
    install_requires=['tqdm', 'pandas', 'scikit-learn'],
    packages=find_packages(exclude=[]),
    keywords=['sy_custom'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
    
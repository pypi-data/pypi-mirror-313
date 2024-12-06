from setuptools import setup, find_packages

setup(
    name='MultiBgolearn',
    version='0.0.4',
    description="Python package designed for multi-objective Bayesian global optimization (MOBO)",
    long_description=open('README.md', encoding='utf-8').read(),
    include_package_data=True,
    author='CaoBin',
    author_email='bcao686@connect.hkust-gz.edu.cn',
    maintainer='CaoBin',
    maintainer_email='bcao686@connect.hkust-gz.edu.cn',
    license='MIT License',
    url='https://github.com/Bin-Cao/MultiBgolearn',
    packages=find_packages(),  # Automatically include all Python modules
    package_data={'MultiBgolearn': ['utility/*']},  # Specify non-Python files to include
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.5',
    install_requires=[ 'scikit-learn', 'openpyxl',  'art'],
    entry_points={
        'console_scripts': [
            '',
        ],
    },
)

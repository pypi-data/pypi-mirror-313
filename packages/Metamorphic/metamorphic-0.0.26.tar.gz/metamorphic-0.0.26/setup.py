from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "Metamorphic.MorphAlyt",
        sources=["Metamorphic/MorphAlyt.pyx"])
]

setup(
    name="Metamorphic",
    version="0.0.26",
    description="Elliptic curve operations using SageMath",
    long_description_content_type="text/markdown",
    author='fourchains_R&D',
    author_email='fourchainsrd@gmail.com',
    packages=["Metamorphic"],
    ext_modules=cythonize(ext_modules),  # Cython 컴파일 활성화
    #ext_modules=cythonize(ext_modules, compiler_directives={"language_level": "3"}),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={
        "Metamorphic.data": ["*.csv"],  # data 폴더 내의 모든 .csv 파일을 포함
    },
    #package_data={
    #    "MetaMorphic": ["*.pxd", "*.c", "*.h", "*.pyd"],
    #},
    #exclude_package_data={
    #    "MetaMorphic": ["*.py", "*.pyx"],  # .py와 .pyx 파일 제외
    #},
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "sympy",
        "matplotlib",
        "seaborn",
    ],
)


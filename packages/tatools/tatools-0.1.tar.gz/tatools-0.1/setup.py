from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tatools",  # tên của gói thư viện
    version="0.1",
    description="Thư viện hữu ích của Tuấn Anh.",
    url="https://pypi.org/project/tatools/",
    author="Tuấn Anh - Foxconn",
    author_email="nt.anh.fai@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "ruamel.yaml",
        "lxml",
        "tqdm",
    ],  # ultralytics 8.2.84 requires numpy<2.0.0,>=1.23.0  pip install numpy==1.26.4
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "ntanh": [
            "About/*",
            "Thoi_gian/*",
            "file_folder/*",
            "IVIS_Data/*",
        ]
    },
    # package_dir={"": "ntanh"},
    # packages=find_packages(where="ntanh"),
    Homepage="https://github.com/ntanhfai/tact",
    Issues="https://github.com/ntanhfai/tact/issues",
    entry_points={
        "console_scripts": [
            "tatools=tatools:console_main",
            "tatools_base_params_help=tatools:Print_BaseParam_using",
            "tatools_Print_Check_license=tatools:Print_Check_license",  # in cách sử dụng Check_license
            "tatools_delete_files_extention=tatools:iconsole_delete_files",
        ],
    },
)

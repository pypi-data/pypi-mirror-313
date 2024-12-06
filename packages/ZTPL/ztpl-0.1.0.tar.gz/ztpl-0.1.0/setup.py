import pathlib
import setuptools
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

# 指定 CUDA 源文件目录
include_dirs = ["ZTPL/CUDA"]

# CUDA 扩展模块
ext_modules = [
    CUDAExtension(
        name="Test_CUDA",  # 扩展名
        sources=["ZTPL/CUDA/Test.cu"],  # CUDA 源文件
        include_dirs=include_dirs,
        extra_compile_args={"cxx": ["-O2"], "nvcc": ["-O2"]},
    ),
]

# 使用 setuptools 构建包
setuptools.setup(
    name="ZTPL",
    version="0.1.0",
    description="ZTPL test with CUDA support",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="YuningYe",
    author_email="1956860113@qq.com",
    license="The Unlicense",
    packages=setuptools.find_packages(),  # 自动查找所有子包
    install_requires=[],  # 根据需要添加其他依赖
    include_package_data=True,  # 包含额外的非代码文件
    ext_modules=ext_modules,  # 包含 CUDA 扩展
    cmdclass={"build_ext": BuildExtension},  # 使用 BuildExtension 编译 CUDA 扩展
)

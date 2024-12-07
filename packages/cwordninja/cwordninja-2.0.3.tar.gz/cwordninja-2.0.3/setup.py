from setuptools import setup, Extension
import os

try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None

def no_cythonize(extensions, **_ignore):
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in (".pyx", ".py"):
                if extension.language == "c++":
                    ext = ".cpp"
                else:
                    ext = ".c"
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions

# 定义Cython扩展模块
extensions = [
    Extension(
        "_cwordninja_core",  # 模块名
        sources=["core.pyx"],  # Cython源文件
        extra_compile_args=['-O3'],  # 额外的编译参数
    )
]

CYTHONIZE = bool(int(os.getenv("CYTHONIZE", 0))) and cythonize is not None

if CYTHONIZE:
    compiler_directives = {"language_level": 3}
    extensions = cythonize(extensions, compiler_directives=compiler_directives)
else:
    extensions = no_cythonize(extensions)

# 设置setup参数
setup(
    name='cwordninja',  # 包名
    version='2.0.3',  # 版本号
    author='MoYan',  # 作者
    author_email='moyanjdc@qq.com',  # 作者邮箱
    description='Probabilistically split concatenated words using NLP based on English Wikipedia uni-gram frequencies.',  # 包描述
    long_description=open("README.md").read(),  # 长描述
    long_description_content_type="text/markdown",
    url='https://github.com/moyanj/cwordninja',  # 项目URL
    packages=["cwordninja"],  # 包名
    ext_modules=extensions,  # Cython编译选项
    install_requires=[  # 依赖
    ],
    python_requires='>=3.7',  # 兼容的Python版本
    include_package_data=True,  # 包含数据文件
    classifiers=[  # 包分类
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)

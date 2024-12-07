import os
from setuptools import setup


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()


long_description = read("README.rst")


setup(
    name='model-wrapper',
    packages=['model_wrapper', 'model_wrapper.training'],
    description="Model wrapper for Pytorch, which can training, predict, evaluate, etc.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.2.0',
    install_requires=[
        "numpy>=1.0.0",
        "numpy<2.0.0; sys_platform == 'darwin'",  # macOS OpenVINO errors https://github.com/ultralytics/ultralytics/pull/17221
        "tqdm>=3.0.0",
        "torch>=1.0.0",
        "torch>=1.0.0,!=2.4.0; sys_platform == 'win32'",  # Windows CPU errors w/ 2.4.0 https://github.com/ultralytics/ultralytics/issues/15049
    ],
    url='https://gitee.com/summry/model-wrapper',
    author='summy',
    author_email='xiazhongbiao@126.com',
    keywords=['Pytorch', 'Training', 'AI', 'Machine learning', 'Deep learning', 'torch'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    zip_safe=False
)


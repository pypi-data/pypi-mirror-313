import codecs
import os
from setuptools import setup, find_packages
# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
 long_description = "\n" + fh.read()
# you need to change all these
VERSION = '1.0.3.241205'
DESCRIPTION = 'Static LiDAR point cloud processing library'
LONG_DESCRIPTION = 'Produced by Professor Wang Liying team from the School of Geomatics, Liaoning Technology University'
setup(
 name="Zelas2",
 version=VERSION,
 author="Ze You, Shichao Wang, Huaxin Chen, Yimo Geng, Yuqing Wang",
 author_email="878054597@qq.com",
 description=DESCRIPTION,
 long_description_content_type="text/markdown",
 long_description=long_description,
 packages=find_packages(),
 install_requires=[],
 keywords=['python', 'las', 'LiDAR','windows','linux'],
 classifiers=[
 "Development Status :: 1 - Planning",
 "Intended Audience :: Developers",
 "Programming Language :: Python :: 3.8",
 "Operating System :: Unix",
 "Operating System :: Microsoft :: Windows",
 ]
)
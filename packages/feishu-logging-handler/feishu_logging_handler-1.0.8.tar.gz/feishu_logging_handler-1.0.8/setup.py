import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="feishu_logging_handler",
  version="1.0.8",
  author="smock",
  author_email="smockg@gmail.com",
  description="logging的飞书handler",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/smockgithub/feishu-logging-handler",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  install_requires=['httpx','cachetools'],
  python_requires='>=3'
)

# python setup.py sdist bdist_wheel
# twine upload dist/*
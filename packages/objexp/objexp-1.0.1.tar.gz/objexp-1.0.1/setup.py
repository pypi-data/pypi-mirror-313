from setuptools import setup

setup()




# 注意：您可能会收到一条错误消息，指出“项目文件具有 'pyproject.toml' ，并且其构建后端缺少 'build_editable' 钩子。
# 这是由于 Setuptools 对 PEP 660 的支持存在限制。您可以通过添加包含以下内容的名为 setup.py 的文件来解决此问题：
# # setup.py
# ```python
# from setuptools import setup
# setup()
# ``
# 此填充码将执行可编辑安装的工作委托给 Setuptools 的旧机制，直到对 PEP 660 的本机支持可用。








# setup(
#     name='objexp',
#     version='1.0.0',
#     description='A plugin to say sorry in several ways',
#     url='http://wuxv.art',
#     author='lukelin',
#     author_email='luke.l.lin@hotmail.com',
#     license='SimPL-2.0',
#     packages=['objexp'],
#     zip_safe=False
# )

# `pip install -e . `
# `-e` means sync modify from source to installed package.

# `python setup.py register`

# https://setuptools.pypa.io/en/latest/userguide/quickstart.html


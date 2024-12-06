该脚本仅用于口碑项目（或其他按需）。

更新步骤：
1/首先cd到该文件夹；
2/删除build、dist和egg-info文件
3/改变setup.py文件中的description及version，根据改动的大小来修改version号
3/更新使用：python setup.py sdist build
4/提交：twine upload dist/*
5/更新库：pip install --upgrade general_calculator_zsd -i https://pypi.python.org/simple
e319a6d22898173c
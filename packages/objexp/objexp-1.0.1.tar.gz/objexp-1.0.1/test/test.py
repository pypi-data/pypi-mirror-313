
from sys import path
import os
 
# setting path
def setparentpathbeforeimport():
    testfile_path = os.path.dirname(__file__)
    objexp_path = os.path.join(testfile_path,"../src/")
    path.append(objexp_path)

def checkdir(dirpath):
    for (root,dirs,files) in os.walk(dirpath,topdown=True):
        print("Directory path: %s"%root)
        print("Directory Names: %s"%dirs)
        print("Files Names: %s"%files)
        break

# path[-1] 是最后添加的目录
# 第一遍循环检查最后添加的目录的根目录下都有什么内容, 以确认当前目录的绝对路径
# 但是现在用的是运行python的路径 如果运行test.py的位置变了，就会产生错误，
# 若要避免这种错误，就要使用test.py文件的目录做标的

# 获取当前文件（test.py）路径
# https://note.nkmk.me/en/python-script-file-path/
# checkdir(path[-1])

if False or 1:
    
    setparentpathbeforeimport()
    from objexp import ox

    class TestEmptyClass:
        pass

    def tst():
        ox(os)

    tst()
        

    # print('getcwd:      ', os.getcwd())
    # print('__file__:    ', __file__)
    # print('path:    ', (os.path.dirname(__file__)))

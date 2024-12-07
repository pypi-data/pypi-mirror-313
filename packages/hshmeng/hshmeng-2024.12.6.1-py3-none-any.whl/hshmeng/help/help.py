# -*- coding: utf-8 -*-

# 这是一篇帮助文档
def 帮助(页面=None, 页码=None):
    if 页面 is None:
        print("欢迎使用帮助文档")
        print("尝试运行：帮助(\"目录\")吧！")
    elif 页面 == "目录":
        if 页码 is not None:
            keys = list(dict_help.keys())
            if 0 <= 页码 < len(keys):
                dict_help[keys[页码]]()  # 调用函数
            else:
                print("索引超出范围")
        else:
            for key in dict_help.keys():
                print(key)


def the_keyword():
    keyword_english_is = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class',
                          'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if',
                          'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
                          'while', 'with', 'yield']
    for i in range(0, len(keyword_english_is), 5):
        print("{:<10}{:<10}{:<10}{:<10}{:<10}".format(*keyword_english_is[i:i + 5]))
    keyword_chinese_is = ['假', '空', '真', '和', '作为', '断言', '异步', '等待', '中断', '类', '继续', '定义', '删除',
                          '否则如果', '否则', '除非', '最终', '循环', '从', '全局', '如果', '导入', '在', '是',
                          '匿名函数', '非局部', '非', '或', '跳过', '引发', '返回', '尝试', '当', '与', '生成']
    for i in range(0, len(keyword_chinese_is), 5):
        print("{:<10}{:<10}{:<10}{:<10}{:<10}".format(*keyword_chinese_is[i:i + 5]))

def the_keyword_for_we():
    print("""
print(values, sep, end, file, flush)
输出(值, 分隔符, 结束, 文件, 刷新)
    """)

dict_help = {
    "0.保留关键字对应中文名称": the_keyword,
    "1.其它更改的函数": the_keyword_for_we,
}


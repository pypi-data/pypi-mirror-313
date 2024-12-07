# -*- coding: utf-8 -*-
import sys
def 输出(值, 分隔符='', 结束='\n', 文件=sys.stdout, 刷新=False):
    # 使用列表推导式将值转换为字符串，并用分隔符连接
    output = 分隔符.join(str(value) for value in 值) + 结束
    # 将输出写入文件
    文件.write(output)
    if 刷新:
        # 如果进行刷新，则刷新文件
        文件.flush()


import os,sys,time
# 列出所请路径根目录下的文件和文件夹
def path_list(request_path):
    path_list = {'dirs':[],'files':[]}
    for item in os.listdir(request_path):
        full_path = os.path.join(request_path,item)
        fsize = os.path.getsize(full_path)
        fmtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(full_path)))
        if os.path.isdir(full_path):
            path_list['dirs'].append({'d_name': item, 'd_mtime': fmtime})
        else:
            path_list['files'].append({'f_name': item, 'f_fsize': str(fsize/1000) + 'KB', 'f_mtime': fmtime})
    return path_list



# 当前目录下文件总数
def file_total(currpath):
    return sum([len(files) for root, dirs, files in os.walk(currpath)])


# 递归列出所请路径下的全部文件和文件夹树状图
def path_tree(request_path):
    '''''树形打印出目录结构，结果保存到f_tree文件中'''
    f_tree = open('/tmp/tree.txt', 'w')
    sys.stdout = f_tree
    for root, dirs, files in os.walk(request_path):
        # 获取当前目录下文件数
        fileCount = file_total(root)
        # 获取当前目录相对输入目录的层级关系,整数类型
        level = root.replace(request_path, '').count(os.sep)
        # 树形结构显示关键语句
        # 根据目录的层级关系，重复显示'| '间隔符，
        # 第一层 '| '
        # 第二层 '| | '
        # 第三层 '| | | '
        # 依此类推...
        # 在每一层结束时，合并输出 '|____'
        indent = '| ' * 1 * level + '|____'
        print('%s%s  --total:%s' % (indent, os.path.split(root)[1], fileCount))

        for file in files:
            indent = '| ' * 1 * (level + 1) + '|____'
            print('%s%s' % (indent, file))
    f_tree.close()

    with open('/tmp/tree.txt', 'r') as f:
        return f.read()


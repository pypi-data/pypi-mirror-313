import os
import glob
from colorama import init, Fore

init()

def findFile(dirs, file_suffix_to_find):
    # 遍历每个文件夹路径
    fileFound=[]
    for folder_path in dirs:
        matching_files=[]
        # 构建要删除的文件路径模式
        for suffix in file_suffix_to_find:

            files_to_find= os.path.join(folder_path, suffix)
        # 获取匹配模式的文件列表
            matching_files += glob.glob(files_to_find)
        print('\n',folder_path,end=':\n')
        for m in sorted(matching_files):
            # 获取文件名
            file_name = m.split(os.sep)[-1]
            # 获取文件大小并格式化字符串
            file_size = "%3.1f %s" % (os.path.getsize(m) / 1000, 'KB')
            # 打印文件名（不着色）
            print('  ', file_name[:7], end=' ')
            # 打印文件大小，并设置为红色
            print(Fore.RED + file_size, end=' ')
            # 重置颜色设置
            print(Fore.RESET,end=' ')
            #print('     ',m.split(os.sep)[-1], Fore.RED+"%3.1f %s" % (os.path.getsize(m) / 1024,'KB'),end='  ')

        #print('\n')
        fileFound.append(matching_files)
    return fileFound


def delete_files_with_suffix(dirs, file_suffix_to_delete):
    # 遍历每个文件夹路径
    i=0
    for folder_path in dirs:
        # 构建要删除的文件路径模式
        #files_to_delete = os.path.join(folder_path, f'*.{file_suffix_to_delete}')
        files_to_delete = os.path.join(folder_path, file_suffix_to_delete)

        # 获取匹配模式的文件列表
        matching_files = glob.glob(files_to_delete)
        print(matching_files,':')
        # 遍历匹配的文件并删除
        for file_path in matching_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    i=i+1
                    print(f'Deleted file {i}: {file_path}')
                else:
                    print(f'File does not exist: {file_path}')
            except Exception as e:
                print(f'Error deleting {file_path}: {e}')





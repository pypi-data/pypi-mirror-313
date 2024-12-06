# -*- coding: UTF-8 –*-
import os
import platform
import subprocess
from bypy import ByPy


class BaiDu:
    """
    如果通过调用命令行终端运行, 云端路径必须使用linux格式，不要使用windows格式,否则在windows系统里面会上传失败(无法在云端创建文件)
    """
    def __init__(self):
        self.local_path = None
        self.remote_path = None
        self.skip = ['.DS_Store', '.localized', 'desktop.ini', '$RECYCLE.BIN', 'Icon']
        self.delete_remote_files = ['.DS_Store', '.localized', 'desktop.ini', '$RECYCLE.BIN', 'Icon']
        self.bp = ByPy()

    def upload_dir(self, local_path, remote_path):
        """
        上传整个文件夹，执行完后删除指定文件
        如果通过调用命令行终端运行, 《云端路径!!》必须使用linux格式，不要使用反斜杆,否则在windows系统里面会上传失败
        """
        self.local_path = local_path
        self.remote_path = remote_path.replace('\\', '/')
        if not os.path.exists(self.local_path):
            print(f'{self.local_path}: 本地目录不存在，没有什么可传的')
            return

        if platform.system() == 'Windows':
            self.bp.upload(localpath=self.local_path, remotepath=self.remote_path.replace('\\', '/'))  # 上传文件到百度云
        else:
            command = f'bypy upload "{self.local_path}" "{self.remote_path}" --on-dup skip'  # 相同文件跳过
            try:
                subprocess.run(command, shell=True)
            except Exception as e:
                print(e)
        self.delete_files()  # 最好是在内部执行删除, 避免路径异常

    def upload_file(self, local_path, remote_path):
        """
        上传文件夹，按单个文件上传，可以跳过指定文件
        《云端路径!!》必须使用linux格式
        """
        self.local_path = local_path
        self.remote_path = remote_path.replace('\\', '/')
        if not os.path.exists(self.local_path):
            print(f'{self.local_path}: 本地目录不存在，没有什么可传的')
            return

        files = os.listdir(self.local_path)
        for file in files:
            if os.path.isfile(os.path.join(self.local_path, file)):
                if file in self.skip:
                    continue
                lc_path = os.path.join(self.local_path, file)
                rt_path = os.path.join(self.remote_path, file).replace('\\', '/')
                print(f'上传: {file}')
                self.bp.upload(localpath=lc_path, remotepath=rt_path)  # 上传文件到百度云
            elif os.path.isdir(os.path.join(self.local_path, file)):
                for root, dirs, files in os.walk(os.path.join(self.local_path, file), topdown=False):
                    for name in files:
                        if name in self.skip:
                            continue
                        lc_path = os.path.join(root, name)
                        rt_path = lc_path.replace(self.local_path, self.remote_path).replace('\\', '/')
                        print(f'上传: {name}')
                        self.bp.upload(localpath=lc_path, remotepath=rt_path)  # 上传文件到百度云

    def delete_files(self):
        """ 移除云端文件，位于 self.remote_path 文件夹下的子文件 """
        for delete_file in self.delete_remote_files:
            self.bp.remove(remotepath=f'{self.remote_path.replace('\\', '/')}/{delete_file}')  # 移除文件

    def download_dir(self, local_path, remote_path):
        """ 下载文件夹到本地 """
        self.local_path = local_path
        self.remote_path = remote_path.replace('\\', '/')
        if not os.path.exists(self.local_path):
            os.mkdir(self.local_path)

        self.bp.download(localpath=f'{self.local_path}', remotepath=f'{self.remote_path.replace('\\', '/')}')


if __name__ == '__main__':
    pass
    import datetime
    upload_path = f'windows/{str(datetime.date.today().strftime("%Y-%m"))}/{str(datetime.date.today())}'
    b = BaiDu()
    # b.upload_dir(local_path='/Users/xigua/Downloads', remote_path=upload_path)
    b.download_dir(local_path='/Users/xigua/Downloads', remote_path=upload_path)

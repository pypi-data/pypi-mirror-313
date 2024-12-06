import os
import sys
import win32com.client
import time
import multiprocessing
import psutil
from pywinauto.application import Application
import warnings
from mdbq.config import set_support

warnings.filterwarnings('ignore')
top_path = os.path.realpath(os.path.dirname(sys.argv[0]))  # 程序运行目录, 打包时使用
sys.path.append(top_path)


class RefreshAll:
    def __init__(self):
        self.my_conf = os.path.join(set_support.SetSupport(dirname='support').dirname, '.my_conf')
        self.pbix_path = os.path.join(set_support.SetSupport(dirname='support').dirname, 'ref_list.txt')
        self.excel_path = os.path.join(set_support.SetSupport(dirname='support').dirname, 'ref_list.txt')
        self.run_py_path = 'run_py'
        self.procname = 'PBIDesktop.exe'

    def refresh_pbix(self):
        # 刷新 PBI
        if not os.path.exists(self.pbix_path):
            print(f'{self.pbix_path}: PBIxx file not found. ')
            return
        with open(self.pbix_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
            content = [item.strip() for item in content if not item.strip().startswith('#') and not item.strip().startswith('[')]
            pbix_list = [item for item in content if item]

        if not pbix_list:
            return
        for filename in pbix_list:
            if filename.endswith('.pbix'):
                newfile = os.path.join(self.run_py_path, filename)
                """刷新程序"""
                for es in range(4):
                    try:
                        print(f'正在刷新 >>>{filename}')
                        self.pbi(path=newfile)
                        print('文件刷新 >>>' + filename)
                        break
                    except Exception as e:
                        print(e)
                        print('报错的文件 >>>' + filename + ' >> ' + str(es + 1))

    def refresh_excel(self):
        # 刷新 excel
        if not os.path.exists(self.excel_path):
            print(f'{self.excel_path}: Excel file not found. ')
            return
        with open(self.excel_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
            content = [item.strip() for item in content if not item.strip().startswith('#')]
            excel_list = [item for item in content if item]

        if not excel_list:
            return
        for filename in excel_list:
            if filename.endswith('.xlsx'):
                try:
                    print(f'正在刷新 >>>{filename}')
                    path = os.path.join(top_path, self.run_py_path, filename)  # 拼接文件路径
                    xlapp = win32com.client.Dispatch('Excel.Application')  # 创建Excel程序App
                    xlapp.Visible = False  # 窗口是否可见
                    xlapp.DisplayAlerts = False  # 是否显示警告信息
                    wb = xlapp.Workbooks.Open(path)
                    conjuncts = wb.Connections.Count  # 统计工作簿含有多少外部链接
                    if conjuncts == 0:
                        wb.Close(SaveChanges=False)
                        xlapp.Quit()
                    else:
                        time.sleep(2)
                        wb.RefreshAll()
                        xlapp.CalculateUntilAsyncQueriesDone()
                        time.sleep(2)
                        wb.Save()
                        wb.Close(SaveChanges=True)
                        xlapp.Quit()
                    print('文件刷新 >>>' + filename)
                except Exception as e:
                    print(e)

    def refresh_excel2(self, excel_file):
        # 刷新 excel
        if excel_file.endswith('.xlsx'):
            try:
                print(f'正在刷新 >>>{excel_file}')
                xlapp = win32com.client.Dispatch('Excel.Application')  # 创建Excel程序App
                xlapp.Visible = False  # 窗口是否可见
                xlapp.DisplayAlerts = False  # 是否显示警告信息
                wb = xlapp.Workbooks.Open(excel_file)
                conjuncts = wb.Connections.Count  # 统计工作簿含有多少外部链接
                if conjuncts == 0:
                    wb.Close(SaveChanges=False)
                    xlapp.Quit()
                else:
                    time.sleep(2)
                    wb.RefreshAll()
                    xlapp.CalculateUntilAsyncQueriesDone()
                    time.sleep(2)
                    wb.Save()
                    wb.Close(SaveChanges=True)
                    xlapp.Quit()
                print('文件刷新 >>>' + excel_file)
            except Exception as e:
                print(e)

    def pbi(self, path, _timeout=300):
        """
        这是原本属于独立的库模块:  pbix_refresh
        path: pbi文件路径
        _timeout: 刷新等待时间
        如果连接失败，请将 power bi 文件名的特殊字符(空格等)去掉或改为英文文件名试试
        """
        # 关闭已打开的 power bi进程
        for proc in psutil.process_iter():
            if proc.name() == self.procname:
                proc.kill()
        time.sleep(1)

        # 启动 Power bi
        os.system('start "" "' + path + '"')
        time.sleep(5)

        # 通过 connect 方法连接进程
        app = Application(backend='uia').connect(path=self.procname)
        # title_re可以通过正则表达式连接：".*Power BI Desktop", 仅限 2023年9月之前的 Power bi版本
        # 2023年10月之后的版本没有此窗口后缀, 因此需用文件名找窗口
        # 如果同时打开了其他同名的文件（非 power bi文件时）, 可能会引发错误
        _filename = os.path.splitext(os.path.basename(path))[0]  # 文件名不含后缀
        win = app.window(title_re=f'{_filename}.*?')  # 连接 pbi 窗口
        time.sleep(10)
        # win.print_control_identifiers()  # 打印窗口全部信息, 推荐使用 inspect 开发工具查询窗口句柄信息
        num = 0
        while True:
            try:
                win['刷新'].wait("enabled", timeout=_timeout)
                time.sleep(3)
                win['刷新'].click()
                break
            except:
                print(f'{path}, 未识别窗口句柄, 连接超时')
                num += 1
                if num > 1:
                    break

        num = 0
        while True:
            try:
                win['保存'].wait("enabled", timeout=_timeout)  # timeout 通过"保存"按键状态, 等待刷新窗口关闭, 时间不要设置太短
                time.sleep(3)
                win['保存'].click()
                break
            except:
                print(f'{path}, 未识别窗口句柄, 文件未保存')
                num += 1
                if num > 1:
                    break
        # win.type_keys("^s")
        win.wait("enabled", timeout=15)
        win.close()

        # 关闭进程
        for proc in psutil.process_iter():
            if proc.name() == self.procname:
                proc.kill()


if __name__ == '__main__':
    # r = RefreshAll()
    # # r.refresh_pbix()
    # r.refresh_excel()
    pass

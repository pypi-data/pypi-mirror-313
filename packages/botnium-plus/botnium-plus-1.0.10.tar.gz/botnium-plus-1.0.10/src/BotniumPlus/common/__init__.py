__version__ = "1.0.9"

from datetime import datetime, timedelta
import os
import shutil
from typing import List
from clicknium import clicknium as cc, locator, ui
from time import sleep
import clr
import openpyxl
from BotniumPlus.common.models import TypeMothod

from BotniumPlus.common.utils import Utils

source_path = Utils.get_libfolder()
dlls = Utils.get_import_dlls(source_path)
for dll in dlls:
    dll_path = os.path.join(source_path, dll)
    clr.AddReference(dll_path)
from CSharpRPA.FileHelpers import *
from CSharpRPA.RegisterHelpers import *
from CSharpRPA.UI import *
from CSharpRPA import *
from Webhook.Toolkit import *
import KeyboardCollection as kb
# clr.AddReference(os.path.join(os.getcwd(), "lib", "KeyboardCollection.dll"))

class CellType:
    string = "string"
    numeric = "numeric"
    date = "date"
    pass

def printf(msg):
    try:
        print(str(msg).replace('\xa0', ' '))
        pass
    except:
        pass
    
'''获取文件夹下指定后缀的文件 如png'''
def get_files(filepath, target_suffix):
    match_files = []
    files = os.listdir(filepath)
    for file in files:
        if '.' in file:
            suffix = file.split('.')[-1]
            if target_suffix == '*' or suffix == target_suffix:
                match_files.append(os.path.join(filepath, file))
    return match_files

'''如果指定文件存在则删除'''
def remove_file_if_exists(filepath):
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        finally:
            # 忽略异常
            pass

def parse_month_zh(month):
        if month == 1:
            return '一月'
        if month == 2:
            return '二月'
        if month == 3:
            return '三月'
        if month == 4:
            return '四月'
        if month == 5:
            return '五月'
        if month == 6:
            return '六月'
        if month == 7:
            return '七月'
        if month == 8:
            return '八月'
        if month == 9:
            return '九月'
        if month == 10:
            return '十月'
        if month == 11:
            return '十一月'
        if month == 12:
            return '十二月'
        pass


'''
Function Keys: [enter],[esc],[alt],[tab],[backspace],[clear],[shift],[capelock],[ctrl]
'''
def input_function(func):
    keyop = kb.Wingring0Keyboard()  
    keyop.Input(func)
    sleep(0.3)
    
'''清除输入，times为N表示点击N次Backspace按键'''
def clear_text(times, type: TypeMothod = TypeMothod.Ring):
    if type == TypeMothod.Ring:
        keyop = kb.Wingring0Keyboard()  
        for i in range(0, times):
            keyop.Input("[backspace]")
            sleep(0.3)
    else:
        keyop = kb.AutoKeyboard()
        sleep(2)
        for i in range(0, times):
            keyop.InputFunctionKey("{BACKSPACE}")
            sleep(0.3)


def input_text(text, type: TypeMothod = TypeMothod.Ring):
    '''输入文本，默认winring方式'''
    if type == TypeMothod.Ring:
        keyop = kb.Wingring0Keyboard()
        for c in text:
            keyop.Input(c)
            sleep(0.6)
    else:
        keyop = kb.AutoKeyboard()
        sleep(2)
        keyop.Input(text, 300)



def monitor_file_download(folder, lastDateTime, extensions, timeout = 60):
    '''监听下载文件路径'''
    monitor = FileMonitor(folder, lastDateTime, extensions, timeout)
    file_path = monitor.GetDownloadFilePath()
    # sleep(10) # 某些文件下载会扫描
    return file_path

'''删除指定路径下匹配的文件'''
def remove_files(folder, searchPattern):
    DirectoryHelper.RemoveFiles(folder, searchPattern)

'''dlt格式转csv（如：工商银行流水文件）'''
def dlt2Csv(file, startIndex):
    csvPath = DltFileHelper.ToCsv(file, startIndex)
    return csvPath

def read_pdf_text(path) -> str:
    '''读取pdf文本'''        
    return PdfHelper.ReadText(path)

def pdf_to_images(path, image_folder) -> List[str]:
    '''pdf文件转为图片'''
    return PdfHelper.ConvertToImages(path, image_folder)

def check_and_create_folder(folder_path):
    """
    如果文件夹不存在就创建文件夹
    """
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)  

def move_file(source, destination):
    '''
    将文件从 source 移动到 destination
    '''
    targetFileDir = os.path.dirname(destination)
    if not os.path.exists(targetFileDir):
        os.makedirs(targetFileDir, exist_ok=True)
    shutil.move(source, destination)
    pass

def update_cell_value(file, cell, val, sheet_index = 0, sheet_name = '', cell_type: CellType = CellType.string):
    if str(file).endswith('.xlsx'):
        # 打开Excel文件
        workbook = openpyxl.load_workbook(file)

        # 选择工作表（如果有多个工作表）
        sheet = None
        if len(sheet_name) > 0:
            sheet = workbook[sheet_name]
            pass
        else:
            sheet = workbook.worksheets(sheet_index)

        # 更新单元格值
        sheet[cell] = val

        # 保存更改
        workbook.save(file)
        pass
    else:
       ExcelHelper.UpdateCellValue(file, cell, val, sheet_index, sheet_name, cell_type)
    pass

def write_data_to_excel(file, data, sheet_index, start_row, start_col):
    '''写入数据到excel'''
    ExcelHelper.WriteData(file, data, sheet_index, start_row, start_col)
    pass

def remove_readonly_attribute(file):
    ExcelHelper.RemoveReadOnly(file)
    pass

def remove_readonly_attribute(file):
    ExcelHelper.RemoveReadOnly(file)
    pass
def remove_excel_protection(file, pwd):
    ExcelHelper.RemoveProtection(file, pwd)
    pass
def excel_to_xls(file, output_file = ''):
    '''将指定excel转为 *.xls'''
    try:
        ExcelHelper.SaveAsXls(file, output_file)
        return True
    except Exception as ex:
        print(str(ex))
        return False
    pass

def excel_to_xlsx(file, output_file = ''):
    '''将指定excel转为 *.xlsx'''
    try:
        ExcelHelper.SaveAsXlsx(file, output_file)
        return True
    except Exception as ex:
        print(str(ex))
        return False
    pass

def write_data_to_excel(file, data, sheet_index, start_row, start_col):
    '''写入数据到excel'''
    ExcelHelper.WriteData(file, data, sheet_index, start_row, start_col)
    pass

def remove_excel_rows(file, sheet_index, start_row, count = 1):
    '''删除（HSSFWorkbook）excel行'''
    '''sheet_index: 工作表索引，从0开始'''
    '''start_row:从1开始'''
    '''count：移除的行数量'''
    ExcelHelper.RemoveRows(file, sheet_index, start_row, count)
    pass

def upload_ftp_file(file, remote_path, user_id, password, server, port = 21):
    return FtpFileProxy(user_id, password, server, port).UploadFile(file, remote_path)

def upload_sftp_file(file, remote_path, user_id, password, server, port = 21):
    return SFtpFileProxy(user_id, password, server, port).UploadFile(file, remote_path)

'''
配置选项及对应10进制几个组合为：
SSL2.0   00000008(8)
SSL3.0   00000020(32)
TLS1.0 00000080(128)
TLS1.1 00000200(512)
TLS1.2 00000800(2048)

TLS1.3 00002000(8192)
TLS1.1 TLS1.2   00000a00(2560)
SSL3.0 TLS1.0   000000a0(160)  //32+128=160
SSL3.0 TLS1.0 TLS1.1   000002a0(672)      
SSL3.0 TLS1.0 TLS1.2   000008a0(2208)
SSL3.0 TLS1.0 TLS1.1 TLS1.2   00000aa0(2720)
SSL2.0 SSL3.0 TLS1.0 TLS1.1 TLS1.2 00000aa8(2728)
链接：https://blog.csdn.net/dong123ohyes/article/details/127983040
'''
def set_secure_protocols(v):
    IESettings.SetSecureProtocols(v)

def enable_TLS1_2():
    setSecureProtocols(2720)
    pass

def disable_TLS1_2():
    setSecureProtocols(672)
    pass

def setDefaultProtocols():
    setSecureProtocols(160)
    pass

def disable_chrome_prompt(profile = 'Default'):
    return ChromeHelper.DisablePrompt(profile)

def get_local_ip():
    return MachineHelper.GetLocalIP()
    pass

def toast(message, title = '', duration = 2):
    ToastHelper.Show(title, message, duration)
    pass

def match_image(smallImg, bigImg, show = False):
    '''匹配图片1在图片2中的位置'''
    return CvHelper.Match(smallImg, bigImg, show)

def notify_text(message, title = '', url = ''):
    '''发送文本通知'''
    webhookService = WebhookService(url)
    if not url:
        _config = WebhookConfig()
        _config.Url = config.webhook_url
        _config.Keyword = config.webhook_keyword
        _config.Sign = config.webhook_sign
        webhookService = WebhookService(_config)
        pass

    res = webhookService.SendMarkdown(str(message).rstrip(' ').rstrip('\n'), title)
    if res and res.Message:
        print(res.Message)
    pass

def notify_file(file_path, url = ''):
    webhookService = WebhookService(url)
    if not url:
        _config = WebhookConfig()
        _config.Url = config.webhook_url
        _config.Keyword = config.webhook_keyword
        _config.Sign = config.webhook_sign
        _config.AppKey = config.webhook_app_key
        _config.AppSecret = config.webhook_app_secret
        webhookService = WebhookService(_config)
        pass
    res = webhookService.SendFile(file_path)
    if res and res.Message:
        print(res.Message)
    pass
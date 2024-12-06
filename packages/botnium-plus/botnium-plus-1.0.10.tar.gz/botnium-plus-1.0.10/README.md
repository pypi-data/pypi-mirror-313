Python toolkits for RPA projects.
- logging
- utility methods
- cc extensions

Sample
``` python
import BotniumPlus as bot
import BotniumPlus.logger as logger
from BotniumPlus.common import *
from clicknium import clicknium as cc, locator

logger = logger.logger
bot.is_existing(locator.explorer.edit_name)  # 判断是否存在
bot.wait_appear(locator.explorer.edit_name)  # 等待元素出现
bot.try_click(locator.explorer.edit_name, wait_timeout=10)  # 如果元素出现，则点击。否则忽略

logger.debug('Debug test logging')
logger.info('Info test logging')

remove_file_if_exists("")  # 移除文件如果存在
toast('Hello')  # Toast通知

```

工具方法列表：
- printf  打印文本，解决文本如果含有不可见字符无法打印的问题
- get_files  获取指定路径下特定后缀的文件列表
- remove_file_if_exists  如果指定文件存在则删除
- parse_month_zh  将数字转为中文月份，比如把1转为"一月"
- input_function WinRing发送功能键
- clear_text  模拟发送退格键，支持WinRing和幽灵键鼠
- input_text  模拟输入文本，支持WinRing和幽灵键鼠
- monitor_file_download  监听文件下载
- remove_files  删除指定路径下的文件，支持通配符
- read_pdf_text  读取PDF文本
- pdf_to_images  将PDF转为图片，支持多页
- check_and_create_folder  检查文件夹是否存在，不存在则创建
- move_file  移动文件，文件夹不存在则自动创建
- update_cell_value  更新excel单元格的值，支持 .xls 和 .xlsx 
- write_data_to_excel  将数据写入excel区域 （HSSFWorkbook）
- remove_excel_rows 移除excel指定的行（HSSFWorkbook）
- upload_sftp_file  上传文件到SFTP
- set_secure_protocols  更新IE TLS SSL安全值
- disable_chrome_prompt  禁止Chrome弹出恢复提示框
- get_local_ip  获取本机IP
- toast  在windows 右下角弹出toast 提示框
- match_image  匹配滑块缺口在大图中的位置信息，要求缺口背景颜色单一
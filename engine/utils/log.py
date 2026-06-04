"""
日志模块，导出若干个用于日志记录的函数。
整体逻辑分为两层，loguru负责日志文件的记录（默认关闭），Rich Console负责控制台的格式化输出。
 - info、warning、error、success 根据语义有其相应的颜色
 - panel 用来打印一个对象，以面板形式呈现，可以添加标题
 - rule 用来打印一个分割线，标题为输入的字符串
 - use_loggerfile 用来设置日志文件路径，这能让日志同时输出到控制台和文件中
 - export_to_html 用来将Rich Console的内容导出为HTML文件，方便保存和分享日志内容
"""
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty

console = Console(record=True) # 创建一个Rich的Console对象，用于格式化输出日志到控制台
logger.remove() # 取消loguru的默认日志到终端，咱们让Console代劳

def info(msg):
    console.log(f"[green][常规] {msg}[/green]")
    logger.info(msg)


def warning(msg):
    console.log(f"[yellow][警告] {msg}[/yellow]")
    logger.warning(msg)


def error(msg):
    console.log(f"[red][出错] {msg}[/red]")
    logger.error(msg)
    
    
def success(msg):
    console.log(f"[bold blue][成功] {msg}[/bold blue]")
    logger.info(f"[SUCCESS] {msg}")
      
    
def panel(obj, title=None):
    console.print(Panel(Pretty(obj, indent_guides=True), title=title, expand=False))
    logger.info(f"[OBJ][{type(obj).__name__}] {obj}")
    
    
def rule(title):
    console.rule(title)
    logger.info(f"[RULE] {title}")
        
    
def use_loggerfile(output_dir):
    """
    输入一个输出目录，将日志文件设置为该目录下的log.log
    主动触发，否则不记录日志到本地
    """
    logger.add(f"{output_dir}/log.log", rotation="500 MB")
    info(f"日志文件：'{output_dir}/log.log'")
    
    
def export_to_html(html_path):
    """
    将Rich Console的内容导出为HTML文件
    """
    html_content = console.export_html()
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
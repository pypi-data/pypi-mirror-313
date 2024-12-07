import pandas as pd
from tdxtrader.logger import logger
from tdxtrader.anis import RED, GREEN, YELLOW, BLUE, RESET

# 自定义函数处理格式不正确的行
def handle_bad_lines(bad_line):
    # 将 "新 和 成" 替换为 "新和成"
    stock_list = ['新 和 成', '五 粮 液', '农 产 品', '南 玻A', '万 科A', '新 华 都', '奥 特 迅', '三 力 士', '诺 普 信', '达 意 隆', '海 利 得', '全 聚 德', '怡 亚 通', '粤 传 媒', '红 宝 丽', '远 望 谷', '报 喜 鸟', '安 纳 达', '生 意 宝', '金 螳 螂', '兔 宝 宝', '南 京 港', '苏 泊 尔', '七 匹 狼', '新 大 陆', '中 关 村', '新 希 望', '张 裕A', '罗 牛 山', '鲁 泰A', '英 力 特', '柳 工', '渝 开 发', '金 融 街', '盐 田 港', '深 赛 格', '特 力A']
    fixed_line = ' '.join(bad_line)
    for stock in stock_list:
        fixed_stock = stock.replace(' ', '')
        fixed_line = fixed_line.replace(stock, fixed_stock)
    
    # 检查修复后的行是否符合预期格式
    fields = fixed_line.split()
    if len(fields) == 8:
        return fields
    else:
        logger.error(f"【错误行】 {' '.join(bad_line)}")
        return None  # 返回 None 表示跳过该行

def read_file(file_path):
    COLUMNS = ['code', 'name', 'date', 'time', 'price', 'rate', 'value', 'sign']
    try:
        # 检查文件是否为空
        with open(file_path, 'r', encoding='gb2312') as file:
            first_line = file.readline()
            if not first_line:  # 文件为空
                return pd.DataFrame(columns=COLUMNS)
        
        df = pd.read_csv(file_path, sep=r'\s+', header=None, encoding='gb2312', on_bad_lines=handle_bad_lines, engine='python', dtype={0: str})
        df.columns = COLUMNS
        return df
    except Exception as e:
        logger.error(f"读取文件时发生错误: {e}")
        return None

def clear_file_content(file_path):
    try:
        with open(file_path, 'w', encoding='gb2312') as file:
            file.truncate(0)
        logger.debug(f"【重置文件】内容已清空")
    except Exception as e:
        logger.error(f"清空文件内容时发生错误: {e}")
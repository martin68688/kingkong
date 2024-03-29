
import pandas as pd
import time
from urllib.request import urlopen  # python自带爬虫库
import urllib.request


# # =====直接通过网址获取数据
# import sys
# import requests
# url = 'https://27.push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.600000&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&end=20500101&lmt=120'
# r = requests.get(url).json()['data']['klines']
# l = [i.split(',') for i in r]
# df = pd.DataFrame(l)
# df = df[[0, 1, 2, 3, 4, 5, 6]]
# df.columns = ['交易日期', '开盘价', '收盘价', '最高价', '最低价', '成交量', '成交额']
# print(df)
# sys.exit()



def requestForNew(url, max_try_num=10, sleep_time=5):
    headers = {
        'Referer': 'http://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'
    }
    request = urllib.request.Request(url, headers=headers)
    for i in range(max_try_num):
        response = urlopen(request)
        if response.code == 200:
            return response.read().decode('gbk')
        else:
            print("链接失败", response)
            time.sleep(sleep_time)





stock_code_list = ['sh600001', 'sz000001', 'sh600002', 'sh600601', 'sh601595', 'sz002174', 'sz000977', 'sh600271', 'sz000988', 'sz002605'] #在后面添加,' '即可，注意一定要用英文符号
url = "https://hq.sinajs.cn/list=" + ",".join(stock_code_list)



#抓取数据
content = requestForNew(url)
# print(content)
# exit()

# 转换成DataFrame
data_line = content.strip().split('\n')  # 去掉文本前后的空格、回车等。每行是一个股票的数据
data_line = [i.replace('var hq_str_', '').split(',') for i in data_line]
df = pd.DataFrame(data_line)

# 对DataFrame进行整理
df[0] = df[0].str.split('="')
df['stock_code'] = df[0].str[0].str.strip()
df['stock_name'] = df[0].str[-1].str.strip()
df['candle_end_time'] = pd.to_datetime(df[30] + ' ' + df[31])  # 股票市场的K线，是普遍以当跟K线结束时间来命名的

rename_dict = {1: 'open', 2: 'pre_close', 3: 'close', 4: 'high', 5: 'low', 6: 'buy1', 7: 'sell1',
               8: 'volume', 9: 'amount', 32: 'status'}  # 自己去对比数据，会有新的返现
df.rename(columns=rename_dict, inplace=True)
df['status'] = df['status'].str.strip('";')
df = df[['stock_code', 'stock_name', 'candle_end_time', 'open', 'high', 'low', 'close', 'pre_close', 'amount', 'volume',
         'buy1', 'sell1', 'status']]
print(df)

# 保存数据
# df.to_csv('homework2_stock_data.csv', index=False)
import os

# 指定保存文件夹路径
folder_path = 'C:/Users/33194/Desktop'

# 拼接文件路径
file_path = os.path.join(folder_path, 'homework2_stock_data.csv')

# 保存文件
df.to_csv(file_path, index=False)





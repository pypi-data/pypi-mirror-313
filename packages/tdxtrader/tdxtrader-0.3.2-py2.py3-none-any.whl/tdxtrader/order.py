from xtquant import xtconstant
import time
import logging
import math
from tdxtrader.file import read_file
from tdxtrader.utils import add_stock_suffix, timestamp_to_datetime_string, convert_to_current_date
from tdxtrader.anis import RED, GREEN, YELLOW, BLUE, RESET
from tdxtrader.logger import logger

def get_volume(paload, row):
    if paload.get('size') is not None:
        return paload.get('size')
    elif paload.get('amount') is not None:
        if paload.get('price') > 0:
            return math.floor(paload.get('amount') / paload.get('price') / 100) * 100
        else:
            return math.floor(paload.get('amount') / row.get('price') / 100) * 100
    else:
        return 100

def create_order(xt_trader, account, file_path, previous_df, buy_sign, sell_sign, buy_event, sell_event):
    current_df = read_file(file_path)
    if current_df is not None:
        if previous_df is not None:
            # 比较前后两次读取的 DataFrame，找出新增的行
            new_rows = current_df[~current_df.index.isin(previous_df.index)]
            if not new_rows.empty:
                for index, row in new_rows.iterrows():

                    stock_code = add_stock_suffix(row['code'])

                    price_type_map = {
                        '市价': xtconstant.LATEST_PRICE,
                        '限价': xtconstant.FIX_PRICE
                    }
                    
                    if row['sign'] == buy_sign:
                        buy_paload = buy_event(row, xt_trader)
                        xt_trader.order_stock_async(
                            account=account, 
                            stock_code=stock_code, 
                            order_type=xtconstant.STOCK_BUY, 
                            order_volume=get_volume(buy_paload, row), 
                            price_type=price_type_map.get(buy_paload.get('type')) or xtconstant.LATEST_PRICE,
                            price=buy_paload.get('price') or -1,
                            order_remark=row.get('name')
                        )
                    elif row['sign'] == sell_sign:
                        position = xt_trader.query_stock_position(account, stock_code)
                        if position is not None:
                            sell_paload = sell_event(row, position, xt_trader)
                            xt_trader.order_stock_async(
                                account=account, 
                                stock_code=stock_code, 
                                order_type=xtconstant.STOCK_SELL, 
                                order_volume=get_volume(sell_paload, row),
                                price_type=price_type_map.get(sell_paload.get('type')) or xtconstant.LATEST_PRICE,
                                price=sell_paload.get('price') or -1,
                                order_remark=row.get('name')
                            )
                        else:
                            logger.warning(f"{YELLOW}【无持仓】{RESET}没有查询到持仓信息，不执行卖出操作。股票代码：{stock_code}, 名称：{row['name']}")
                
        return current_df
    
    return None

def cancel_order(xt_trader, account, cancel_after):
    if cancel_after is not None:
        orders = xt_trader.query_stock_orders(account, cancelable_only=True)
        for order in orders:
            order_time = convert_to_current_date(order.order_time)
            # print(order_time, time.time())
            # print(timestamp_to_datetime_string(order_time), timestamp_to_datetime_string(time.time()))
            if time.time() - order_time >= cancel_after:
                xt_trader.cancel_order_stock_async(account, order.order_id)
                # if seq > 0:
                #     logger.warning(f"{YELLOW}【已撤单】{RESET}代码: {order.stock_code} 订单编号：{order.order_id} 下单时间: {timestamp_to_datetime_string(order.order_time)} 撤单时间：{timestamp_to_datetime_string(time.time())}")
                # else:
                #     logger.error(f"【撤单失败】代码: {order.stock_code} 订单号：{order.order_id} 下单时间: {timestamp_to_datetime_string(order.order_time)} 撤单时间：{timestamp_to_datetime_string(time.time())}")
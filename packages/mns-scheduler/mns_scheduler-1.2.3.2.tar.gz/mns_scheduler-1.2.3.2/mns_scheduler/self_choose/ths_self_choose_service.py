import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_common.api.ths.self_choose.ths_self_choose_api as ths_self_choose_api
import mns_common.constant.db_name_constant as db_name_constant
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.api.ths.zt.ths_stock_zt_pool_api as ths_stock_zt_pool_api
import mns_common.component.common_service_fun_api as common_service_fun_api
from datetime import datetime
import mns_common.utils.data_frame_util as data_frame_util
from functools import lru_cache
import mns_common.constant.self_choose_constant as self_choose_constant
import mns_common.component.trade_date.trade_date_common_service_api as trade_date_common_service_api

mongodb_util = MongodbUtil('27017')

# 固定的选择
# fixed_optional_list = ['USDCNH', 'XAUUSD',
#                        '881279',
#                        '886054', '881153', '881157', '881155',
#                        '885736', '881124', '886078',
#                        '881145', '886073', '881160', '885730',
#                        '886076', '883418', '881169', '885530',
#                        '510300', '512100',
#                        'CN0Y',
#                        '1B0888',
#                        '1A0001',
#                        '399001',
#                        '399006',
#                        '1B0688',
#                        '899050',
#                        'HSI',
#                        'HS2083',
#                        ]

# 固定的选择
fixed_optional_list = ['899050', '881157']


@lru_cache()
def get_ths_cookie():
    query = {"type": "ths_cookie"}
    stock_account_info = mongodb_util.find_query_data(db_name_constant.STOCK_ACCOUNT_INFO, query)
    ths_cookie = list(stock_account_info['cookie'])[0]
    return ths_cookie


def add_fixed_optional():
    ths_cookie = get_ths_cookie()
    for symbol in fixed_optional_list:
        ths_self_choose_api.add_stock_to_account(symbol, ths_cookie)


def delete_all_self_choose_stocks():
    ths_cookie = get_ths_cookie()
    all_self_choose_stock_list = ths_self_choose_api.get_all_self_choose_stock_list(ths_cookie)
    for stock_one in all_self_choose_stock_list.itertuples():
        symbol = stock_one.code
        ths_self_choose_api.del_stock_from_account(symbol, ths_cookie)


def add_self_choose_local():
    ths_cookie = get_ths_cookie()
    # 固定自选
    self_choose_symbol_df = mongodb_util.find_all_data(db_name_constant.SELF_CHOOSE_STOCK)
    if data_frame_util.is_not_empty(self_choose_symbol_df):
        self_choose_symbol_df = self_choose_symbol_df.sort_values(by=['str_now_date'], ascending=False)
        for stock_one in self_choose_symbol_df.itertuples():
            ths_self_choose_api.add_stock_to_account(stock_one.symbol, ths_cookie)

    now_date = datetime.now()
    str_day = now_date.strftime('%Y-%m-%d')
    last_trade_day = trade_date_common_service_api.get_last_trade_day(str_day)
    last_trade_day_time = last_trade_day + " 15:00:00"
    query = {'str_now_date': {"$gte": last_trade_day_time}, "valid": True}
    self_choose_symbol_today_df = mongodb_util.find_query_data(db_name_constant.TODAY_SELF_CHOOSE_STOCK, query)
    if data_frame_util.is_not_empty(self_choose_symbol_today_df):
        self_choose_symbol_today_df = self_choose_symbol_today_df.sort_values(by=['str_now_date'], ascending=True)
        for stock_one in self_choose_symbol_today_df.itertuples():
            ths_self_choose_api.add_stock_to_account(stock_one.symbol, ths_cookie)

    query_plate = {'self_type': {
        "$in": [self_choose_constant.SELF_CHOOSE_THS_CONCEPT,
                self_choose_constant.SELF_CHOOSE_THS_INDUSTRY]}}
    self_choose_plate_df = mongodb_util.find_query_data(db_name_constant.SELF_CHOOSE_PLATE, query_plate)
    # 自选同花顺概念
    if data_frame_util.is_not_empty(self_choose_plate_df):
        self_choose_plate_df = self_choose_plate_df.sort_values(by=['str_now_date'], ascending=False)
        for stock_one in self_choose_plate_df.itertuples():
            ths_self_choose_api.add_stock_to_account(str(stock_one.self_code), ths_cookie)


# 添加最近交易股票
def add_trade_stocks():
    now_date = datetime.now()
    str_day = now_date.strftime('%Y-%m-%d')
    last_trade_day = trade_date_common_service_api.get_last_trade_day(str_day)
    query = {"$and": [{"str_day": {"$gte": last_trade_day}}, {"str_day": {"$lte": str_day}}]}
    trade_stocks_df = mongodb_util.find_query_data(db_name_constant.POSITION_STOCK, query)
    ths_cookie = get_ths_cookie()
    if data_frame_util.is_not_empty(trade_stocks_df):
        for stock_one in trade_stocks_df.itertuples():
            ths_self_choose_api.add_stock_to_account(stock_one.symbol, ths_cookie)


# 添加连板到自选
def add_continue_boards_zt_stocks():
    ths_cookie = get_ths_cookie()
    now_date = datetime.now()
    str_day = now_date.strftime('%Y-%m-%d')
    if trade_date_common_service_api.is_trade_day(str_day):
        ths_stock_zt_pool_df = ths_stock_zt_pool_api.get_zt_reason(None)
    else:
        str_day = trade_date_common_service_api.get_last_trade_day(str_day)
        ths_stock_zt_pool_df = ths_stock_zt_pool_api.get_zt_reason(str_day)
    ths_stock_zt_pool_df = ths_stock_zt_pool_df.loc[ths_stock_zt_pool_df['connected_boards_numbers'] >= 3]
    ths_stock_zt_pool_df = common_service_fun_api.exclude_st_symbol(ths_stock_zt_pool_df)
    ths_stock_zt_pool_df = ths_stock_zt_pool_df.sort_values(by=['connected_boards_numbers'], ascending=False)
    for stock_one in ths_stock_zt_pool_df.itertuples():
        ths_self_choose_api.add_stock_to_account(stock_one.symbol, ths_cookie)


# 自选股操作 删除当天自选股 增加新的连板股票  添加固定选择自选
def self_choose_stock_handle():
    delete_all_self_choose_stocks()
    # 固定自选
    add_fixed_optional()
    # 自己买入的股票
    add_trade_stocks()
    # 本地自选
    add_self_choose_local()
    # 连板股票
    add_continue_boards_zt_stocks()


if __name__ == '__main__':
    self_choose_stock_handle()

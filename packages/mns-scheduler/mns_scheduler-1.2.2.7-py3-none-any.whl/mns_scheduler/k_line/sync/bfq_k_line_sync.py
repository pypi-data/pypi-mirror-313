import os
import sys

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)

from loguru import logger
import mns_common.api.em.east_money_stock_api as east_money_stock_api
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.utils.date_handle_util as date_handle_util
import mns_common.component.common_service_fun_api as common_service_fun_api
import mns_common.api.akshare.k_line_api as k_line_api
import mns_common.component.company.company_common_service_new_api as company_common_service_new_api

mongodb_util = MongodbUtil('27017')


def sync_bfq_k_line_data(period='daily',
                         hq='hfq',
                         hq_col='stock_hfq_daily',
                         end_date='22220101',
                         symbol=None):
    stock_hfq_df = k_line_api.stock_zh_a_hist(symbol=symbol, period=period,
                                              start_date=date_handle_util.no_slash_date('1990-12-19'),
                                              end_date=date_handle_util.no_slash_date(end_date),
                                              adjust=hq)

    stock_hfq_df.rename(columns={"日期": "date", "开盘": "open",
                                 "收盘": "close", "最高": "high",
                                 "最低": "low", "成交量": "volume",
                                 "成交额": "amount", "振幅": "pct_chg",
                                 "涨跌幅": "chg", "涨跌额": "change",
                                 "换手率": "exchange"}, inplace=True)

    stock_hfq_df['symbol'] = symbol
    stock_hfq_df['_id'] = stock_hfq_df['symbol'] + '-' + stock_hfq_df['date']
    stock_hfq_df['last_price'] = round(((stock_hfq_df['close']) / (1 + stock_hfq_df['chg'] / 100)), 2)
    stock_hfq_df['max_chg'] = round(
        ((stock_hfq_df['high'] - stock_hfq_df['last_price']) / stock_hfq_df['last_price']) * 100, 2)
    stock_hfq_df['amount_level'] = round((stock_hfq_df['amount'] / common_service_fun_api.HUNDRED_MILLION), 2)
    stock_hfq_df['flow_mv'] = round(stock_hfq_df['amount'] * 100 / stock_hfq_df['exchange'], 2)
    stock_hfq_df['flow_mv_sp'] = round(stock_hfq_df['flow_mv'] / common_service_fun_api.HUNDRED_MILLION, 2)

    classification = common_service_fun_api.classify_symbol_one(symbol)
    stock_hfq_df['classification'] = classification
    stock_hfq_df = stock_hfq_df.sort_values(by=['date'], ascending=False)
    insert_data(stock_hfq_df, hq_col, symbol)
    logger.info(period + 'k线同步-' + hq + '-' + symbol)
    return stock_hfq_df


def sync_all_bfq_k_line(period='daily',
                        hq='hfq',
                        hq_col='stock_hfq_daily',
                        end_date='22220101',
                        symbol=None):
    real_time_quotes_now_es = east_money_stock_api.get_real_time_quotes_all_stocks()

    symbol_list = list(real_time_quotes_now_es['symbol'])
    # 退市公司
    de_list_company = company_common_service_new_api.get_de_list_company()
    symbol_list.extend(de_list_company)
    symbol_list = set(symbol_list)
    if symbol is not None:
        symbol_list = [symbol]
    for symbol in symbol_list:
        try:
            sync_bfq_k_line_data(period,
                                 hq,
                                 hq_col,
                                 end_date,
                                 symbol)
        except BaseException as e:
            logger.warning("同步不复权k线:{},{}", symbol, e)


def insert_data(stock_hfq_df, hq_col, symbol):
    query = {'symbol': symbol}
    tag = mongodb_util.remove_data(query, hq_col)
    success = tag.acknowledged
    if success:
        mongodb_util.insert_mongo(stock_hfq_df, hq_col)


if __name__ == '__main__':
    sync_all_bfq_k_line('daily',
                        '',
                        'stock_bfq_daily',
                        None,
                        None)

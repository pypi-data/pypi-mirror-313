import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_common.api.em.east_money_stock_api as east_money_stock_api
import mns_common.constant.db_name_constant as db_name_constant
from mns_common.db.MongodbUtil import MongodbUtil
from loguru import logger
import mns_common.component.company.company_common_service_new_api as company_common_service_new_api
import mns_common.utils.date_handle_util as date_handle_util
import mns_common.api.akshare.k_line_api as k_line_api

mongodb_util = MongodbUtil('27017')


def history_high_chg(symbol_param):
    company_info_df = company_common_service_new_api.get_company_info_info()
    begin_date = '20140722'
    end_date = '20150615'

    real_time_quotes_all_stocks_df = east_money_stock_api.get_real_time_quotes_all_stocks()
    if symbol_param is not None:
        real_time_quotes_all_stocks_df = real_time_quotes_all_stocks_df.loc[
            real_time_quotes_all_stocks_df['symbol'] == symbol_param]
    real_time_quotes_all_stocks_list_date_before = real_time_quotes_all_stocks_df.loc[
        real_time_quotes_all_stocks_df['list_date'] < 20150615]

    for company_one in real_time_quotes_all_stocks_list_date_before.itertuples():
        try:

            symbol = company_one.symbol
            stock_qfq_daily_df = k_line_api.stock_zh_a_hist(symbol=symbol, period='daily',
                                                            start_date=date_handle_util.no_slash_date(begin_date),
                                                            end_date=date_handle_util.no_slash_date(end_date),
                                                            adjust='hfq')

            if stock_qfq_daily_df.shape[0] < 100:
                continue
                logger.error("新股或者交易时间不足{}:{}", symbol, company_one.name)
            stock_qfq_daily_df = stock_qfq_daily_df.sort_values(by=['date'], ascending=True)
            first_row = stock_qfq_daily_df.iloc[0]

            open_price = first_row.open

            last_row = stock_qfq_daily_df.iloc[-1]

            close_price = last_row.close

            sum_chg = round((close_price - open_price) * 100 / open_price, 2)

            company_info_df_one = company_info_df.loc[company_info_df['_id'] == symbol]
            if company_info_df_one.shape[0] > 0:
                company_info_df_one['sum_chg'] = sum_chg
                company_info_df_one['name'] = company_one.name
                company_info_df_one = company_info_df_one[
                    ['_id',
                     'name',
                     'sum_chg',
                     'industry',
                     'first_sw_industry',
                     'second_sw_industry',
                     'third_sw_industry',
                     'em_industry',
                     'list_date',
                     'ths_concept_list_info',
                     'kpl_plate_name',
                     'kpl_plate_list_info',
                     'company_type']]
                mongodb_util.save_mongo(company_info_df_one, '2014-2015-chg-statistics')
            else:
                logger.error("该股票已经退市{}:{}", symbol, company_one.name)
        except BaseException as e:
            logger.error("出现异常{}:{}", symbol, e)


if __name__ == '__main__':
    symbol_test = None

    # qfq_k_line_df = k_line_api.stock_zh_a_hist(symbol=symbol_test, period='daily',
    #                                            start_date=date_handle_util.no_slash_date('1990-12-19'),
    #                                            end_date=date_handle_util.no_slash_date('2990-12-19'),
    #                                            adjust='hfq')

    history_high_chg(symbol_test)

import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.utils.date_handle_util as date_handle_util
from mns_common.component.classify.symbol_classify_param import stock_type_classify_param

mongodb_util = MongodbUtil('27017')


# 处理月线 周线 todo 暂时简单计算周线之和
def handle_month_week_line(k_line_info, str_day, symbol, deal_days):
    sub_stock_new_max_deal_days = stock_type_classify_param['sub_new_stock_max_deal_days']
    if deal_days > sub_stock_new_max_deal_days:
        k_line_info = handle_month_line(k_line_info, str_day, symbol)
        k_line_info = handle_week_line(k_line_info, str_day, symbol)
    else:
        k_line_info['week01'] = 0
        k_line_info['week02'] = 0
        k_line_info['week03'] = 0
        k_line_info['week04'] = 0
        k_line_info['sum_week'] = 0
        k_line_info['week_num'] = 0
        k_line_info['week_last_day'] = '19890729'

        k_line_info['sum_month'] = 0
        k_line_info['month_num'] = 0
        k_line_info['month01'] = 0
        k_line_info['month02'] = 0
        k_line_info['month01_date'] = '19890729'
        k_line_info['month02_date'] = '19890729'
    return k_line_info


# 处理月线
def handle_month_line(k_line_info, str_day, symbol):
    month_begin_day = str_day[0:7] + '-01'
    query = {"symbol": symbol,
             'date': {"$lt": date_handle_util.no_slash_date(month_begin_day)}}
    stock_hfq_monthly = mongodb_util.descend_query(query, 'stock_qfq_monthly', 'date', 2)
    month_num = stock_hfq_monthly.shape[0]
    k_line_info['month_num'] = month_num
    if month_num > 0:
        k_line_info['sum_month'] = round(sum(stock_hfq_monthly['chg']), 2)
    else:
        k_line_info['sum_month'] = 0

    if month_num == 0:
        k_line_info['month01'] = 0
        k_line_info['month02'] = 0
        k_line_info['month01_date'] = '19890729'
        k_line_info['month02_date'] = '19890729'
    elif month_num == 1:
        k_line_info['month01'] = stock_hfq_monthly.iloc[0].chg
        k_line_info['month02'] = 0
        k_line_info['month01_date'] = stock_hfq_monthly.iloc[0].date
        k_line_info['month02_date'] = '19890729'
    elif month_num == 2:
        k_line_info['month01'] = stock_hfq_monthly.iloc[0].chg
        k_line_info['month02'] = stock_hfq_monthly.iloc[1].chg
        k_line_info['month01_date'] = stock_hfq_monthly.iloc[0].date
        k_line_info['month02_date'] = stock_hfq_monthly.iloc[1].date

    return k_line_info


# 处理周线
def handle_week_line(k_line_info, str_day, symbol):
    month_begin_day = str_day[0:7] + '-01'
    query = {"symbol": symbol,
             '$and': [{'date': {"$gte": date_handle_util.no_slash_date(month_begin_day)}},
                      {'date': {"$lt": date_handle_util.no_slash_date(str_day)}}]}
    stock_hfq_weekly = mongodb_util.find_query_data('stock_qfq_weekly', query)
    week_num = stock_hfq_weekly.shape[0]
    if week_num > 0:
        stock_hfq_weekly = stock_hfq_weekly.sort_values(by=['date'], ascending=False)
        k_line_info['sum_week'] = round(sum(stock_hfq_weekly['chg']), 2)
    else:
        k_line_info['sum_week'] = 0
    k_line_info['week_num'] = week_num
    if week_num == 1:
        k_line_info['week01'] = stock_hfq_weekly.iloc[0].chg
        k_line_info['week02'] = 0
        k_line_info['week03'] = 0
        k_line_info['week04'] = 0
    elif week_num == 2:
        k_line_info['week01'] = stock_hfq_weekly.iloc[0].chg
        k_line_info['week02'] = stock_hfq_weekly.iloc[1].chg
        k_line_info['week03'] = 0
        k_line_info['week04'] = 0
    elif week_num == 3:
        k_line_info['week01'] = stock_hfq_weekly.iloc[0].chg
        k_line_info['week02'] = stock_hfq_weekly.iloc[1].chg
        k_line_info['week03'] = stock_hfq_weekly.iloc[2].chg
        k_line_info['week04'] = 0
    elif week_num >= 4:
        k_line_info['week01'] = stock_hfq_weekly.iloc[0].chg
        k_line_info['week02'] = stock_hfq_weekly.iloc[1].chg
        k_line_info['week03'] = stock_hfq_weekly.iloc[2].chg
        k_line_info['week04'] = stock_hfq_weekly.iloc[3].chg
    elif week_num == 0:
        k_line_info['week01'] = 0
        k_line_info['week02'] = 0
        k_line_info['week03'] = 0
        k_line_info['week04'] = 0
        k_line_info['week_last_day'] = month_begin_day
        k_line_info['sum_week'] = 0
        return k_line_info
    stock_hfq_weekly = stock_hfq_weekly.sort_values(by=['date'], ascending=False)
    stock_hfq_weekly_last = stock_hfq_weekly.iloc[0:1]
    k_line_info['week_last_day'] = list(stock_hfq_weekly_last['date'])[0]

    return k_line_info

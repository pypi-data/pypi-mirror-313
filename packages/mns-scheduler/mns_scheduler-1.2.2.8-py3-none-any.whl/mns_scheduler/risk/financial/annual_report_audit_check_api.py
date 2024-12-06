import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_common.component.self_choose.black_list_service_api as black_list_service_api
from mns_common.db.MongodbUtil import MongodbUtil
from datetime import datetime
from mns_common.constant.black_list_classify_enum import BlackClassify

# 年报审计意见check
mongodb_util = MongodbUtil('27017')
# 审核标准意见
OPINION_TYPE = "标准无保留意见"


def annual_report_audit_check(new_report_df, period_time):
    new_report_one_df = new_report_df.loc[new_report_df['REPORT_DATE'] == period_time]
    # 审核意见
    opinion_type = list(new_report_one_df['OPINION_TYPE'])[0]
    symbol = list(new_report_one_df['SECURITY_CODE'])[0]
    name = list(new_report_one_df['SECURITY_NAME_ABBR'])[0]
    notice_date = list(new_report_one_df['NOTICE_DATE'])[0]
    now_date = datetime.now()
    str_day = now_date.strftime('%Y-%m-%d')
    str_now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

    # 年报有问题
    if opinion_type != OPINION_TYPE:
        id_key = symbol + "_" + period_time + "_" + BlackClassify.AUDIT_PROBLEM.level_code
        black_list_service_api.save_black_stock(id_key,
                                                symbol,
                                                name,
                                                str_day,
                                                notice_date,
                                                '年报审计有问题:' + "[" + str(opinion_type) + "]",
                                                '年报审计有问题',
                                                '',
                                                BlackClassify.AUDIT_PROBLEM.up_level_code,
                                                BlackClassify.AUDIT_PROBLEM.up_level_name,
                                                BlackClassify.AUDIT_PROBLEM.level_code,
                                                BlackClassify.AUDIT_PROBLEM.level_name)

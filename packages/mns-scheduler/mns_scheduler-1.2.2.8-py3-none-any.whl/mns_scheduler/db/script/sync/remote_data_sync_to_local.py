import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_common.utils.data_frame_util as data_frame_util
from mns_scheduler.db.script.sync.remote_mongo_util import RemoteMongodbUtil
from mns_scheduler.db.script.sync.local_mongo_util import LocalMongodbUtil
from loguru import logger
import numpy as np

remote_mongodb_util = RemoteMongodbUtil('27017')
local_mongodb_util = LocalMongodbUtil('27017')

col_list = [
    'company_remark_info',
    'company_holding_info',
    'industry_concept_remark',
    'trade_date_list',
    'company_info',
    'de_list_stock',
    'kpl_best_choose_index',
    'kpl_best_choose_index_detail',
    'realtime_quotes_now_zt_new_kc_open',
    'industry_concept_remark',
    'self_black_stock',
    'self_choose_plate',
    'self_choose_stock',
    'stock_account_info',
    'ths_concept_list',
    'stock_zt_pool',
    'ths_stock_concept_detail'
]


def remote_data():
    for col in col_list:
        try:
            col_df = remote_mongodb_util.find_all_data(col)
            if data_frame_util.is_not_empty(col_df):
                result = local_mongodb_util.remove_all_data(col)
                if result.acknowledged:
                    col_df.replace([np.inf, -np.inf], 0, inplace=True)

                    local_mongodb_util.save_mongo(col_df, col)

                logger.info("同步集合完成:{}", col)
        except BaseException as e:
            logger.error("同步失败:{},{}", e, col)


if __name__ == '__main__':
    remote_data()

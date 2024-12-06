import os
import sys

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_common.constant.db_name_constant as db_name_constant
import mns_common.component.common_service_fun_api as common_service_fun_api
import mns_common.component.cache.cache_service as cache_service
import mns_common.utils.cmd_util as cmd_util
import mns_common.utils.data_frame_util as data_frame_util
from loguru import logger
from datetime import datetime
import mns_common.utils.date_handle_util as date_handle_util
from mns_common.db.MongodbUtil import MongodbUtil

mongodb_util = MongodbUtil('27017')

MAX_NUMBER_KEY = 'max_number_key'
# 实时行情同步任务 python名称
REAL_TIME_SCHEDULER_NAME = "sync_realtime_quotes_task"
# 实时行情补偿任务 python名称
REAL_TIME_TASK_NAME = "realtime_quotes_now_sync"

REAL_TIME_SCHEDULER_NAME_PATH = 'H:\\real_time_task.bat'


def get_real_time_max_number():
    number = common_service_fun_api.realtime_quotes_now_max_number(db_name_constant.REAL_TIME_QUOTES_NOW,
                                                                   'number')

    return number


# 检查数据同步最大值
def check_max_number():
    now_max_number = get_real_time_max_number()
    last_minute_number = cache_service.get_cache(MAX_NUMBER_KEY)
    cache_service.set_cache(MAX_NUMBER_KEY, now_max_number)
    if last_minute_number is None:
        return True
    elif now_max_number == last_minute_number:
        return False
    else:
        return True


#  实时行情数据同步状态check
def run_check_real_time_data_sync_status():
    now_date = datetime.now()
    if bool(1 - date_handle_util.is_trade_time(now_date)):
        return False
    flag = check_max_number()
    if bool(1 - flag):
        all_cmd_processes = cmd_util.get_all_process()
        if data_frame_util.is_empty(all_cmd_processes):
            return None
        all_cmd_processes_real_time_task = get_real_time_quotes_task(all_cmd_processes)
        if data_frame_util.is_empty(all_cmd_processes_real_time_task):
            return None
        for match_task_one in all_cmd_processes_real_time_task.itertuples():
            try:
                processes_pid = match_task_one.process_pid
                # 关闭当前进程
                cmd_util.kill_process_by_pid(processes_pid)
                # 清空临时数据表
                mongodb_util.remove_all_data(db_name_constant.REAL_TIME_QUOTES_NOW)

            except BaseException as e:
                logger.error("关闭实时行情任务异常:{}", e)
        # 重开任务进程
        cmd_util.open_bat_file(REAL_TIME_SCHEDULER_NAME_PATH)


def get_real_time_quotes_task(all_cmd_processes):
    return all_cmd_processes[
        (all_cmd_processes['total_info'].str.contains(REAL_TIME_SCHEDULER_NAME, case=False, na=False))
        | (all_cmd_processes['total_info'].str.contains(REAL_TIME_TASK_NAME, case=False, na=False))]


if __name__ == '__main__':
    while True:
        run_check_real_time_data_sync_status()

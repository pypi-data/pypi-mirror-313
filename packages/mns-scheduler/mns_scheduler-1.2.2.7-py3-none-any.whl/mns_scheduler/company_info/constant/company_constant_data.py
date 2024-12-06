import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
import pandas as pd
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.utils.data_frame_util as data_frame_util

mongodb_util = MongodbUtil('27017')


# 修改行业分类的股票
def get_fix_symbol_industry():
    return pd.DataFrame([['688480', '赛恩斯', '760103', '环境治理'],
                         ['000032', '深桑达Ａ', '730204', '通信网络设备及器件'],
                         ['688480', '赛恩斯', '640704', '自动化设备'],
                         ['603260', '合盛硅业', '220316', '有机硅'],
                         ['300559', '佳发教育', '461102', '培训教育'],
                         ['300836', '佰奥智能', '640701', '机器人'],
                         ['300293', '蓝英装备', '640701', '机器人'],
                         ['688630', '芯碁微装', '270108', '半导体设备'],
                         ['001309', '德明利', '270104', '数字芯片设计'],
                         ['600338', '西藏珠峰', '240303', '铅锌'],
                         ['300042', '朗科科技', '270108', '半导体设备'],
                         ['688507', '索辰科技', '710402', '横向通用软件'],
                         ['301387', '光大同创', '270504', '消费电子零部件及组装'],
                         ['300295', '三六五网', '430301', '物业管理'],
                         ['300947', '德必集团', '430301', '物业管理'],
                         ['300483', '首华燃气', '410301', '燃气Ⅲ'],
                         ['300215', '电科院', '410110', '电能综合服务'],
                         # 持有上海微电子装备有限公司10%的股份 国产光刻机 主要炒作在芯片概念 不在房地产
                         ['600895', '张江高科', '270108', '半导体设备'],
                         ['301112', '信邦智能', '640704', '其他自动化设备'],
                         ['002693', '双成药业', '270104', '数字芯片设计'],
                         ['000670', '盈方微', '270401', '其他电子'],
                         ['300803', '指南针', '490101', '证券'],
                         ['300085', '银之杰', '490101', '证券'],
                         ['300380', '安硕信息', '490101', '证券'],
                         ['600446', '金证股份', '490101', '证券'],
                         ['688318', '财富趋势', '490101', '证券'],
                         ['600570', '恒生电子', '490101', '证券'],
                         ['837592', '华信永道', '490101', '证券'],
                         ['830799', '艾融软件', '490101', '证券'],
                         ['300033', '同花顺', '490101', '证券'],
                         ['300399', '天利科技', '490201', '保险'],

                         # EDA软件
                         ['301269', '华大九天', '270108', '半导体设备'],
                         ['688206', '概伦电子', '270108', '半导体设备'],
                         ['301095', '广立微', '270108', '半导体设备'],

                         ],
                        columns=['symbol', 'name', 'new_industry_code', 'new_industry'])


def get_industry_final_fix_df():
    return pd.DataFrame([
        # 汽车
        ['汽车零部件', '汽车零部件'],
        ['汽车服务', '汽车服务'],
        ['乘用车', '汽车整车'],  # = merge 汽车整车
        ['商用车', '汽车整车'],

        # 医药生物
        ['化学制药', '化学制药'],
        ['生物制品', '生物制品'],
        ['中药Ⅱ', '中药'],
        ['医疗器械', '医疗器械'],
        ['医疗服务', '医疗服务'],
        ['医药商业', '医药商业'],

        # 电力设备
        ['电网设备', '电网设备'],
        ['电池', '电池'],
        ['电机Ⅱ', '电机'],  #
        ['光伏设备', '光伏设备'],
        ['风电设备', '风电设备'],
        ['其他电源设备Ⅱ', '其他电源设备'],

        # 房地产
        ['房地产开发', '房地产'],
        ['房地产服务', '房地产'],

        # 计算机 联动板块
        ['计算机设备', '计算机设备'],
        ['IT服务Ⅱ', 'IT服务'],
        ['软件开发', '软件开发'],

        # 环保
        ['环境治理', '环保'],  # merge, 环保
        ['环保设备Ⅱ', '环保'],  # merge '环保'

        # 电子
        ['半导体', '半导体'],
        ['电子化学品Ⅱ', '电子化学品'],
        ['光学光电子', '光学光电子'],
        ['消费电子', '消费电子'],
        ['元件', '元件'],
        ['其他电子Ⅱ', '其他电子'],  #

        # 国防
        ['军工电子Ⅱ', '军工电子'],  # todo merge 国防
        ['地面兵装Ⅱ', '地面兵装'],  # todo merge 国防
        ['航天装备Ⅱ', '航天装备'],
        ['航空装备Ⅱ', '航空装备'],  # todo merge 国防
        ['航海装备Ⅱ', '航海装备'],

        # 金融 互联网金融 参股券商
        ['证券Ⅱ', '证券'],
        ['国有大型银行Ⅱ', '银行'],  # merge  to 银行
        ['城商行Ⅱ', '银行'],  #
        ['农商行Ⅱ', '银行'],  # merge   银行
        ['股份制银行Ⅱ', '银行'],  # merge  to 银行
        ['保险Ⅱ', '保险'],
        ['多元金融', '多元金融'],

        # 通信
        ['通信服务', '通信服务'],
        ['通信设备', '通信设备'],

        # 酒 喝死你
        ['白酒Ⅱ', '酒类'],  # merge '酒类'
        ['非白酒', '酒类'],  # merge '酒类'

        # 轻工制造
        ['造纸', '造纸'],
        ['包装印刷', '包装印刷'],  #
        ['文娱用品', '文娱用品'],  #
        ['家居用品', '家居用品'],

        # 纺织服装
        ['服装家纺', '纺织服装'],  # merge 纺织服装
        ['纺织制造', '纺织服装'],  # merge 纺织服装
        ['饰品', '饰品'],  # todo exclude

        # 美容护理
        ['化妆品', '美容护理'],  # merge  to 美容护理
        ['医疗美容', '美容护理'],  # merge  美容护理
        ['个护用品', '个护用品'],

        # 食品饮料
        ['饮料乳品', '饮料乳品'],  # merge 食品饮料
        ['食品加工', '食品加工'],  # merge 食品饮料
        ['调味发酵品Ⅱ', '调味发酵品'],  # merge  to  食品饮料
        ['休闲食品', '休闲食品'],  # merge '食品饮料'

        # 石油石化
        ['炼化及贸易', '石油行业'],  # merge 石油行业
        ['油服工程', '采掘行业'],  # merge '采掘行业'
        ['油气开采Ⅱ', '石油行业'],  # merge  to 石油行业

        #  钢铁
        ['普钢', '钢铁'],  # merge 钢铁
        ['特钢Ⅱ', '钢铁'],  # merge '钢铁'
        ['冶钢原料', '钢铁'],  # merge to 钢铁

        # 有色金属
        ['能源金属', '能源金属'],  # merge
        ['小金属', '小金属'],
        ['贵金属', '贵金属'],  #
        ['金属新材料', '金属新材料'],
        # 铅锌  铝  铜
        ['工业金属', '工业金属'],

        # 建筑装饰
        ['基础建设', '工程建设'],
        ['房屋建设Ⅱ', '工程建设'],  # merge 工程建设
        ['工程咨询服务Ⅱ', '工程咨询服务'],
        ['专业工程', '建筑工程'],
        ['装修装饰Ⅱ', '装修装饰'],
        ['工程机械', '工程机械'],

        # 建筑材料
        ['装修建材', '装修建材'],  #
        ['建筑建材', '装修建材'],  #
        ['玻璃玻纤', '玻璃玻纤'],
        ['水泥', '水泥'],

        # 家用电器
        ['白色家电', '家用电器'],  # merge 家用电器
        ['照明设备Ⅱ', '家用电器'],  # merge 家用电器
        ['其他家电Ⅱ', '家用电器'],  # merge  家用电器
        ['家电零部件Ⅱ', '家用电器'],  # merge 家用电器
        ['小家电', '家用电器'],  # merge '家用电器'
        ['黑色家电', '家用电器'],  # merge 家用电器
        ['厨卫电器', '家用电器'],  # merge   家用电器

        # 基础化工
        ['化学制品', '化学制品'],
        ['化学原料', '化学原料'],
        ['化学纤维', '化学纤维'],
        ['农化制品', '化肥农药'],
        ['塑料', '塑料'],
        ['橡胶', '橡胶'],  # todo   exclude
        ['非金属材料Ⅱ', '非金属材料'],

        # 商贸零售
        ['一般零售', '一般零售'],
        ['互联网电商', '互联网电商'],
        ['贸易Ⅱ', '贸易'],  #

        # 农林牧渔
        ['养殖业', '养殖业'],  # merge 农林牧渔
        ['农产品加工', '农产品加工'],  # merge 农林牧渔
        ['饲料', '饲料'],  # merge  to 农林牧渔
        ['渔业', '渔业'],  # merge  to 农林牧渔
        # merge 农林牧渔
        ['动物保健Ⅱ', '动物保健'],
        ['种植业', '种植业'],
        ['林业Ⅱ', '林业'],  # merge  农林牧渔
        ['农业综合Ⅱ', '农业综合'],  # merge  农林牧渔

        # 公用事业
        ['燃气Ⅱ', '燃气'],
        ['电力', '电力'],

        # 传媒
        ['数字媒体', '数字媒体'],
        ['电视广播Ⅱ', '电视广播'],
        ['游戏Ⅱ', '游戏'],
        ['出版', '出版'],
        ['影视院线', '影视院线'],
        ['广告营销', '广告营销'],

        # 交通运输
        ['物流', '物流'],
        ['铁路公路', '铁路公路'],
        ['航运港口', '航运港口'],
        ['航空机场', '航空机场'],

        # 旅游酒店
        ['酒店餐饮', '旅游酒店'],  # merge  to 旅游酒店
        ['旅游零售Ⅱ', '旅游酒店'],  # merge   旅游酒店 中国中免
        ['旅游及景区', '旅游酒店'],  # merge 旅游酒店

        # 煤炭
        ['焦炭Ⅱ', '煤炭'],  # merge  to 煤炭
        ['煤炭开采', '煤炭'],  # merge 煤炭

        ['教育', '教育'],

        ['自动化设备', '自动化设备'],
        ['轨交设备Ⅱ', '轨交设备'],

        # 机械设备  仪器仪表 农用机械 制冷空调设备  印刷包装机械 机床工具
        # 楼宇设备 磨具磨料  纺织服装设备  能源及重型设备 金属制品
        ['专用设备', '专用设备'],  # todo exclude
        ['通用设备', '通用设备'],  # todo exclude
        ['专业服务', '专业服务'],  # todo exclude 无法具体分类
        ['摩托车及其他', '摩托车及其他'],  # todo exclude

        ['专业连锁Ⅱ', '专业连锁'],  # 专业连锁 综合Ⅱ

        ['体育Ⅱ', '综合'],  # merge  综合Ⅱ
        ['综合Ⅱ', '综合']  # todo exclude

    ], columns=['second_sw_industry', 'industry'])


# 第三行业作为筛选行业
def fix_industry_use_sw_third(company_info_df):
    # 细分工业金属行业
    company_info = company_info_df.copy()
    company_info.loc[company_info.third_industry_code == '240303', 'industry'] = '铅锌'
    company_info.loc[company_info.third_industry_code == '240301', 'industry'] = '铝'
    company_info.loc[company_info.third_industry_code == '240302', 'industry'] = '铜'
    # 细分专业设备
    company_info.loc[company_info.third_industry_code == '640203', 'industry'] = '能源及重型设备'
    company_info.loc[company_info.third_industry_code == '640204', 'industry'] = '楼宇设备'
    company_info.loc[company_info.third_industry_code == '640206', 'industry'] = '纺织服装设备'
    company_info.loc[company_info.third_industry_code == '640207', 'industry'] = '农用机械'
    company_info.loc[company_info.third_industry_code == '640208', 'industry'] = '印刷包装机械'
    # todo 细分
    company_info.loc[company_info.third_industry_code == '640209', 'industry'] = '专用设备'
    company_info.loc[company_info.third_industry_code == '630402', 'industry'] = '专用设备'
    company_info.loc[company_info.third_industry_code == '220702', 'industry'] = '非金属材料'
    # 细分通用设备
    company_info.loc[company_info.third_industry_code == '640101', 'industry'] = '机床工具'
    company_info.loc[company_info.third_industry_code == '640103', 'industry'] = '磨具磨料'
    company_info.loc[company_info.third_industry_code == '640105', 'industry'] = '制冷空调设备'
    company_info.loc[company_info.third_industry_code == '640106', 'industry'] = '通用设备'
    company_info.loc[company_info.third_industry_code == '640107', 'industry'] = '仪器仪表'
    company_info.loc[company_info.third_industry_code == '640301', 'industry'] = '仪器仪表'
    # todo 细分
    company_info.loc[company_info.third_industry_code == '640108', 'industry'] = '金属制品'
    return company_info


def find_sw_third_industry(industry_id):
    sw_third_industry = mongodb_util.find_query_data('sw_industry', query={"_id": industry_id})
    first_sw_industry_name = list(sw_third_industry['first_sw_industry'])[0]
    second_sw_industry_name = list(sw_third_industry['second_sw_industry'])[0]

    first_sw_industry = mongodb_util.find_query_data('sw_industry', query={'first_sw_industry': first_sw_industry_name,
                                                                           "second_sw_industry": 0,
                                                                           "third_sw_industry": 0
                                                                           })

    second_sw_industry = mongodb_util.find_query_data('sw_industry',
                                                      query={'second_sw_industry': second_sw_industry_name,
                                                             "third_sw_industry": 0
                                                             })

    sw_third_industry['first_industry_code'] = first_sw_industry['_id']
    sw_third_industry['second_industry_code'] = second_sw_industry['_id']
    return sw_third_industry


def fix_industry_data(industry_id, company_info):
    sw_industry = find_sw_third_industry(industry_id)
    company_info['first_sw_industry'] = sw_industry.first_sw_industry
    company_info['first_industry_code'] = sw_industry.industry_code
    company_info['second_sw_industry'] = sw_industry.second_sw_industry
    company_info['second_industry_code'] = sw_industry.second_industry_code
    company_info['third_sw_industry'] = sw_industry.third_sw_industry
    company_info['third_industry_code'] = sw_industry.industry_code
    return company_info


def fix_symbol_industry(company_info, symbol):
    fix_symbol_df = get_fix_symbol_industry()
    fix_symbol_df_one = fix_symbol_df.loc[fix_symbol_df['symbol'] == symbol]
    if data_frame_util.is_not_empty(fix_symbol_df_one):
        new_industry_code = list(fix_symbol_df_one['new_industry_code'])[0]
        company_info = fix_industry_data(new_industry_code, company_info)

    return company_info


def fix_one_symbol():
    symbol = '300483'
    company_info = mongodb_util.find_query_data('company_info', query={'_id': symbol})
    company_info = fix_symbol_industry(company_info, symbol)
    company_info['industry'] = company_info['second_sw_industry']
    mongodb_util.save_mongo(company_info, 'company_info')


def filed_sort(company_info):
    return company_info[[
        "_id",
        "name",
        "industry",
        "first_sw_industry",
        "first_industry_code",
        "second_sw_industry",
        "second_industry_code",
        "third_sw_industry",
        "third_industry_code",
        "ths_concept_name",
        "ths_concept_code",
        "ths_concept_sync_day",
        "em_industry",
        "em_concept",
        "business_nature",
        "actual_controller_name",
        "actual_controller_rate",
        "final_controller_name",
        "final_controller_rate",
        "mv_circulation_ratio",
        "flow_mv_sp",
        "total_mv_sp",
        "now_price",
        "total_share",
        "flow_share",
        "total_mv",
        "flow_mv",
        "flow_mv_level",
        "holder_controller_name",
        "holder_controller_rate",
        "area",
        "list_date",
        "deal_days",
        "pe_ttm",
        "pb",
        "ROE",
        "classification",
        "base_business",
        "address",
        "market_id",
        "symbol",
        "amount",
        "sync_date",
        "ths_concept_list_info",
        'ths_concept_name_list_str',
        'ths_concept_count',
        "kpl_plate_name",
        "kpl_most_relative_name",
        "kpl_plate_list_info",
        'operate_profit',
        'total_operate_income',
        'kzz_debt_list',
        'hk_stock_code',
        'hk_stock_name',
        'main_business_list',
        'most_profitable_business',
        'most_profitable_business_rate',
        'most_profitable_business_profit',
    ]]


if __name__ == '__main__':
    fix_one_symbol()
    industry_df = get_industry_final_fix_df()
    print(industry_df)

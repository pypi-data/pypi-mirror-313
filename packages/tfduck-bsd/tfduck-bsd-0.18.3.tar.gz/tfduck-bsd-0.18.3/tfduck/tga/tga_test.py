# -*- coding: utf-8 -*-
"""
本文件夹内执行测试
"""
from train_sql_ltv import TrainFeatureSql
# from predict_sql_ltv import TrainFeatureSql  # 预测的用法和以前一样

def test():
    class GConf(object):
        def __init__(self):
            self.part_date_start = "2023-01-15"
            self.part_date_end = "2023-01-17"
            # 注册后0-14天的所有ltv作为标签
            self.label_durs = [int(86400*0), int(86400*14)]
            self.level_durs = [86400*0.25, 86400*0.5,
                               86400, 86400*2, 86400*3]  # 由小到大排列
            self.tga_user_table = "v_user_30"
            self.tga_event_table = "v_event_30"

    gconf = GConf()

    need_events = (
        'new_device',
        'new_session',
        'g_push',
        'sdk_close_session'
    )
    need_event_attrs = (
        "#lib",
        "pn",
        "#device_model",
        "#screen_width",
        "#screen_height",
        "#country_code",
        "$part_event",
        "#user_id"
    )
    feature_names = {
        'b': '打开游戏次数',
        'c': '本地推送打开游戏次数'
    }
    addon_attrs = [
        "#device_model",
        "#screen_width",
        "#screen_height"
    ]
    sub_sql_fs = {
        'b':
        # 打开游戏次数
        """
                                --%(real_des)s
                                sum(
                                    if(
                                    "$part_event"='new_session' and rt_dur<%(level_dur)s,
                                    1, 
                                    0)
                                ) as %(sub_field_name)s
                                """, 'c':
        # 本地推送打开游戏次数
        """
                                --%(real_des)s
                                sum(
                                    if(
                                    "$part_event"='g_push' and  rt_dur<%(level_dur)s,
                                    1,
                                    0)
                                ) as %(sub_field_name)s
                                """
    }
    user_cols2 = """ "#lib"='Android' """
    tf_sql_obj = TrainFeatureSql(
        ctx={},
        gconf=gconf,
        need_events=need_events,
        need_event_attrs=need_event_attrs,
        feature_names=feature_names,
        sub_sql_fs=sub_sql_fs,
        user_cols2=user_cols2,
        addon_attrs=addon_attrs,  # 可选参数
        line_value_rd=0.5,  # 可选参数
        mode="iaa+iap"
    )
    sql = tf_sql_obj.get_sql()  # 这个sql就是拉取特征值的sql
    # 将sql复制到剪贴板
    import pyperclip
    pyperclip.copy(sql)
    return sql


if __name__ == "__main__":
    test()

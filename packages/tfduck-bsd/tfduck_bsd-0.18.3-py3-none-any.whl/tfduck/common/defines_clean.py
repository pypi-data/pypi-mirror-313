# coding=utf-8
"""
脱离tfduck系统环境的一些公共方法
"""
from tfduck.common.extendEncoder import DatetimeJSONEncoder
from tfduck.common.defines import Et, CeleryRetryError
import ast
import hashlib
import json
import logging
import sys
import shutil
import time
import traceback
import random
import requests
import os
import uuid
import arrow



class BaseMethod(object):
    """
    @des:一些基础方法
    """

    def __init__(self):
        """
        @des:保持一些全局变量
        """
        self.dj44_base_dir = "/opt/djcelery44/djcelery44"
        self.http_api = Dj44HttpApi() # 后面使用需要BMOBJ.http_api.set_user_token('xxxxx')设置token
    
    def get_unique_id(self):
        unique_id = (uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()) + str(random.random()))).hex
        return unique_id
    
    def get_unique_id2(self):
        unique_id = (uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()) + str(random.random()))).hex
        return unique_id

    def remove_file(self, file_path):
        """
        @des: 删除文件
        """
        try:
            os.remove(file_path)
        except:
            pass

    def remove_folder(self, folder_path):
        """
        @des: 删除文件夹
        """
        try:
            shutil.rmtree(folder_path)
        except:
            pass

    def get_file_path(self, path):
        """
        @des: 文件的真实路径
        """
        return os.path.join(self.dj44_base_dir, os.path.join("dags/sptasks/p_code", path))
        
            

    def gen_local_unique_file(self, pre_path="", pre_name="", ext="csv"):
        """
        @des:生成本地文件唯一路径
        """
        # media_root = settings.MEDIA_ROOT
        media_root = "/mydata/media"
        base_dir = os.path.join(media_root, "docs", pre_path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        real_name = "%s%s_%s.%s" % (pre_name, uuid.uuid1(
        ).hex, arrow.now().format("YYYYMMDD_HHmmSS"), ext)
        file_path = os.path.join(base_dir, real_name)
        return file_path

    def gen_local_unique_path(self, pre_path="", pre_name="", is_create=False):
        """
        @des:生成本地目录唯一路径
        """
        # media_root = settings.MEDIA_ROOT
        media_root = "/mydata/media"
        base_dir = os.path.join(media_root, "docs", pre_path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        real_name = "%s%s_%s" % (pre_name, uuid.uuid1(
        ).hex, arrow.now().format("YYYYMMDD_HHmmSS"))
        folder_path = os.path.join(base_dir, real_name)
        if is_create:
            os.makedirs(folder_path)
        return folder_path

    def get_var(self, name):
        """
        @des: 获取变量
        """
        data = self.http_api.get_model_data("gconfig", "VarConfig", {"name": name}, ["content"])
        result = json.loads(data[0]['content'])
        return result

    def clog(self, ctx, *log_values):
        """
        @des: 向数据库中记录日志
        """
        try:
            pd_logs = [str(item) for item in log_values]
            pd_logs = "".join(pd_logs)
            if len(pd_logs) > 1024*1024*50:  # 大于5M
                log_values = ["log data too long"]
        except:
            pass
        
        task_type = ctx['task_type']
        trid = ctx['trid']
        index = ctx['index']
        #
        real_values = []
        for log_value in log_values:
            try:
                value = str(log_value)
                real_values.append(value)
            except:
                value = "log value must be string"
                real_values.append(value)

        app_name = None
        if task_type == "dtask":
            # Record = apps.get_model("dtask", 'RunRecord')
            app_name = "dtask"
            model_name = "RunRecord"
        elif task_type == "retask":
            # Record = apps.get_model("retask", 'RETaskRecord')
            app_name = "retask"
            model_name = "RETaskRecord"
        elif task_type == "sptask":
            # Record = apps.get_model("sptask", 'DPTaskRecord')
            app_name = "sptask"
            model_name = "DPTaskRecord"
        if app_name is not None:
            try:
                self.http_api.run_model_method(app_name, model_name, "add_records", {
                    "lock_id": trid, "task_index": index, "recs": real_values})
                # Record.objects.add_records(
                #     lock_id=trid, task_index=index, recs=real_values)
            except Exception as e:
                self.log_error("clog error ----- :")
                self.logerr(e)
        # 防止过度写入日志
        time.sleep(0.2)

    def get_record_now(self, ctx={}, tz="UTC"):
        """
        @des: 获取执行任务记录的创建时间，方便dag里面取根据现在时间去执行part_date-----其实这个方法用不到，因为都是在dag里面用,dag用的是defines.BMOBJ，因为这个dag是必须带默认环境的
        start = arrow.now(tz="Asia/Shanghai")
        @ return: datetime 带时区
        """
        # 如果是查看任务，而不是任务记录，是不会有这两个参数的
        task_type = ctx.get('task_type', None)
        trid = ctx.get('trid', None)
        if trid is None:
            root_create_time = arrow.now(tz=tz)
        else:
            # Record = None
            if task_type == "dtask":
                # Record = apps.get_model("dtask", 'RunRecord')
                app_name = "dtask"
                model_name = "RunRecord"
            elif task_type == "retask":
                # Record = apps.get_model("retask", 'RETaskRecord')
                app_name = "retask"
                model_name = "RETaskRecord"
            elif task_type == "sptask":
                # Record = apps.get_model("sptask", 'DPTaskRecord')
                app_name = "sptask"
                model_name = "DPTaskRecord"
            if app_name is not None:
                # obj = Record.objects.get(id=trid)
                objs = self.http_api.get_model_data(app_name, model_name, {"id": trid}, ["extra", "create_time"])
                #
                obj = objs[0]
                obj['extras'] = json.loads(obj['extra'])
                #
                root_create_time = obj['extras'].get("root_create_time", None)
                if root_create_time is None:  # 如果拿不到，那么obj肯定是根节点
                    root_create_time = arrow.get(obj['create_time']).to(tz)
                else:  # 读取extra的信息，即根节点
                    # root_create_time带有时区信息，可以直接get
                    root_create_time = arrow.get(root_create_time).to(tz)
        # 返回
        return root_create_time.datetime

    def jsonloads(self, data):
        """
        @des: 自动jsonload
        """
        try:
            data = json.loads(data)
        except Exception as e:
            try:
                data = ast.literal_eval(data)
            except Exception as e:
                raise Et(2, u"参数格式不正确")
        return data

    def jsondumps(self, data, mode=1, sort_keys=False):
        """
        @des:返回值dumps
        """
        #data = json.dumps(data, ensure_ascii=False, cls=DatetimeJSONEncoder)
        data = json.dumps(data, separators=(',', ':'), cls=DatetimeJSONEncoder)
        return data

    def text_tran_html(self, text):
        """
        @des:将文本转换为html,比如help_text
        """
        text = text.replace("\n", "<br/>")
        text = text.replace(" ", "&nbsp")
        return text


    def geterr(self, e):
        result = []
        errorMeg = ''
        try:
            for file, lineno, function, text in traceback.extract_tb(sys.exc_info()[2]):
                errorMeg += '%s\n%s, in %s\n%s:                %s!' % (
                    str(e), file, function, lineno, text)
            result.append("error"+"*"*50)
            for error in errorMeg.split("\n"):
                result.append(error)
                result.append('error')
            try:
                result.append(getattr(e, '_msg', 'exception'))
            except Exception as e1:
                result.append(getattr(e, 'msg', 'exception'))
        except Exception as e2:
            result.append(str(e2))
        return "\n".join(result)

    def logerr(self, e):
        errorMeg = ''
        try:
            for file, lineno, function, text in traceback.extract_tb(sys.exc_info()[2]):
                errorMeg += '%s\n%s, in %s\n%s:                %s!' % (
                    str(e), file, function, lineno, text)
            self.log_error("error"+"*"*50)
            for error in errorMeg.split("\n"):
                self.log_error(error, "error")
            try:
                error_self = "".join(traceback.format_exception_only(type(e), e))  # 捕获错误本身,这样才能捕获到compile里面的错误
                self.log_error(error_self, "error")
            except:
                pass
            try:
                self.log_error(getattr(e, '_msg', 'exception'))
            except Exception as e1:
                self.log_error(getattr(e, 'msg', 'exception'))
        except Exception as e2:
            self.log_error(e2)

    def get_log_str(self, *msgs):
        try:
            msg_str = " ".join([str(msg) for msg in msgs])
        except Exception as _:
            msg_str = msgs
        return msg_str

    def log_debug(self, *msgs):
        msg_str = self.get_log_str(*msgs)
        print(msg_str)

    def log_info(self, *msgs):
        msg_str = self.get_log_str(*msgs)
        print(msg_str)

    def log_error(self, *msgs):
        msg_str = self.get_log_str(*msgs)
        print(msg_str)

    def log_warning(self, *msgs):
        msg_str = self.get_log_str(*msgs)
        print(msg_str)
    # end--日志记录


class Dj44HttpApi(object):
    """
    @des: 外部api
    """
    def __init__(self):
        self.r_timeout = (5, 10)
        self.retry_count = 1
        self.retry_delay = 5
        self.user_token = ''
    
    def get_user_token(self):
        if self.user_token == '':
            raise Et(2, "请先设置user_token")
        return self.user_token
    
    def set_user_token(self, user_token):
        self.user_token = user_token


    def get_host_name(self):
        # 后面可以改成从配置中心获取
        PROJECT_ENV = os.environ.get("PROJECT_ENV", "dev")
        if PROJECT_ENV == "dev": # 本地测试
            endpoint_url = "http://localhost:8000"
        else:
            endpoint_url = "http://tfduck.163py.com"   # 后面可以改成从配置中心获取
        return {'s': 1, 'v': endpoint_url}  
    
    # 旧的接口也从tfduck的外部接口调用

    def get_model_data(self, app_name, model_name, query_str, r_field):
        """
        @des: 获取模型数据
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        data = {
                "tfduck_api_token": self.get_user_token(),
                "app_name": app_name,
                "model_name": model_name,
                "query_str": query_str,
                "r_field": r_field,
        }
        #
        url = os.path.join(host_name, 'get_model_data')
        for i in range(self.retry_count):
            try:
                res = requests.post(url, json=data, timeout=self.r_timeout)
                break
            except:
                time.sleep(self.retry_delay)
                continue
        else:  # 循环完成
            raise Et(
                2, f"bmobj clean set_model_data retry {self.retry_count} times failed!")
        #
        res = res.json()
        if res['s'] == 1:
            result = res['data']
            return result
        else:
            raise Et(2, res['msg'])
        
    
    def set_model_data(self, app_name, model_name, query_str, r_field, save_data):
        """
        @des: 给模型更新数据
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        data = {
                "tfduck_api_token": self.get_user_token(),
                "app_name": app_name,
                "model_name": model_name,
                "query_str": query_str,
                "r_field": r_field,
                "save_data": save_data
        }
        #
        url = os.path.join(host_name, 'set_model_data')
        for i in range(self.retry_count):
            try:
                res = requests.post(url, json=data, timeout=self.r_timeout)
                break
            except:
                time.sleep(self.retry_delay)
                continue
        else:  # 循环完成
            raise Et(
                2, f"bmobj clean set_model_data retry {self.retry_count} times failed!")
        #
        res = res.json()
        if res['s'] == 1:
            result = res['data']
            return result
        else:
            raise Et(2, res['msg'])

    
    def run_model_method(self, app_name, model_name, run_method, run_params):
        """
        @des: 运行模型自定义方法
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        data = {
            "tfduck_api_token": self.get_user_token(),
            "app_name": app_name,
            "model_name": model_name,
            "run_method": run_method,
            "run_params": run_params
        }
        #
        url = os.path.join(host_name, 'run_model_method')
        for i in range(self.retry_count):
            try:
                res = requests.post(url, json=data, timeout=self.r_timeout)
                break
            except:
                time.sleep(self.retry_delay)
                continue
        else:  # 循环完成
            raise Et(
                2, f"bmobj clean retry {self.retry_count} times failed!")
        #
        res = res.json()
        if res['s'] == 1:
            result = res['data']
            return result
        else:
            raise Et(2, res['msg'])



    # start----tfduck的外部接口调用
    def run_sptasks_by_taskname(self, task_names):
        """
        @des: http外部接口运行非定时的任务
        一般用于多个工程的上游依赖，A->B
        当A工程执行完毕后, 执行B工程的所有任务
        @param user_token[必填]: tfduck的用户token; self.set_user_token('xxxxx')
               task_names[必填]: 运行的sptask任务(不是任务工程，也不是任务记录)的全名的列表, 比如 ["同步任务_3",...]
        @return: 
               成功---{"s":1,  'value':[任务名称]}
               失败---{"s: 非1, 'msg':'失败原因'}
        @example:
        ######
        from tfduck.common.defines import BMOBJ
        BMOBJ.http_api.run_sptasks_by_taskname('xxxxx', ['helloworld_end_tf_2_0'])
        ######
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        #
        url = os.path.join(host_name, 'run_sptasks_by_taskname')
        data = {
            'user_token': self.get_user_token(),
            'task_names': json.dumps(task_names),
        }
        res = requests.post(url, data=data, timeout=(5, 30))
        result = res.json()
        return result

    def run_sptasks_by_projectname(self, project_names):
        """
        @des: http外部接口运行非定时的任务
        一般用于多个工程的上游依赖，A->B
        当A工程执行完毕后, 执行B工程的所有任务
        @param user_token   [必填]: tfduck的用户token; self.set_user_token('xxxxx')
               project_names[必填]: 运行的sptask任务工程的名称(不是任务，也不是任务记录)的全名的列表, 比如 ["同步任务工程名",...]
        @return: 
               成功---{"s":1,  'value':[任务名称]}
               失败---{"s: 非1, 'msg':'失败原因'}
        @example:
        ######
        from tfduck.common.defines import BMOBJ
        BMOBJ.http_api.run_sptasks_by_projectname('xxxxx', ['helloworld_end_tf_2_0'])
        ######
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        #
        url = os.path.join(host_name, 'run_sptasks_by_projectname')
        data = {
            'user_token': self.get_user_token(),
            'project_names': json.dumps(project_names)
        }
        res = requests.post(url, data=data, timeout=(5, 30))
        result = res.json()
        return result

    def get_sptasks_info_by_taskname(self, task_names, start_time, end_time):
        """
        @des: http外部接口查询任务的信息，根据任务名称查询
        一般用于多个工程的上游依赖，A->B
        当A工程执行完毕后, 执行B工程的所有任务
        @param user_token[必填]: tfduck的用户token;self.set_user_token('xxxxx')
               task_names[必填]: 运行的sptask任务(不是任务工程，也不是任务记录)的全名的列表, 比如 ["同步任务_3",...]
               start_time[选填]: 任务的create_time的查询时间范围的开始时间，格式YYYY-MM-DD HH:mm:ss 例如 2022-02-15 14:23:44
               end_time  [选填]: 任务的create_time的查询时间范围的结束时间，格式YYYY-MM-DD HH:mm:ss 例如 2022-02-15 18:23:44
        @return: 
               成功---{"s":1,  'value':[{'task__name': '任务名称', 'task__id': 109, 'id': 78, 'state': 3, 'revoke_state': 1},...]}
               失败---{"s: 非1, 'msg':'失败原因'}
        @example:
        ######
        from tfduck.common.defines import BMOBJ
        BMOBJ.http_api.get_sptasks_info_by_taskname('xxxxx', ['helloworld_end_tf_2_0'], '2022-02-15 14:23:44', '2022-02-15 18:23:44')
        ######
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        #
        url = os.path.join(host_name, 'get_sptasks_info_by_taskname')
        data = {
            'user_token': self.get_user_token(),
            'task_names': json.dumps(task_names),
            'start_time': start_time,
            'end_time': end_time,
        }
        res = requests.post(url, data=data, timeout=(5, 30))
        result = res.json()
        return result

    def get_sptasks_info_by_projectname(self, project_names, start_time, end_time):
        """
        @des: http外部接口查询任务的信息，根据任务工程名称查询
        一般用于多个工程的上游依赖，A->B
        当A工程执行完毕后, 执行B工程的所有任务
        @param user_token[必填]: tfduck的用户token;self.set_user_token('xxxxx')
               project_names[必填]: 运行的sptask任务(不是任务工程，也不是任务记录)的全名的列表, 比如 ["同步任务_3",...]
               start_time[选填]: 任务的create_time的查询时间范围的开始时间，格式YYYY-MM-DD HH:mm:ss 例如 2022-02-15 14:23:44
               end_time  [选填]: 任务的create_time的查询时间范围的结束时间，格式YYYY-MM-DD HH:mm:ss 例如 2022-02-15 18:23:44
        @return: 
               成功---{"s":1,  'value':[{'task__name': '任务名称', 'task__id': 109, 'id': 78, 'state': 3, 'revoke_state': 1},...]}
               失败---{"s: 非1, 'msg':'失败原因'}
        @example:
        ######
        from tfduck.common.defines import BMOBJ
        BMOBJ.http_api.get_sptasks_info_by_projectname('xxxxx', ['helloworld_end_tf_2_0'], '2022-02-15 14:23:44', '2022-02-15 18:23:44')
        ######
        """
        hresult = self.get_host_name()
        if hresult['s'] == 1:
            host_name = hresult['v']
        else:
            return hresult
        #
        url = os.path.join(host_name, 'get_sptasks_info_by_projectname')
        data = {
            'user_token': self.get_user_token(),
            'project_names': json.dumps(project_names),
            'start_time': start_time,
            'end_time': end_time,
        }
        res = requests.post(url, data=data, timeout=(5, 30))
        result = res.json()
        return result

    # end----tfduck的外部接口调用


BMOBJ = BaseMethod()

#!encoding:utf-8
import json
import logging
import subprocess
import traceback

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class AssessmentPage(View):
    """考核-页面"""

    def get(self, request, *args, **kwargs):
        subprocess.check_output("ssh root@docker sh /usr/local/share/xiaodu/script/start_docker.sh")
        template_name = "assess/info/index.html"
        return render(request, template_name, {})


class AssessmentResult(View):
    """考核-结果"""

    def post(self, request, *args, **kwargs):
        result_dict = {"err": 0, "msg": "success", "data": ""}
        try:
            result_info = subprocess.check_output("ssh root@docker sh /usr/local/share/xiaodu/script/demo_kaohe.sh")
            result_dict["data"] = json.loads(result_info)
        except:
            traceback.print_exc()
            logging.getLogger().error(traceback.format_exc())
            result_dict["err"] = 1
            result_dict["msg"] = traceback.format_exc()
        finally:
            return HttpResponse(json.dumps(result_dict, ensure_ascii=False))

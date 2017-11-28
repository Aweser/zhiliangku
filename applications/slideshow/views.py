#!encoding:utf-8
import json
import logging
import traceback

from django.http import HttpResponse
from django.views.generic import View

from applications.slideshow.models import Carousel


class SlideList(View):
    def post(self, request, *args, **kwargs):
        result_dict = {"err": 0, "message": "success", "data": []}
        try:
            carousel_objs = Carousel.objects.all().values()
            result_dict["data"] = list(carousel_objs)
        except:
            traceback.print_exc()
            logging.getLogger().error(traceback.format_exc())
            result_dict["err"] = 1
            result_dict["message"] = traceback.format_exc()
        finally:
            return HttpResponse(json.dumps(result_dict, ensure_ascii=False))

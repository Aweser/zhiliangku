#!encoding:utf-8
import json
import logging
import traceback

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

from applications.record.models import WatchRecord
from applications.tracks_learning.models import *
from lib.permissionMixin import class_view_decorator, user_login_required
from lib.util import str_to_int


class VideoList(View):
    """视频列表"""

    def get(self, request, *args, **kwargs):
        result_dict = {"err": 0, "msg": "success", "data": list()}
        try:
            # 获取查询参数
            section_id = str_to_int(request.GET.get('section_id', 0))
            custom_user_id = str_to_int(request.GET.get('custom_user_id', 0))  # 用户ID

            data_list = list()
            if section_id:
                videos = Video.objects.filter(section__id=section_id).order_by("sequence")
                for one_video in videos:
                    video_dict = dict()
                    video_dict["id"] = one_video.id
                    video_dict["type"] = one_video.type
                    video_dict["type_name"] = one_video.get_type_display()
                    video_dict["name"] = one_video.name
                    video_dict["sequence"] = one_video.sequence
                    video_dict["desc"] = one_video.desc
                    video_dict["is_learned"] = 0
                    video_dict["vid"] = one_video.vid if one_video.vid else ""
                    duration_str = ""
                    if one_video.duration:
                        m, s = divmod(one_video.duration, 60)
                        h, m = divmod(m, 60)
                        duration_str = "%02d:%02d:%02d" % (h, m, s)

                    video_dict["duration"] = duration_str

                    # 补全直播信息
                    if one_video.type == "3" and one_video.live:
                        video_dict["live_id"] = one_video.live.id
                        video_dict["live_channelId"] = one_video.live.channelId
                        video_dict["vid"] = one_video.live.channelId
                        video_dict["live_status"] = one_video.live.status
                        video_dict["live_status_name"] = one_video.live.get_status_display()
                        if one_video.live_start_time and one_video.live_end_time:
                            if (one_video.live_start_time > timezone.now()) or (
                                    one_video.live_end_time < timezone.now()):
                                video_dict["live_status"] = "end"
                                video_dict["live_status_name"] = "直播结束"
                        else:
                            video_dict["live_status"] = "end"
                            video_dict["live_status_name"] = "直播结束"
                        video_dict["live_start_time"] = one_video.live_start_time.strftime("%Y-%m-%d %H:%M") \
                            if one_video.live_start_time else ""
                        video_dict["live_end_time"] = one_video.live_end_time.strftime("%H:%M") \
                            if one_video.live_end_time else ""

                    # 补全是否学习状态
                    if one_video.type in ["1", "2"]:  # 点播、直播回放
                        watchrecords = WatchRecord.objects.filter(video=one_video, user_id=custom_user_id)
                        if watchrecords.exists():
                            video_dict["is_learned"] = 99
                        if watchrecords.filter(status=1).exists():
                            video_dict["is_learned"] = 1

                    if one_video.type == "4":  # 习题
                        pass

                    data_list.append(video_dict)
            result_dict["data"] = data_list
        except:
            traceback.print_exc()
            logging.getLogger().error(traceback.format_exc())
            result_dict["err"] = 1
            result_dict["msg"] = traceback.format_exc()
        finally:
            return HttpResponse(json.dumps(result_dict, ensure_ascii=False))


@class_view_decorator(user_login_required)
class VideoDetail(View):
    """视频详情页面"""

    def get(self, request, *args, **kwargs):
        template_name = "tracks/video/detail/index.html"
        return render(request, template_name, {})


@class_view_decorator(user_login_required)
class VideoDetailInfo(View):
    """视频详情信息"""

    def get(self, request, *args, **kwargs):
        result_dict = {"err": 0, "msg": "success", "data": {}}
        try:
            # 获取查询参数
            video_id = str_to_int(request.GET.get('video_id', 0))

            video_dict = dict()
            if video_id:
                videos = Video.objects.filter(id=video_id)
                if videos.exists():
                    video_obj = videos.first()
                    video_dict["id"] = video_obj.id
                    video_dict["course_name"] = video_obj.section.course.name
                    video_dict["section_title"] = video_obj.section.title
                    video_dict["section_desc"] = video_obj.section.desc
                    video_dict["type"] = video_obj.type
                    video_dict["type_name"] = video_obj.get_type_display()
                    video_dict["name"] = video_obj.name
                    video_dict["desc"] = video_obj.desc
                    video_dict["duration"] = video_obj.duration
                    video_dict["notes"] = video_obj.notes

                    # 直播信息
                    if video_obj.type == "3":
                        if video_obj.live:
                            video_dict["live_channelId"] = video_obj.live.channelId
                            video_dict["live_id"] = video_obj.live.id
                            video_dict["live_status"] = video_obj.live.status
                            video_dict["live_status_name"] = video_obj.live.get_status_display()
                            video_dict["live_start_time"] = video_obj.live_start_time.strftime("%Y-%m-%d %H:%M") \
                                if video_obj.live_start_time else ""
                            video_dict["live_end_time"] = video_obj.live_end_time.strftime("%H:%M") \
                                if video_obj.live_end_time else ""
                    # 点播信息
                    if video_obj.type in ["1", "2"]:
                        video_dict["vid"] = video_obj.vid
            result_dict["data"] = video_dict
        except:
            traceback.print_exc()
            logging.getLogger().error(traceback.format_exc())
            result_dict["err"] = 1
            result_dict["msg"] = traceback.format_exc()
        finally:
            return HttpResponse(json.dumps(result_dict, ensure_ascii=False))


@class_view_decorator(user_login_required)
class GetNextVideo(View):
    """获取下一节视频信息"""

    def get(self, request, *args, **kwargs):
        result_dict = {"err": 0, "msg": "success", "data": {}}
        try:
            # 获取查询参数
            course_id = str_to_int(request.GET.get('course_id', 0))  # 当前访问课程ID
            video_id = str_to_int(request.GET.get('video_id', 0))  # 当前访问视频ID

            video_objs = Video.objects.filter(section__course__id=course_id)
            if video_objs.exists():
                video = video_objs.filter(id=video_id).first()
                video_list = list(video_objs)
                next_video = None
                try:
                    next_video = video_list[video_list.index(video) + 1]
                except:
                    pass
                if next_video:
                    result_dict["data"]["type"] = next_video.type
                    result_dict["data"]["video_id"] = next_video.id
                    result_dict["data"]["course_id"] = next_video.section.course_id

        except:
            traceback.print_exc()
            logging.getLogger().error(traceback.format_exc())
            result_dict["err"] = 1
            result_dict["msg"] = traceback.format_exc()
        finally:
            return HttpResponse(json.dumps(result_dict, ensure_ascii=False))

#!encoding:utf-8
from __future__ import unicode_literals

import logging
import traceback

from django.db import models
from django.db.models import F
from django.db.models.signals import *
from django.dispatch import receiver
from django.utils import timezone

from applications.custom_user.models import CustomUser
from lib.util import NULL_BLANK_TRUE
from applications.tracks_learning.models import CustomUserClass


class Exam(models.Model):
	"""考试"""

	# 考试性质
	NATURE = (
		("1", '日考核'),
		("2", '阶段考核'),
		("3", '课程考核'),
		("4", '项目考核'),
		("5", '结业考核'),
	)

	# 考试方式
	STYLE = (
		("1", '试卷'),
		("2", '项目答辩'),
		("3", '机试'),
	)

	name = models.CharField("考试名称", max_length=255, **NULL_BLANK_TRUE)
	dates = models.DateField(verbose_name='考试时间', **NULL_BLANK_TRUE)
	customuserclass = models.ForeignKey(CustomUserClass, verbose_name="班级", **NULL_BLANK_TRUE)
	style = models.CharField("考试方式", max_length=1, choices=STYLE, **NULL_BLANK_TRUE)
	nature = models.CharField("考试性质", max_length=1, choices=NATURE, **NULL_BLANK_TRUE)
	number = models.PositiveIntegerField("参加人数", default=0)
	create_time = models.DateField(verbose_name='创建时间', default=timezone.now)

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'Exam'
		verbose_name = "考试"
		verbose_name_plural = "考试"


class ExamNatureCount(models.Model):
	"""指定班级下考试性质考试次数"""
	customuserclass = models.ForeignKey(CustomUserClass, verbose_name="班级", **NULL_BLANK_TRUE)
	nature = models.CharField("考试性质", max_length=255, **NULL_BLANK_TRUE)
	nature_id = models.CharField("考试性质ID", max_length=255, **NULL_BLANK_TRUE)
	count = models.PositiveIntegerField("总数", default=0)

	def __unicode__(self):
		return self.nature

	class Meta:
		db_table = 'ExamNatureCount'
		verbose_name = "考试性质总数"
		verbose_name_plural = "考试性质总数"


class Grade(models.Model):
	"""学生成绩"""
	custom_user = models.ForeignKey(CustomUser, verbose_name="学生", limit_choices_to={'role': 0})
	exam = models.ForeignKey(Exam, verbose_name="考试", related_name="Grades")
	fraction = models.PositiveIntegerField("分数", **NULL_BLANK_TRUE)
	remark = models.CharField("备注", max_length=255, **NULL_BLANK_TRUE)

	def __unicode__(self):
		return self.custom_user.nickname

	class Meta:
		db_table = 'Grade'
		verbose_name = "考试成绩"
		verbose_name_plural = "考试成绩"


@receiver(post_save, sender=Exam)
def exam_nature_add_counter(sender, instance, created, **kwargs):
	"""当有新的考试录入，增加对应考试性质总数 +1
	:param sender:
	:param instance:
	:param created:
	:param kwargs:
	:return:
	"""
	try:
		# 只有当这个instance是新创建的，投注记录+1
		if not created:
			return
		filter_param = {
			"nature_id": instance.nature,
			"customuserclass": instance.customuserclass
		}
		ExamNatureCount.objects.filter(**filter_param).update(count=F('count') + 1)
	except:
		traceback.print_exc()
		logging.getLogger().error(traceback.format_exc())


@receiver(post_delete, sender=Exam)
def exam_nature_del_counter(sender, instance, created, **kwargs):
	"""当删除考试，对应考试性质总数 -1
	:param sender:
	:param instance:
	:param created:
	:param kwargs:
	:return:
	"""
	try:
		# 只有当这个instance是新创建的，投注记录+1

		filter_param = {
			"nature_id": instance.nature,
			"customuserclass": instance.customuserclass
		}

		ExamNatureCount.objects.filter(**filter_param).update(count=F('count') - 1)
	except:
		traceback.print_exc()
		logging.getLogger().error(traceback.format_exc())

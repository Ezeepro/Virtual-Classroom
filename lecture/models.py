from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.

class CoursePack(models.Model):
	user = models.ForeignKey(User, default=1)
	instructor = models.CharField(max_length=250)
	course_title = models.CharField(max_length=500)
	course_code = models.CharField(max_length=100)
	thumbnail = models.FileField()
	is_favorite = models.BooleanField(default=False)

	def __str__(self):
		return self.course_title + ' - ' + self.instructor

class Podcast(models.Model):
	course = models.ForeignKey(CoursePack, on_delete=models.CASCADE)
	material_title = models.CharField(max_length=300)
	material_file = models.FileField(default='')
	is_favorite = models.BooleanField(default=False)

	def __str__(self):
		return self.material_title 


class Video(models.Model):
	course = models.ForeignKey(CoursePack, on_delete=models.CASCADE)
	video_title = models.CharField(max_length=300)
	video_file = models.FileField(default='')
	is_favorite = models.BooleanField(default=False)

	def __str__(self):
		return self.video_title 


class Pdf(models.Model):
	course = models.ForeignKey(CoursePack, on_delete=models.CASCADE)
	pdf_title = models.CharField(max_length=300)
	pdf_file = models.FileField(default='')
	is_favorite = models.BooleanField(default=False)
	
	def __str__(self):
		return self.pdf_title 



class Evaluation(models.Model):
	answer = models.CharField(max_length=500)
		
	def __str__(self):
		return self.score

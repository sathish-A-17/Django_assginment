from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='subtitles')
    start_time = models.FloatField()
    end_time = models.FloatField()
    text = models.TextField()

    def __str__(self):
        return f"{self.video.title} - {self.start_time} to {self.end_time}"






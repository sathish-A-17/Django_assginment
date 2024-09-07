from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import VideoForm
from .models import Video, Subtitle
import subprocess
import re


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})


def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    subtitles = video.subtitles.all()  # Fetch associated subtitles
    timestamp = request.GET.get('t')  # Get timestamp if provided
    return render(request, 'video_detail.html', {'video': video, 'subtitles': subtitles, 'timestamp': timestamp})


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            video_path = video.video_file.path
            subtitle_path = f"{video_path}.srt"
            subprocess.run(['ccextractor', video_path, '-o', subtitle_path])

            with open(subtitle_path, 'r', encoding='utf-8') as f:
                srt_content = f.read()

                # Basic parsing logic for SRT format
            subtitle_entries = re.findall(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n',
                                          srt_content, re.DOTALL)

            for entry in subtitle_entries:
                _, start, end, text = entry
                start_time = convert_to_seconds(start)
                end_time = convert_to_seconds(end)
                Subtitle.objects.create(video=video, start_time=start_time, end_time=end_time, text=text.strip())

            return redirect('video_list')

    else:
        form = VideoForm()
    return render(request, 'upload.html', {'form': form})


def convert_to_seconds(time_str):
    """Convert SRT time format to seconds."""
    hours, minutes, seconds = map(float, re.split('[:.,]', time_str))
    return hours * 3600 + minutes * 60 + seconds


def search(request):
    query = request.GET.get('q')
    if query:
        subtitles = Subtitle.objects.filter(
            Q(text__icontains=query) | Q(video__title__icontains=query)
        )
    else:
        subtitles = []
    return render(request, 'search.html', {'subtitles': subtitles})


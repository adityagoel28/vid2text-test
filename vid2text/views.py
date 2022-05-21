from django.shortcuts import redirect, render
from .models import *
import requests
import time
from django.utils.datastructures import MultiValueDictKeyError
from moviepy.editor import VideoFileClip
# import urllib2  # the lib that handles the url stuff
from urllib.request import urlopen

# Create your views here.

def home(request):
    print('home')
    return render(request, 'index.html')

def video(request):
    context = {}
    request.session['text'] = ''
    return render(request, 'video.html', context)

def transcript(request):
    if (request.session['text'] == ''):
        return redirect(video)
    return render(request, 'video.html')

def upload(request):
    try:
        videoUpload = request.FILES['video']
        file_obj = videoUploader.objects.create(video=videoUpload)
        file_path = str(file_obj.video.url)
        filename = file_path
        videoD = VideoFileClip(filename)
        # print(videoD.duration)  # this will return the length of the video in seconds

        file_namee = './static/images/AssemblyAIProductOverview.mp4'
        file_namee = './templates/test.html'

        rsp = urlopen(filename)
        with open(file_namee,'wb') as f:
            f.write(rsp.read())
        
        sleepTime = videoD.duration * 0.4

        def read_file(file_name, chunk_size=5242880):
            with open(file_name, 'rb') as _file:
                while True:
                    data = _file.read(chunk_size)
                    if not data:
                        break
                    yield data

        headers = {'authorization': "879ba2458d7c47debbc7189214746348"}
        response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(file_namee))

        url = response.json()['upload_url']

        endpoint = "https://api.assemblyai.com/v2/transcript"
        json = { "audio_url": url }
        headers = {
            "authorization": "879ba2458d7c47debbc7189214746348",
            "content-type": "application/json"
        }
        response = requests.post(endpoint, json=json, headers=headers)
        # print(response.json())
        print(response.json()['id'])
        time.sleep(sleepTime)
        
        id = str(response.json()['id'])
        request.session['id'] = id
        endpoint = "https://api.assemblyai.com/v2/transcript/"+id
        headers = {
            "authorization": "879ba2458d7c47debbc7189214746348",
        }
        response = requests.get(endpoint, headers=headers)
        print()
        print(response.json()['text'])
        text = response.json()['text']
        request.session['text'] = text
        # context = {'text': text}
        return redirect(transcript)

    except MultiValueDictKeyError:
        return redirect(video)

def keywordSearch(request):
    id = request.session.get('id')

    endpoint = "https://api.assemblyai.com/v2/transcript/"+id+"/word-search?words=deep"
    headers = {
        "authorization": "879ba2458d7c47debbc7189214746348",
        "content-type": "application/json"
    }
    response = requests.post(endpoint, headers=headers)
    print(response.json())

    query = request.POST['query']
    print(query)
    context = {'query': query}
    return render(request, 'search.html', context)

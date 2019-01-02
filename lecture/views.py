import cv2
import numpy as np

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import CoursePackForm, PodcastForm, UserForm
from .models import CoursePack, Podcast, Video, Pdf, Evaluation
from lecture.forms import EvaluationForm



AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg', 'mp4', 'pdf']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']


def create_coursepack(request):
    if not request.user.is_authenticated():
        return render(request, 'lecture/login.html')
    else:
        form = CoursePackForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.thumbnail = request.FILES['thumbnail']
            file_type = course.thumbnail.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'course': course,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'lecture/create_coursepack.html', context)
            course.save()
            return render(request, 'lecture/detail.html', {'course': course})
        context = {
            "form": form,
        }
        return render(request, 'lecture/create_coursepack.html', context)

def delete_course(request, course_id):
    course = CoursePack.objects.get(pk=course_id)
    course.delete()
    courses = CoursePack.objects.filter(user=request.user)
    return render(request, 'lecture/index.html', {'courses': courses})




def create_podcast(request, course_id):
    form = PodcastForm(request.POST or None, request.FILES or None)
    course = get_object_or_404(CoursePack, pk=course_id)
    if form.is_valid():
        courses_podcasts = course.podcast_set.all()
        for p in courses_podcasts:
            if p.material_title == form.cleaned_data.get("material_title"):
                context = {
                    'course': course,
                    'form': form,
                    'error_message': 'You already added that podcast',
                }
                return render(request, 'lecture/create_podcast.html', context)
        podcast = form.save(commit=False)
        podcast.course = course
        podcast.material_file = request.FILES['material_file']
        file_type = podcast.material_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'course': course,
                'form': form,
                'error_message': 'Podcast file must be MP4, MP3, or OGG',
            }
            return render(request, 'lecture/create_podcast.html', context)

        podcast.save()
        return render(request, 'lecture/detail.html', {'course': course})
    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'lecture/create_podcast.html', context)


def podcasts(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'lecture/login.html')
    else:
        try:
            podcast_ids = []
            for course in CoursePack.objects.filter(user=request.user):
                for podcast in course.podcast_set.all():
                    podcast_ids.append(podcast.pk)
            users_podcasts = Podcast.objects.filter(pk__in=podcast_ids)
            if filter_by == 'favorites':
                users_podcasts = users_podcasts.filter(is_favorite=True)
        except CoursePack.DoesNotExist:
            users_podcasts = []
        return render(request, 'lecture/podcasts.html', {
            'podcast_list': users_podcasts,
            'filter_by': filter_by,
        })


def delete_podcast(request, course_id, podcast_id):
    course = get_object_or_404(CoursePack, pk=course_id)
    podcast = Podcast.objects.get(pk=podcast_id)
    podcast.delete()
    return render(request, 'lecture/detail.html', {'course': course})



def favorite(request, podcast_id):
    podcast = get_object_or_404(Podcast, pk=podcast_id)
    try:
        if podcast.is_favorite:
            podcast.is_favorite = False
        else:
            podcast.is_favorite = True
        podcast.save()
    except (KeyError, Podcast.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_course(request, course_id):
    course = get_object_or_404(CoursePack, pk=course_id)
    try:
        if course.is_favorite:
            course.is_favorite = False
        else:
            course.is_favorite = True
        course.save()
    except (KeyError, CoursePack.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'lecture/login.html')
    else:
        courses = CoursePack.objects.filter(user=request.user)
        podcast_results = Podcast.objects.all()
        query = request.GET.get("q")
        if query:
            courses = courses.filter(
                Q(course_title__icontains=query) |
                Q(instructor__icontains=query)
            ).distinct()
            podcast_results = podcast_results.filter(
                Q(material_title__icontains=query)
            ).distinct()
            return render(request, 'lecture/index.html', {
                'courses': courses,
                'podcasts': podcast_results,
            })
        else:
            return render(request, 'lecture/index.html', {'courses': courses})





def detail(request, course_id):
    if not request.user.is_authenticated():
        return render(request, 'lecture/login.html')
    else:
        user = request.user
        course = get_object_or_404(CoursePack, pk=course_id)
        return render(request, 'lecture/detail.html', {'course': course, 'user': user})




def classroom(request):
	return render(request, 'lecture/classroom.html')


def video(request):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

    while True:
        ret, frame = cap.read()
        out.write(frame) #saving
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release() #saving
    cv2.destroyAllWindows()     
    return render(request, 'lecture/video.html')    


def desktop(request):
    import cv2
    import numpy as np
    from PIL import ImageGrab

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("screen.avi", fourcc, 5.0, (1366, 760))

    while True:
        img = ImageGrab.grab()
        img_np = np.array(img)
        cv2.imshow("Screen", img_np)
        out.write(img_np)

        if cv2.waitKey(1) == 27:
            break

    out.release()
    cv2.destroyAllWindows() 
    return render(request, 'lecture/desktop.html')        




def collaboration(request):
    return render(request, 'lecture/collaboration.html')


        
        
def evaluation(request):
    return render(request, 'lecture/evaluation.html')

def answer(request):
    print("Form submitted")
    answer = request.POST["answer_area"]

    evaluation = Evaluation(answer=answer)
    evaluation.save()
    return render(request, 'lecture/evaluation.html')

def profile(request):
	return render(request, 'lecture/profile.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'lecture/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                courses = CoursePack.objects.filter(user=request.user)
                return render(request, 'lecture/index.html', {'courses': courses})
            else:
                return render(request, 'lecture/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'lecture/login.html', {'error_message': 'Invalid login'})
    return render(request, 'lecture/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                courses = CoursePack.objects.filter(user=request.user)
                return render(request, 'lecture/index.html', {'courses': courses})
    context = {
        "form": form,
    }
    return render(request, 'lecture/register.html', context)
		
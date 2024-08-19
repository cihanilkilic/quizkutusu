import os
from django.shortcuts import get_object_or_404, render
from main import settings
from question.models import Question
from django.http import HttpResponseNotFound, JsonResponse
from user.models import Profile
from django.core.paginator import Paginator
from .models import MyModel
from forum.models import *
from django.db.models import Q



# def index(request):
#     if request.user.is_authenticated:
#         users = Profile.objects.filter(following_users=request.user)
#         posts = Question.objects.filter(author__in=users)

#         for post in posts:
#             post.author_full_name = f"{post.author.first_name} {post.author.last_name}" if post.author.first_name and post.author.last_name else "Anonymous"
#             post.author_avatar_url = post.author.avatars.url if post.author.avatars else None
#         print("evet")
#     else:
#         print("hayır")
#         return render(request, "quizbox/index.html")

#     return render(request, "quizbox/index.html", {'posts': posts})

from django.templatetags.static import static
def index(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(author=request.user)
        user_avatar = user_profile.avatars

        # Kullanıcının takip ettiği kişileri al
        following_users = user_profile.following.all()

        # Kullanıcının kendi postlarını ve takip ettiği kişilerin postlarını filtrele
        posts = Question.objects.filter(Q(author=request.user) | Q(author__in=following_users))

        # Her bir postun yazarının avatarını ve adını/soyadını al
        for post in posts:
            # Kullanıcının profilini al
            author_profile = Profile.objects.get(author=post.author)
            # Kullanıcının profilinde avatar varsa URL'sini al, yoksa None döndür
            post.author_avatar = author_profile.avatars.url if author_profile.avatars else None

            # Yazarın adını ve soyadını al
            post.author_first_name = post.author.first_name
            post.author_last_name = post.author.last_name
        image_folder = os.path.join(settings.MEDIA_ROOT, 'quizbox')

        try:
            image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
        except FileNotFoundError:
            return HttpResponseNotFound("Image folder not found.")

        image_files = [os.path.join('quizbox', f) for f in image_files]

        context = {
            'image_files': image_files,
            'MEDIA_URL': settings.MEDIA_URL,
            'posts': posts,
            'user_avatar': user_avatar
        }

        return render(request, "quizbox/index.html", context)

    else:
        image_folder = os.path.join(settings.MEDIA_ROOT, 'quizbox')

        try:
            image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
        except FileNotFoundError:
            return HttpResponseNotFound("Image folder not found.")

        image_files = [os.path.join('quizbox', f) for f in image_files]

        context = {
            'image_files': image_files,
            'MEDIA_URL': settings.MEDIA_URL
        }

        return render(request, "quizbox/index.html", context)

    return render(request, "quizbox/index.html", {'posts': posts, 'user_avatar': user_avatar})



def search_questions(request):
    if request.method == 'GET' and 'term' in request.GET:
        term = request.GET.get('term')
        items = Question.objects.filter(Q(Lessons__icontains=term) | Q(Question__icontains=term))

        data = [{'pk': item.pk,
                 'text': item.Question,
                 'topic_type': item.Topics_Name,
                 'lessons': item.Lessons,
                 'author': f"{item.author.first_name} {item.author.last_name}",  # Full name
                 'Created_Date': item.Created_Date,
                 'question_image': item.Question_Image.url if item.Question_Image else None  # Include Question_Image URL if available
                } for item in items]

        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Bad Request'}, status=400)

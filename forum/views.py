from django.shortcuts import get_object_or_404, redirect, render
from user.models import *
from main import settings
from .models import *
from .forms import *
# Create your views here.
from django.http import HttpResponse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.html import escape

def forum_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateForm(request.POST, request.FILES)
            if form.is_valid():
                text = form.cleaned_data['text']
                forum_topics_post = form.cleaned_data['topic_type']
                img = form.cleaned_data['forum_image']

                if text:
                    forum_save = FORUM(author=request.user, text=text, topic_type=forum_topics_post, forum_image=img)
                    forum_save.save()
                    messages.success(request, 'Forum başarıyla oluşturuldu.')
                    return HttpResponseRedirect(reverse('forum:forum_create'))
                else:
                    forum_topics = ("Genel", "Tartışma", "Soru-Cevap")
                    context = {
                        "forum_topics": forum_topics,
                        "form": form,  # Formu tekrar göndermek için
                    }
                    messages.error(request, 'Text Alanı Boş Geçilemez.')
                    return render(request, "forum/forum_create.html", context)

        elif request.method == 'GET':
            form = CreateForm()
            forum_topics = ("Genel", "Tartışma", "Soru-Cevap")
            context = {
                "forum_topics": forum_topics,
                "form": form  # Formu gönder
            }
            return render(request, "forum/forum_create.html", context)
    else:
        messages.error(request, 'Konu Başlatmak İçin Oturum Açılmalısınız...')
        return redirect('quizorder:index')


    # if request.user.is_authenticated:
    #     forum_topics = ("Genel", "Tartışma", "Soru-Cevap")
    #     context = {"forum_topics": forum_topics}

    #     if request.method == 'POST':
    #         # Process the forum creation form
    #         form = CreateForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             instance = form.save(commit=False)
    #             instance.author = request.user  # Assuming you have a profile associated with users
    #             instance.save()
    #             return redirect('forum:forum_create')  # Redirect to success_url upon successful form submission
    #         else:
    #             # Handle invalid form data here
    #             # You can customize this based on your requirements
    #             # For example, you might want to re-render the form with errors
    #             return render(request, 'forum/forum_create.html', {'form': form, 'forum_topics': forum_topics})


    #     elif request.method == 'GET':
    #         # Handle GET request here
    #         form = CreateForm()
    #         return render(request, 'forum/forum_create.html', {'form': form, 'forum_topics': forum_topics})

    # else:
    #     return redirect('quizorder:index')





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Forum_Comment  # Forum_Comment modelini ekledik
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
@csrf_exempt
def forum_comment_create(request):
    if request.method == 'POST':
        # Form verilerini al
        comment_content_id = request.POST.get('comment_content_id')


        print("gelen ıd değeri",comment_content_id)
        comment_content = request.POST.get('comment_content')
        # Kullanıcı kimliğini almak için: request.user
        # Veritabanına kaydedin
        # forum_comment = Forum_Comment(forum_text_id=comment_content_id, comment_author=request.user, comment_content=comment_content)
        # forum_comment.save()
        ########################################################
        #forum_instance = get_object_or_404(FORUM, pk=comment_content_id)

        # Convert number_of_answers to an integer before incrementing
        #forum_instance.number_of_answers = int(forum_instance.number_of_answers) + 1
        #forum_instance.save()
        ########################################################
        # Kullanıcı kimliğini almak için: request.user
        # Veritabanına kaydedin
        forum_comment = Forum_Comment(forum_text_id=comment_content_id, comment_author=request.user, comment_content=comment_content)
        forum_comment.save()  # Save the comment first

        FORUM.objects.filter(pk=comment_content_id).update(number_of_answers=F('number_of_answers') + 1)
        # Başarılı bir şekilde kaydedildiğini varsayalım
        response_data = {'message': 'Yorum başarıyla kaydedildi.'}
        return JsonResponse(response_data)
    else:
        response_data = {'error': 'Sadece POST istekleri kabul edilir.'}
        return JsonResponse(response_data, status=400)

def discover(request):
    get_forum = FORUM.objects.all().order_by('-created_date')
    for forum in get_forum:
        # 'author' alanından ilgili Profile modeline ulaşarak 'avatars' özelliğine erişin
        author_profile = Profile.objects.get(author=forum.author)
        forum.author_avatar_url = author_profile.avatars.url if author_profile.avatars else None
    context = {
        'get_forum': get_forum
    }
    return render(request, "quizbox/discover.html", context)



from django.core.serializers import serialize
def forum_comment_list(request):
    if request.method == 'GET':
        comment_content_id = request.GET.get('comment_content_id')
        print("comment_content_id", comment_content_id)

        if comment_content_id:
            # İlgili verileri alın, örneğin:
            comments = Forum_Comment.objects.filter(forum_text_id=comment_content_id)
            get_comments_count = comments.count()
            # Yorum yapan kullanıcıların adını, soyadını ve avatarını alarak serialize edelim
            if comments.exists():
                serialized_comments = []
                for comment in comments:
                    # Profile modeline erişim yaparak avatarı al
                    author_profile = Profile.objects.get(author=comment.comment_author)
                    author_name = f"{comment.comment_author.first_name} {comment.comment_author.last_name}"
                    author_avatar = author_profile.avatars.url if author_profile.avatars else None
                    serialized_comment = {
                        "comment_content": comment.comment_content,
                        "created_date": comment.created_date,
                        "comment_author": {
                            "name": author_name,
                            "avatar": author_avatar,
                            "get_comments_count":get_comments_count
                        }
                    }
                    serialized_comments.append(serialized_comment)
                return JsonResponse({'success': True, 'comments': serialized_comments})

            else:
                return JsonResponse({'success': False, 'message': 'No comments found for the given content ID.'})
        else:
            return JsonResponse({'success': False, 'message': 'No comment content ID received.'})



def search_forum(request):
    if request.method == 'GET' and 'term' in request.GET:
        term = request.GET.get('term')
        items = FORUM.objects.filter(
        Q(text__icontains=term) & Q(topic_type__icontains=term) | 
        Q(text__icontains=term) | Q(topic_type__icontains=term)
        )
        
        #items = FORUM.objects.filter(text__icontains=term, topic_type__icontains=term)
        # Retrieve id (pk) and text fields
        data = [{'pk': item.pk, 'text': item.text,'topic_type': item.topic_type,'created_date': item.created_date,'number_of_answers':item.number_of_answers} for item in items]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Bad Request'}, status=400)


def forum_detail(request, pk):
    get_forum = get_object_or_404(FORUM, pk=pk)
    
    # Author'ın avatar fotoğrafını al
    author_avatar = None
    author_profile = Profile.objects.filter(author=get_forum.author).first()  # Author'a ait Profile nesnesini al
    if author_profile:
        author_avatar = author_profile.avatars.url
    
    context = {
        'get_forum': get_forum,
        'author_avatar': author_avatar,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, "quizbox/forum_detail.html", context)


def like_forum(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        # Önce bu kullanıcının bu soruyu daha önce beğenip beğenmediğini kontrol edelim
        if request.user.is_authenticated:
            user_profile = request.user
            question = FORUM.objects.get(pk=question_id)
            try:
                existing_like = Forum_Like.objects.get(author=user_profile, forum=question)
                # Kullanıcı bu soruyu zaten beğenmiş, beğeniyi kaldıralım
                existing_like.delete()
                like_count = Forum_Like.objects.filter(forum=question).count()
                return JsonResponse({'liked': False, 'like_count': like_count})
            except Forum_Like.DoesNotExist:
                # Kullanıcı daha önce bu soruyu beğenmemiş, yeni bir beğeni oluşturalım
                new_like = Forum_Like(author=user_profile, forum=question)
                new_like.save()
                like_count = Forum_Like.objects.filter(forum=question).count()
                return JsonResponse({'liked': True, 'like_count': like_count})
        else:
            return JsonResponse({'error': 'Kullanıcı girişi yapmış olmalısınız.'}, status=401)
        


def get_like_count(request):
    if request.method == 'GET':
        question_id = request.GET.get('question_id')
        question = FORUM.objects.get(pk=question_id)
        like_count = Forum_Like.objects.filter(forum=question).count()
        return JsonResponse({'like_count': like_count})
    
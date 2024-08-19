from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from cart.models import CartExamTitle
from exam.models import Exam
from user.models import Profile
from question.models import Lesson,Topic
from .import *
from django.contrib import messages
from .models import Question
from django.db.models import Q
import random
from cart .views import*
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Comment, Like
from .forms import CommentForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render

def Question_(request):
    try:
        context_from_question = Question_2(request)
    except Exception as e:
        # Hata ile ilgili işlem yapın, burada sadece hatayı ekrana yazdıralım
        print("Bir hata oluştu:", e)
        # Hata durumunda yönlendirilecek olan sayfanın URL'sini belirleyin
        redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)

    return render(request, "question/question.html", context_from_question)




def Question_2(request):
    request_user = Profile.objects.get(author_id=request.user.id)
    
    if request_user.user_types =="Teacher":
        Question_Type = ("Çoktan Seçmeli","Boşluk Doldurma","Klasik","Doğru/Yanlış","Eşleştirme")
        Question_Numer = (1,2,3,4,5,6,7,8,9,10)
        Level = ("KOLAY","ORTA","ZOR")
        existing_exam_title=CartExamTitle.objects.filter(author_id=request.user).order_by('-created_date')

        lesson_topics = []

        for lesson in request_user.lessons.all():
            lessons_topics = Topic.objects.filter(Lessons_Name=lesson)
            
            for lessons_topic in lessons_topics:
                topic_name = lessons_topic.Topics_Name
                lesson_topics.append({
                    'lesson_name': lesson,
                    'topic_name': topic_name,
                })

            context = {
                'RequestUser': request_user,
                'lesson_topics': lesson_topics,
                'Question_Type':Question_Type,
                'existing_exam_title':existing_exam_title,
                'Level':Level,
                'Question_Numer':Question_Numer

            }

            return context
    else:
        return redirect(request,"quizbox:index")



def get_lessons(request):

    classroom_id = request.GET.get('classroom_id')
    lessons = Lesson.objects.filter(Classrooms_Name__id=classroom_id)
    lesson_data = {}
    for lesson in lessons:
        lesson_data[lesson.id] = lesson.Lessons_Name
    return JsonResponse(lesson_data)


# views.py
def get_topics(request):
    lesson_id = request.GET.get('lesson_id')
    topics = Topic.objects.filter(Lessons_Name__id=lesson_id)
    topic_data = {}
    for topic in topics:
        topic_data[topic.id] = topic.Topics_Name
    return JsonResponse(topic_data)


def question_detail(request, id):
    detail = get_object_or_404(Question, id=id)
    like_count = Like.objects.filter(question=id).count()
    comment_content_show = Comment.objects.filter(question=id)
    author_names = []  # Yazar adlarını tutmak için boş bir liste oluştur

    for comment in comment_content_show:
        # Yorumun yazarının avatar fotoğrafını al
        author_avatar = None
        author_profile = Profile.objects.filter(author=comment.comment_author).first()  # Yorumun yazarına ait Profile nesnesini al
        if author_profile:
            comment.author_avatar_url = author_profile.avatars.url if author_profile.avatars else None
        
        # Yazar adını oluştur ve listeye ekle
        author_name = f"{comment.comment_author.first_name} {comment.comment_author.last_name}"
        author_names.append(author_name)  

    cnt = comment_content_show.count()
    context = {
        'detail': detail,
        'author_names': author_names,  # Yazar adlarını context içinde gönder
        'comment_content_show': comment_content_show,
        'cnt': cnt,
        'like_count': like_count
    }

    return render(request, 'question/question_detail.html', context)




def add_comment(request, question_id):
    # İlgili soruyu alıyoruz
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        comment_content = request.POST["comment_content"]

        # Eğer HTTP POST isteği alınıyorsa, formu oluşturuyoruz ve verileri işliyoruz

        new_comment = Comment( comment_author = request.user, comment_content = comment_content, question = question)
# Eğer kullanıcı profili kullanıyorsanız bu şekilde ayarlayabilirsiniz
        new_comment.save()
        return redirect("question:question_detail",question_id)
    else:
        # Eğer HTTP GET isteği alınıyorsa, boş bir form oluşturuyoruz

        return render(request, 'question/question_detail.html')
# def question_detail(request, id):
#     detail = get_object_or_404(Question, id=id)
#     # Eğer nesne varsa, burada işlemler yapılır
#     return render(request, 'question/question_detail.html', {'detail': detail})

def question_delete(request):
    # try:
    #     detail = get_object_or_404(Question, id=id)
    #     detail.delete()
    #     # return render(request, 'question/question_detail.html', {'detail': detail})
    #     return HttpResponse("<h1>İçerik Silindi.</h1>")

    # except:
    #     return HttpResponse("<h1>İçerik Bulunamadı.</h1>", status=404)
    user = request.user
    if user.is_authenticated:
        if user.user_types =="Teacher":

            if request.method == 'POST':
                exam_item_id = request.POST.get('user_id')
                # Assuming the user is logged in
                print("Exam item ID:", exam_item_id)
                product = get_object_or_404(Question, id=exam_item_id)
                # Create a new cart item
                product.delete()
                return JsonResponse({'success': product.Lessons,'Topics_Name': product.Topics_Name,'Level': product.Level})
            return JsonResponse({'success': False})

        else:
            redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)









# def article_create(request):
#     if request.method == "POST":
#         form = Question_Create_Form(request.POST, request.FILES)

#         if form.is_valid():
#             lesson= request.POST.get('Lessons')
#             topic= request.POST.get('Topics_Name')

#             Choice_A= request.POST.get('Choice_A')
#             Choice_B= request.POST.get('Choice_B')
#             Choice_C= request.POST.get('Choice_C')
#             Choice_D= request.POST.get('Choice_D')
#             Choice_E= request.POST.get('Choice_E')

#             topics = get_object_or_404(Topic,id=topic)
#             Lessonn = get_object_or_404(Lesson,id=lesson)
            
#             article = form.save(commit=False)
#             article.author = request.user
#             article.Lessons = Lessonn
#             article.Topics_Name = topics

#             article.Choice_A = Choice_A
#             article.Choice_B = Choice_B
#             article.Choice_C = Choice_C
#             article.Choice_D = Choice_D
#             article.Choice_E = Choice_E







#             article.save()
#             # messages.success(request, 'Makale başarıyla oluşturuldu.')  # Başarılı mesajı
#             return render(request, 'question/question.html', {'success': 'Makale başarıyla oluşturuldu.'})


#             # Diğer işlemleri yapabilirsiniz, gerektiği gibi.
#         else:
#             # messages.error(request, 'Formda hatalar var. Lütfen tekrar deneyin.')  # Hata mesajı
#             return render(request, 'question/question.html', {'error': 'Formda hatalar var. Lütfen tekrar deneyin.'})

#     else:
#         form = Question_Create_Form()

#     return render(request, 'question/question.html', {'form': form})



def article_create(request):

    user = get_object_or_404(Profile, author_id=request.user.id)
     
    if request.user.is_authenticated:

        if user.user_types == "Teacher":
            if request.method == 'POST':
                # Process form data here
                lesson= request.POST.get('Lessons')
                Answer= request.POST.get('Answer')
                Dogru_Yanlis= request.POST.get('Dogru_Yanlis')
                Question_Ticket= request.POST.get('Question_Ticket')
                Question_Image = request.FILES.get('Question_Image')
                topic= request.POST.get('Topics_Name')
                classroom_id = request.POST.get('Classroom')
                question = request.POST.get('Question')
                choice_a = request.POST.get('Choice_A')
                choice_b = request.POST.get('Choice_B')
                choice_c = request.POST.get('Choice_C')
                choice_d = request.POST.get('Choice_D')
                choice_e = request.POST.get('Choice_E')
                selected_option = request.POST.get('SIK')
                Question_Types = request.POST.get('Question_Types')
                Level= request.POST.get('Level')
                topics = get_object_or_404(Topic,id=topic)
                Lessonn = get_object_or_404(Lesson,id=lesson)
                text_before_input_1_values = request.POST.getlist('text_before_input_1')
                text_before_input_2_values = request.POST.getlist('text_before_input_2')
                def process_values(text_before_input_1_values, text_before_input_2_values):
                    for i in range(len(text_before_input_1_values)):
                        value_1 = text_before_input_1_values[i]
                        value_2 = text_before_input_2_values[i]
                # Do something with the values, for example, print them

                # Save data to the database using Django models
                if selected_option:
                    ONE_SAVE = Question(
                        author_id = request.user.id,
                        Classroom=classroom_id,
                        Question_Image = Question_Image,
                        Question=question,
                        Choice_A=choice_a,
                        Choice_B=choice_b,
                        Choice_C=choice_c,
                        Choice_D=choice_d,
                        Choice_E=choice_e,
                        Answer=selected_option,
                        Lessons = Lessonn,
                        Topics_Name = topics,
                        Question_Types= Question_Types,
                        Level = Level
                    )
                    ONE_SAVE.save()

                # Dummy response for demonstration

                if Question_Types == "Boşluk Doldurma":
                    TWO_SAVE = Question(
                        author_id = request.user.id,
                        Classroom=classroom_id,
                        Question=question,
                        Answer=Answer,
                        Lessons = Lessonn,
                        Topics_Name = topics,
                        Question_Types= Question_Types,
                        Level = Level,
                        Question_Image = Question_Image,

                    )
                    TWO_SAVE.save()

                if Question_Types == "Klasik":
                    THREE_SAVE = Question(
                        author_id = request.user.id,
                        Classroom=classroom_id,
                        Question=question,
                        Answer=Answer,
                        Lessons = Lessonn,
                        Topics_Name = topics,
                        Question_Types= Question_Types,
                        Level = Level,
                        Question_Image = Question_Image,

                    )
                    THREE_SAVE.save()
                if Question_Types == "Doğru/Yanlış":
                    FOUR_SAVE = Question(
                        author_id = request.user.id,
                        Classroom=classroom_id,
                        Question=question,
                        Answer=Dogru_Yanlis,
                        Lessons = Lessonn,
                        Topics_Name = topics,
                        Question_Types= Question_Types,
                        Level = Level,
                        Question_Image = Question_Image,

                    )
                    FOUR_SAVE.save()
                if Question_Types == "Eşleştirme":
                    process_values(text_before_input_1_values, text_before_input_2_values)
                    FIVE_SAVE = Question(
                        author_id = request.user.id,
                        Classroom=classroom_id,
                        Ticket=Question_Ticket,
                        Cell_1=text_before_input_1_values,
                        Cell_2=text_before_input_2_values,
                        Question=question,
                        #Answer=Dogru_Yanlis,
                        Lessons = Lessonn,
                        Topics_Name = topics,
                        Question_Types= Question_Types,
                        Level = Level,
                        Question_Image = Question_Image

                    )
                    FIVE_SAVE.save()
                response_data = {'message': 'Form data received and saved successfully'}
                return JsonResponse(response_data)
            return render(request, 'question/question.html')  # Replace 
        else:
            redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)






@csrf_exempt
def save_input_value(request):
    if request.method == 'POST':
        input_value = request.POST.get('input')
        print('Received input value:', input_value)
        exam_title_instance = CartExamTitle(exam_title=input_value,author=request.user)
        exam_title_instance.save()
        return JsonResponse({'success': True,})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

# @csrf_exempt
# def save_input_value(request):
#     if request.method == 'POST':
#         exam_titles = CartExamTitle.objects.values_list('exam_title', flat=True).order_by('-created_date')
#         input_value = request.POST.get('input')
#         print('Received input value:', input_value)
#         exam_title_instance = CartExamTitle(exam_title=input_value,author=request.user)
#         exam_title_instance.save()
#         return JsonResponse({'success': True,'exam_titles': list(exam_titles)})
#     else:
#         return JsonResponse({'success': False, 'message': 'Invalid request method'})
    # if request.method == 'POST':
    #     # Assuming the input value is sent in the POST request
    #     input_value = request.POST.get('input')
    #     author = request.user

    #     # Check if a CartExamTitle with the same exam_title and author already exists
    #     existing_exam_title = CartExamTitle.objects.filter(exam_title=input_value, author=author).first()

    #     if existing_exam_title:
    #         # If a CartExamTitle with the same exam_title and author exists, suggest trying a different name
    #         message = f'A title with the name "{input_value}" already exists. Please try a different name.'
    #         return JsonResponse({'success': False, 'message': message})
    #     else:
    #         # If no existing title with the same exam_title and author, create a new instance and save it
    #         exam_title_instance = CartExamTitle(exam_title=input_value, author=author)
    #         exam_title_instance.save()
    #         return JsonResponse({'success': True})
    # else:
    #     return JsonResponse({'success': False, 'message': 'Invalid request method'})

# def get_exam_titles(request):
#     exam_titles = CartExamTitle.objects.values_list('exam_title', flat=True,author=request.user).order_by('-created_date')
#     return JsonResponse({'exam_titles': list(exam_titles)})

def get_exam_titles(request):
    exam_titles = CartExamTitle.objects.filter(author=request.user).values_list('exam_title', flat=True).order_by('-created_date')
    return JsonResponse({'exam_titles': list(exam_titles)})





# def show_filtered_list(filtere_list):
#     for item in filtere_list:
#         print("Eleman:", item)

# # Sample usage
# filtere_list = [1, 2, 3, 'a', 'b', 'c']
# show_filtered_list(filtere_list)


@csrf_exempt
# def exam_save(request):
#     exam_title_id = request.POST.get('exam_title_id')
#     question_count = request.POST.get('question_count')
#     user = request.user

#     global global_filtere_list  # global değişkene erişim sağlıyoruz

#     # Eğer global_filtere_list boş değilse Exam modeline kayıtları ekleyelim
#     if global_filtere_list:
#         for item in global_filtere_list:
#             topics_name = item['Topics_Name']
#             question_types = item['Question_Types']
#             level = item['Level']
#             lessons = item['Lessons']
#             classroom = item['Classroom']

#             question = Exam.objects.create(
#                 Lessons=lessons,
#                 Question=item['Question'],
#                 Answer=item['Answer'],
#                 Classroom=classroom,
#                 Topics_Name=topics_name,
#                 Question_Types=question_types,
#                 Level=level,
#                 Exam_Title=exam_title_id,
#                 Question_Image=item['Question_Image'],
#                 author=user  # Assign the user as the author
#             )


#         response_data = {'message': 'Sınav kaydedildi ve Exam modele kaydedildi!'}
#     else:
#         response_data = {'message': 'Sınav kaydedildi, ancak global_filtere_list boş olduğu için Exam modele kaydedilmedi.'}

#     return JsonResponse(response_data)
def exam_save(request):
    exam_title_id = request.POST.get('exam_title_id')
    question_count = int(request.POST.get('question_count'))  # Convert to int
    user = request.user

    global global_filtere_list  # Global değişkene erişim sağlıyoruz

    # Eğer global_filtere_list boş değilse Exam modeline kayıtları ekleyelim
    if global_filtere_list:
        selected_questions = random.sample(global_filtere_list, min(question_count, len(global_filtere_list)))

        for item in selected_questions:
            topics_name = item['Topics_Name']
            question_types = item['Question_Types']
            level = item['Level']
            lessons = item['Lessons']
            classroom = item['Classroom']
            Choice_A=item['Choice_A']
            Choice_B=item['Choice_B']
            Choice_C=item['Choice_C']
            Choice_D=item['Choice_D']
            Choice_E=item['Choice_E']
            print(item['id'])
            question = Exam.objects.create(
                Lessons=lessons,
                Question=item['Question'],
                Answer=item['Answer'],
                Classroom=classroom,
                Topics_Name=topics_name,
                Question_Types=question_types,
                Level=level,
                Choice_A =Choice_A,
                Choice_B =Choice_B,
                Choice_C =Choice_C,
                Choice_D =Choice_D,
                Choice_E =Choice_E,
                Exam_Title=exam_title_id,
                Question_Image=item['Question_Image'],
                Question_ID=item['id'],
                author=user  # Assign the user as the author
            )

        response_data = {'message': f'{len(selected_questions)} soru rastgele seçilerek Exam modele kaydedildi!'}
    else:
        response_data = {'message': 'Sınav kaydedildi, ancak global_filtere_list boş olduğu için Exam modele kaydedilmedi.'}

    return JsonResponse(response_data)




# global_filtere_list = None
# def quiz(request):
#     if not request.user.is_authenticated:
#         return redirect('quizbox:index')  # 'index' URL'sini projeye göre değiştirin

#     user_profile = get_object_or_404(Profile, author=request.user)
#     if user_profile.user_types != "Teacher":
#         return redirect('quizbox:index')  # Öğrenci ise anasayfaya yönlendir

#     context_from_question = Question_2(request)  # Bu fonksiyon tanımlanmış olmalı

#     if request.method == "POST":
#         classroom = request.POST.get('Classroom')
#         question_types = request.POST.get('Question_Types')
#         level = request.POST.get('Level')
#         lesson_id = request.POST.get('Lessons')
#         topics_id = request.POST.get('Topics_Name')

#         try:
#             lesson = get_object_or_404(Lesson, id=lesson_id)
#             topics = get_object_or_404(Topic, id=topics_id)
#         except:
#             return JsonResponse({'success': False, 'message': 'Ders veya konu bulunamadı.'})

#         filtere = Question.objects.filter(
#             Lessons=lesson, Topics_Name=topics, Question_Types=question_types, Level=level, Classroom=classroom
#         )
#         cnt = filtere.count()

#         filtere_values = list(filtere.values('id', 'Lessons', 'Topics_Name', 'Question_Types', 'Level', 'Question', 'Question_Image'))
#         for question in filtere_values:
#             question['Question_Image'] = str(question['Question_Image'])

#         return JsonResponse({
#             'success': True,
#             'message': 'Filtrelenmiş sorular başarıyla alındı.',
#             'filtere': filtere_values,
#             'cnt': cnt
#         })

#     return render(request, 'quiz/quiz.html', context_from_question)





global_filtere_list = None

def quiz(request):
    user = get_object_or_404(Profile, author_id=request.user.id)
     
    if request.user.is_authenticated:
        if user.user_types =="Teacher":
            global global_filtere_list  # global değişkeni kullanacağımızı belirtiyoruz

            context_from_question = Question_2(request)
            classroom = request.POST.get('Classroom')
            Question_Types = request.POST.get('Question_Types')
            Level = request.POST.get('Level')


            if request.method == "POST":
                lesson = request.POST.get('Lessons')
                topicss = request.POST.get('Topics_Name')
                topics = get_object_or_404(Topic, id=topicss)
                Lessonn = get_object_or_404(Lesson, id=lesson)

                filtere = Question.objects.filter(Q(Lessons=Lessonn) & Q(Topics_Name=topics) & Q(Question_Types=Question_Types) & Q(Level=Level) & Q(Classroom=classroom))
                
                cnt = filtere.count()

                # global değişkeni güncelliyoruz

                global_filtere_list = list(filtere.values())
                for question in global_filtere_list:
                    question['Question_Image'] = str(question['Question_Image'])
                response_data = {
                    'success': True,
                    'message': 'Successfully retrieved filtered questions.',
                    'filtere': global_filtere_list,
                    'cnt': cnt
                }

                return JsonResponse(response_data, safe=False)  

            else:
                return render(request, 'quiz/quiz.html', context_from_question)
        else:
            redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)













def show_cart(request):
    user = get_object_or_404(Profile, author_id=request.user.id)
     
    if request.user.is_authenticated:
        if user.user_types =="Teacher":
            cart_shows = Cart.objects.filter(author=request.user).order_by('-created_date')
            exam_title = CartExamTitle.objects.filter(author=request.user).order_by('-created_date')
            context = {
                'cart_shows': cart_shows,
                'exam_title': exam_title
            }
            return render(request, 'cart/cart_show.html', context)
        else:
            redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)
# def exam_save_2(request):
#     exam_title_id = request.POST.get('exam_title_id')
#     user_id = request.POST.get('ques_id')
#     print( "buradalar", exam_title_id,user_id)
from django.views.decorators.http import require_POST

def exam_save_2(request):
    user = get_object_or_404(Profile, author_id=request.user.id)
     
    if request.user.is_authenticated:
        if user.user_types =="Teacher":
            if request.method == 'POST':
                ques_id = request.POST.get('user_id')
                exam_title_id = request.POST.get('exam_title_id')
                user = request.user

                # POST isteği ile gelen verileri işle
                getir = Question.objects.filter(id=ques_id).first()
                question = Exam.objects.create(
                    Lessons=getir.Lessons,
                    Question=getir.Question,
                    Answer=getir.Answer,
                    Classroom=getir.Classroom,
                    Topics_Name=getir.Topics_Name,
                    Question_Types=getir.Question_Types,
                    Level=getir.Level,
                    Choice_A=getir.Choice_A,
                    Choice_B=getir.Choice_B,
                    Choice_C=getir.Choice_C,
                    Choice_D=getir.Choice_D,
                    Choice_E=getir.Choice_E,
                    Exam_Title=exam_title_id,
                    Question_Image=getir.Question_Image,
                    Question_ID=ques_id,
                    author=user
                )
                # cart_shows = Cart.objects.filter(author=request.user,exam_items=ques_id)
                # cart_shows.delete()
                # Sonuçları JSON olarak döndür
                data = {'success': 'Başarıyla Sınava Eklendi','exam_title_id':exam_title_id, 'user_id': ques_id}
                return JsonResponse(data)
            elif request.method == 'GET':
                    # ... diğer kodlar ...
                result = show_cart(request)
                # ... diğer kodlar ...
                return result

            else:
                return JsonResponse({'error': 'Geçersiz istek'})
    
        else:
            redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)


def exam_save_2_cart_delete(request,id):
    cart_shows = Cart.objects.filter(author=request.user,exam_items=id)
    cart_shows.delete()
    result = show_cart(request)
    
    # ... diğer kodlar ...
    return result



@require_POST
def like_question(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        # Önce bu kullanıcının bu soruyu daha önce beğenip beğenmediğini kontrol edelim
        if request.user.is_authenticated:
            user_profile = request.user
            question = Question.objects.get(pk=question_id)
            try:
                existing_like = Like.objects.get(author=user_profile, question=question)
                # Kullanıcı bu soruyu zaten beğenmiş, beğeniyi kaldıralım
                existing_like.delete()
                like_count = Like.objects.filter(question=question).count()
                return JsonResponse({'liked': False, 'like_count': like_count})
            except Like.DoesNotExist:
                # Kullanıcı daha önce bu soruyu beğenmemiş, yeni bir beğeni oluşturalım
                new_like = Like(author=user_profile, question=question)
                new_like.save()
                like_count = Like.objects.filter(question=question).count()
                return JsonResponse({'liked': True, 'like_count': like_count})
        else:
            return JsonResponse({'error': 'Kullanıcı girişi yapmış olmalısınız.'}, status=401)
        





def get_like_count(request):
    if request.method == 'GET':
        question_id = request.GET.get('question_id')
        question = Question.objects.get(pk=question_id)
        like_count = Like.objects.filter(question=question).count()
        return JsonResponse({'like_count': like_count})
    


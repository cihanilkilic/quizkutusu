from django.shortcuts import redirect, render
from datetime import datetime
from .models import Question_Choice,Exam_Result, Exam_Table, TIMER_S, Testing_Choice, TIMER_S_TESTTING,Testing_Table,Testing_Result,TYT_Choice,TIMER_S_TYT,TYT_Table,TYT_Result,AYT_Choice,AYT_TIMER_S,AYT_Table,AYT_Result
# Create your views here.
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

def testing_and_exam(request):
    return render(request,"testing_and_exam/testing_and_exam.html")

#DENEME WIEWS ALANI BAŞLANGIÇ
@login_required
def testing(request):
    if request.user.is_authenticated:
        if request.method == 'GET':

            class_choice = ("9. Sınıf","10. Sınıf","11. Sınıf","12. Sınıf")
            Lessons_choice  = ('Matematik','Biyoloji','Kimya','Fizik','Tarih','Coğrafya','İngilizce','Türk Dili ve Edebiyatı','Din Kültürü ve Ahlak Bilgisi')

            context={
                'class_choice':class_choice,
                'Lessons_choice':Lessons_choice
            }
            return render(request,"testing_and_exam/testing.html",context)
        if request.method == 'POST':
            class_choice = ("9. Sınıf","10. Sınıf","11. Sınıf","12. Sınıf")
            Lessons_choice  = ('Matematik','Biyoloji','Kimya','Fizik','Tarih','Coğrafya','İngilizce','Türk Dili ve Edebiyatı','Din Kültürü ve Ahlak Bilgisi')
            class_choice_ = request.POST.get('sinif')
            Lessons_choice_ = request.POST.get('ders')
            #All_Test = Testing_Choice.objects.filter(Q(Class_Choice=class_choice_) & Q(Lessons_Name=Lessons_choice_))
            
            All_Test = Testing_Choice.objects.filter(
                Q(Class_Choice=class_choice_) & 
                Q(Lessons_Name=Lessons_choice_) 
            )

            unique_testing_names = All_Test.values('Testing_Name').distinct()
            first_testing = [All_Test.filter(Testing_Name=testing_name['Testing_Name']).first() for testing_name in unique_testing_names]

            sinavi_goster = False  # Default value

            for cihan in All_Test:
                users = cihan.testi_cozen_kisi.all()
                if request.user in users:
                    sinavi_goster = True
                    #print("TESTİ ÇÖZEN KİŞİNİN ID'Sİ=>", request.user.id, "TESTİN ADI:>", cihan.Testing_Name)
                    break  # Exit loop early since we found a match

            cnt = All_Test.count()

            context = {
                'class_choice': class_choice,
                'Lessons_choice': Lessons_choice,
                'first_testing': first_testing,
                'sinavi_goster': sinavi_goster,
                'cnt': cnt
            }

            return render(request, "testing_and_exam/testing.html", context)


    else:
        messages.error(request, "Denemeleri Görüntüleyebilmek İçin Oturum Açınız...")
        return render(request,"testing_and_exam/testing_and_exam.html")
    

def show_testing(request,Testing_Name):
    if request.user.is_authenticated:
        Exam_Name_Filter = Testing_Choice.objects.filter(Testing_Name=Testing_Name)
        Exam_Time_All = get_object_or_404(TIMER_S_TESTTING, Testing_Name=Testing_Name)

        #Exam_Time_All = TIMER_S.objects.all()
        cnt = Exam_Name_Filter.count()
        context={
            'Exam_Name_Filter':Exam_Name_Filter,
            'cnt':cnt,
            'Exam_Time_All':Exam_Time_All
        }
        return render(request,"testing_and_exam/show_testing.html",context)
    else:

        return redirect("testing_and_exam:testing_and_exam")


def result_testing(request):
    if request.method == 'POST':
        # AJAX isteği ile gönderilen verileri alma
        selected_choices_str = request.POST.get('selectedChoices', '')
        elapsed_time = request.POST.get('elapsed_time')
        print("süreeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",elapsed_time)
        # elapsed_minutes = request.POST.get('elapsedMinutes')
        # elapsed_seconds = request.POST.get('elapsedSeconds')
        # print(f"Elapsed Minutes: {elapsed_minutes}")
        # print(f"Elapsed Seconds: {elapsed_seconds}")


        try:
            # JSON formatındaki veriyi Python dictionary'ye çevirme
            selected_choices = json.loads(selected_choices_str)
            user=request.user
            cevap_yanlis_sayisi = 0
            cevap_dogru_sayisi = 0
            cevap_bos_sayisi = 0
            ders=""
            # Seçenekleri ekrana yazdırma (örnek olarak, konsola yazdırma)
            for question_id, choice in selected_choices.items():
                print(f"Question ID: {question_id}, Selected Choice: {choice}")
                print(question_id,choice)
                _result_=Testing_Choice.objects.all()

                #_result_=Question_Choice.objects.filter(id=question_id,Answer_Choice=choice)
                _result_true = _result_.filter(Q(id=question_id) & Q(Answer_Choice=choice))
                _result_false = _result_.filter(Q(id=question_id) & ~Q(Answer_Choice=choice))
                question_choice = Testing_Choice.objects.get(id=question_id)
                

                su_an = datetime.now()


                if _result_true.exists():
                    for result in _result_true:
                        print("SSSSSSSSSSSSSSSSSSSSSSSS", result.Answer_Choice)
                        print("Cevap Doğru")
                        _result_save = Testing_Result(
                            author=user,
                            Testing_Name=result.Testing_Name,
                            Question_Id=question_id,
                            Question_Key=result.Answer_Choice,
                            author_Key=choice,
                            True_Answer=1
                        )
                        question_choice.testi_cozen_kisi.add(user)
                        question_choice.save()

                        _result_save.save()
                        cevap_dogru_sayisi += 1
                        ders=result.Testing_Name
                else:
                    if choice == "N":
                        for item3 in _result_false:
                            print("Cevap Boş")
                            _result_save3 = Testing_Result(
                                author=user,
                                Testing_Name=item3.Testing_Name,
                                Question_Id=question_id,
                                Question_Key=item3.Answer_Choice,
                                author_Key=choice,
                                True_Answer=2
                            )
                            question_choice.testi_cozen_kisi.add(user)
                            question_choice.save()
                            _result_save3.save()
                            cevap_bos_sayisi += 1
                            ders=item3.Testing_Name
                    else:
                        if _result_false.exists():
                            for item2 in _result_false:
                                print("Cevap Yanlış")
                                _result_save2 = Testing_Result(
                                    author=user,
                                    Testing_Name=item2.Testing_Name,
                                    Question_Id=question_id,
                                    Question_Key=item2.Answer_Choice,
                                    author_Key=choice,
                                    True_Answer=0
                                )
                                question_choice.testi_cozen_kisi.add(user)
                                question_choice.save()
                                _result_save2.save()
                                cevap_yanlis_sayisi += 1
                                ders=item2.Testing_Name

            print("Cevap Doğru Sayısı:", cevap_dogru_sayisi)
            print("Cevap Yanlış Sayısı:", cevap_yanlis_sayisi)
            print("Cevap Boş Sayısı:", cevap_bos_sayisi)
            _total_ = cevap_bos_sayisi + cevap_dogru_sayisi + cevap_yanlis_sayisi
            exam_table_save=Testing_Table.objects.create(
                author=user,
                Testing_Name=ders,
                Total_Number_Of_Questions=_total_,
                Number_Of_True=cevap_dogru_sayisi,
                Number_Of_False=cevap_yanlis_sayisi,
                Number_Of_Empty=cevap_bos_sayisi,
                Testing_Score=6,
                Testing_Rating=10,
                Completion_Time=elapsed_time,
                #Completion_Time= SINAV BİTİRME SÜRESİ GELECEK
                Testing_Date=su_an,
            )
            exam_table_save.save()
            # Başarılı bir şekilde işlendiğine dair bir JSON yanıt gönderme
            #return redirect('quizorder:index')
            return JsonResponse({'message': 'Veriler başarıyla işlendi.'})
        except json.JSONDecodeError:
            # JSON decode hatası durumunda hata mesajı gönderme
            return JsonResponse({'error': 'Veri çözümlenemedi.'}, status=400)

    # POST isteği değilse veya herhangi bir hata oluşursa boş bir JSON yanıt gönderme
    return JsonResponse({})




def testing_result_show(request):
    if request.user.is_authenticated:
        user=request.user
        #exam_finif = get_object_or_404(Exam_Table, author=user)
        exam_finif = Testing_Table.objects.filter(author=user).order_by('-id')
        cnt=exam_finif.count()


        context ={
            'exam_finif':exam_finif,
            'cnt':cnt
        }
        return render(request,"testing_and_exam/testing_result_show.html",context)
    else:
        return redirect('quizorder:index')


def testing_show_result_details(request, Testing_Name):
    if request.user.is_authenticated:
        user = request.user
        get_questions = Testing_Choice.objects.filter(Testing_Name=Testing_Name)
        exam_results_list = []  # Create an empty list to store exam results
        for get_question2 in get_questions:
            exam_results = Testing_Result.objects.filter(author_id=user, Question_Id=get_question2.pk, Testing_Name=get_question2.Testing_Name)
            for exam_rslt2 in exam_results:
                if get_question2.pk == exam_rslt2.Question_Id:
                    print("evet ")
                    exam_results_list.append(exam_rslt2)  # Append each exam result to the list

        context = {
            'exam_results': exam_results_list,
            'get_questions': get_questions,
        }
        
        return render(request, "testing_and_exam/testing_show_result_details.html", context)

    else:
        return redirect('quizorder:index')









#DENEME WIEWS ALANI BİTİŞ
#-------------------------------------------------------------------------------------------------------------------------------------------#  
#SINAV WIEWS ALANI BAŞLANGIÇ
@login_required
def exam_(request):
    if request.user.is_authenticated:
        
        if request.method == 'GET':



            Lessons_choice  = ('Matematik','Biyoloji','Kimya','Fizik','Tarih','Coğrafya','İngilizce','Türk Dili ve Edebiyatı','Din Kültürü ve Ahlak Bilgisi')
            period_choice = ("1. Dönem","2. Dönem")
            class_choice = ("9. Sınıf","10. Sınıf","11. Sınıf","12. Sınıf")
            
            context={
     
                'class_choice':class_choice,
                'period_choice':period_choice,
                'Lessons_choice':Lessons_choice
            }
            return render(request,"testing_and_exam/exam_.html",context)
        if request.method == 'POST':
            exam_rating = None

            Lessons_choice  = ('Matematik','Biyoloji','Kimya','Fizik','Tarih','Coğrafya','İngilizce','Türk Dili ve Edebiyatı','Din Kültürü ve Ahlak Bilgisi')
            period_choice = ("1. Dönem","2. Dönem")
            class_choice = ("9. Sınıf","10. Sınıf","11. Sınıf","12. Sınıf")

            class_choice_ = request.POST.get('class_choice')
            Lessons_choice_ = request.POST.get('lessons_choice')
            period_choice_ = request.POST.get('period_choice')
            # All_Exam = Question_Choice.objects.filter(Q(Class_Choice=class_choice_) & Q(Lessons_Name=Lessons_choice_) & Q(Period_Name=period_choice_)).values('Exam_Name').annotate(count=Count('Exam_Name'))
# Filtreleme işlemi

            All_Exam = Question_Choice.objects.filter(
                Q(Class_Choice=class_choice_) & 
                Q(Lessons_Name=Lessons_choice_) & 
                Q(Period_Name=period_choice_)
            )

            unique_exam_names = All_Exam.values('Exam_Name').distinct()
            first_exams = [All_Exam.filter(Exam_Name=exam_name['Exam_Name']).first() for exam_name in unique_exam_names]

            sinavi_goster = False  # Default value

            for cihan in All_Exam:
                users = cihan.sinavi_cozen_kisi.all()
                if request.user in users:
                    sinavi_goster = True
                    #print("TESTİ ÇÖZEN KİŞİNİN ID'Sİ=>", request.user.id, "TESTİN ADI:>", cihan.Exam_Name)
                    break  # Exit loop early since we found a match


            cnt = All_Exam.count()
            context={
                'first_exams': first_exams,
                'class_choice':class_choice,
                'period_choice':period_choice,
                'Lessons_choice':Lessons_choice,
                'sinavi_goster':sinavi_goster,
                'cnt':cnt,
                'exam_rating':exam_rating
            }
            return render(request,"testing_and_exam/exam_.html",context)
            
    else:
        messages.error(request, "Sınavları Görüntüleyebilmek İçin Oturum Açınız...")
        return render(request,"testing_and_exam/testing_and_exam.html")




# def exam_(request):
#     if request.user.is_authenticated:
        
#         if request.method == 'GET':
#             Lessons_choice = ('Matematik', 'Biyoloji', 'Kimya', 'Fizik', 'Tarih', 'Coğrafya', 'İngilizce', 'Türk Dili ve Edebiyatı', 'Din Kültürü ve Ahlak Bilgisi')
#             period_choice = ("1. Dönem", "2. Dönem")
#             class_choice = ("9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf")
            
#             context = {
#                 'class_choice': class_choice,
#                 'period_choice': period_choice,
#                 'Lessons_choice': Lessons_choice
#             }
#             return render(request, "testing_and_exam/exam_.html", context)

#         if request.method == 'POST':
#             Lessons_choice = ('Matematik', 'Biyoloji', 'Kimya', 'Fizik', 'Tarih', 'Coğrafya', 'İngilizce', 'Türk Dili ve Edebiyatı', 'Din Kültürü ve Ahlak Bilgisi')
#             period_choice = ("1. Dönem", "2. Dönem")
#             class_choice = ("9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf")

#             class_choice_ = request.POST.get('class_choice')
#             Lessons_choice_ = request.POST.get('lessons_choice')
#             period_choice_ = request.POST.get('period_choice')

#             first_exam = Question_Choice.objects.filter(
#                 Q(Class_Choice=class_choice_) & Q(Lessons_Name=Lessons_choice_) & Q(Period_Name=period_choice_)
#             ).first()

#             context = {
#                 'first_exam': first_exam,
#                 'class_choice': class_choice,
#                 'period_choice': period_choice,
#                 'Lessons_choice': Lessons_choice,
#             }
#             return render(request, "testing_and_exam/exam_.html", context)
            
#     else:
#         messages.error(request, "Sınavları Görüntüleyebilmek İçin Oturum Açınız...")
#         return render(request, "testing_and_exam/testing_and_exam.html")










@csrf_exempt
def get_elapsed_time(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time', 0)
        current_time = int(time.time())
        elapsed_time = current_time - int(start_time)
        return JsonResponse({'elapsed_time': elapsed_time})
    return JsonResponse({'error': 'Invalid request method'})

def show_exam_(request,Exam_Name):
    if request.user.is_authenticated:
        Exam_Name_Filter = Question_Choice.objects.filter(Exam_Name=Exam_Name)
        Exam_Time_All = get_object_or_404(TIMER_S, Exam_Name=Exam_Name)

        #Exam_Time_All = TIMER_S.objects.all()
        cnt = Exam_Name_Filter.count()
        context={
            'Exam_Name_Filter':Exam_Name_Filter,
            'cnt':cnt,
            'Exam_Time_All':Exam_Time_All
        }
        return render(request,"testing_and_exam/show_exam_.html",context)
    else:

        return redirect("testing_and_exam:testing_and_exam")

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

@require_POST
# def result_exam(request):
#     try:
#         selected_choices = json.loads(request.POST.get('selectedChoices', '{}'))
        
#         # Burada seçili seçenekleri işleyebilirsiniz
#         # Örneğin, veritabanına kaydedebilir veya başka bir işlem yapabilirsiniz
#         # Aşağıdaki örnekte, sadece seçilen seçenekleri JSON olarak geri döndürüyoruz
#         print("Selected Choices:", selected_choices)
#         return JsonResponse({'success': True, 'selected_choices': selected_choices})
#     except json.JSONDecodeError:
#         return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
def result_exam(request):
    if request.method == 'POST':
        # AJAX isteği ile gönderilen verileri alma
        selected_choices_str = request.POST.get('selectedChoices', '')
        elapsed_time = request.POST.get('elapsed_time')
        print("süreeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",elapsed_time)
        # elapsed_minutes = request.POST.get('elapsedMinutes')
        # elapsed_seconds = request.POST.get('elapsedSeconds')
        # print(f"Elapsed Minutes: {elapsed_minutes}")
        # print(f"Elapsed Seconds: {elapsed_seconds}")


        try:
            # JSON formatındaki veriyi Python dictionary'ye çevirme
            selected_choices = json.loads(selected_choices_str)
            user=request.user
            cevap_yanlis_sayisi = 0
            cevap_dogru_sayisi = 0
            cevap_bos_sayisi = 0
            ders=""
            # Seçenekleri ekrana yazdırma (örnek olarak, konsola yazdırma)
            for question_id, choice in selected_choices.items():
                print(f"Question ID: {question_id}, Selected Choice: {choice}")
                print(question_id,choice)
                _result_=Question_Choice.objects.all()

                #_result_=Question_Choice.objects.filter(id=question_id,Answer_Choice=choice)
                _result_true = _result_.filter(Q(id=question_id) & Q(Answer_Choice=choice))
                _result_false = _result_.filter(Q(id=question_id) & ~Q(Answer_Choice=choice))
                question_choice = Question_Choice.objects.get(id=question_id)
                

                su_an = datetime.now()


                if _result_true.exists():
                    for result in _result_true:
                        print("SSSSSSSSSSSSSSSSSSSSSSSS", result.Answer_Choice)
                        print("Cevap Doğru")
                        _result_save = Exam_Result(
                            author=user,
                            Exam_Name=result.Exam_Name,
                            Question_Id=question_id,
                            Question_Key=result.Answer_Choice,
                            author_Key=choice,
                            True_Answer=1
                        )
                        question_choice.sinavi_cozen_kisi.add(user)
                        question_choice.save()
                        _result_save.save()
                        cevap_dogru_sayisi += 1
                        ders=result.Exam_Name



                else:
                    if choice == "N":
                        for item3 in _result_false:
                            print("Cevap Boş")
                            _result_save3 = Exam_Result(
                                author=user,
                                Exam_Name=item3.Exam_Name,
                                Question_Id=question_id,
                                Question_Key=item3.Answer_Choice,
                                author_Key=choice,
                                True_Answer=2
                            )
                            question_choice.sinavi_cozen_kisi.add(user)
                            question_choice.save()
                            _result_save3.save()
                            cevap_bos_sayisi += 1
                            ders=item3.Exam_Name
                            # Burada question_id'ye göre kaydı bul ve güncelle

                    else:
                        if _result_false.exists():
                            for item2 in _result_false:
                                print("Cevap Yanlış")
                                _result_save2 = Exam_Result(
                                    author=user,
                                    Exam_Name=item2.Exam_Name,
                                    Question_Id=question_id,
                                    Question_Key=item2.Answer_Choice,
                                    author_Key=choice,
                                    True_Answer=0
                                )
                                question_choice.sinavi_cozen_kisi.add(user)

                                _result_save2.save()
                                question_choice.save()
                                cevap_yanlis_sayisi += 1
                                ders=item2.Exam_Name

            print("Cevap Doğru Sayısı:", cevap_dogru_sayisi)
            print("Cevap Yanlış Sayısı:", cevap_yanlis_sayisi)
            print("Cevap Boş Sayısı:", cevap_bos_sayisi)
            _total_ = cevap_bos_sayisi + cevap_dogru_sayisi + cevap_yanlis_sayisi
            exam_table_save=Exam_Table.objects.create(
                author=user,
                Exam_Name=ders,
                Total_Number_Of_Questions=_total_,
                Number_Of_True=cevap_dogru_sayisi,
                Number_Of_False=cevap_yanlis_sayisi,
                Number_Of_Empty=cevap_bos_sayisi,
                Exam_Score=6,
                Exam_Rating=10,
                Completion_Time=elapsed_time,
                #Completion_Time= SINAV BİTİRME SÜRESİ GELECEK
                Exam_Date=su_an,
            )
            exam_table_save.save()
            # Başarılı bir şekilde işlendiğine dair bir JSON yanıt gönderme
            #return redirect('quizorder:index')
            return JsonResponse({'message': 'Veriler başarıyla işlendi.'})
        except json.JSONDecodeError:
            # JSON decode hatası durumunda hata mesajı gönderme
            return JsonResponse({'error': 'Veri çözümlenemedi.'}, status=400)

    # POST isteği değilse veya herhangi bir hata oluşursa boş bir JSON yanıt gönderme
    return JsonResponse({})



def exam_result_show(request):
    if request.user.is_authenticated:
        user=request.user
        #exam_finif = get_object_or_404(Exam_Table, author=user)
        exam_finif = Exam_Table.objects.filter(author=user).order_by('-id')
        cnt=exam_finif.count()


        context ={
            'exam_finif':exam_finif,
            'cnt':cnt
        }
        return render(request,"testing_and_exam/exam_result_show.html",context)
    else:
        return redirect('quizorder:index')




def show_exam_result_details(request, Exam_Name):
    if request.user.is_authenticated:
        user = request.user
        get_questions = Question_Choice.objects.filter(Exam_Name=Exam_Name)
        exam_results_list = []  # Create an empty list to store exam results
        for get_question2 in get_questions:
            exam_results = Exam_Result.objects.filter(author_id=user, Question_Id=get_question2.pk, Exam_Name=get_question2.Exam_Name)
            for exam_rslt2 in exam_results:
                if get_question2.pk == exam_rslt2.Question_Id:
                    print("evet ")
                    exam_results_list.append(exam_rslt2)  # Append each exam result to the list

        context = {
            'exam_results': exam_results_list,
            'get_questions': get_questions,
        }
        
        return render(request, "testing_and_exam/show_exam_result_details.html", context)

    else:
        return redirect('quizorder:index')


#######################################3
    # def show_exam_result_details(request,Exam_Name_Details):
    # if request.user.is_authenticated:
    #     user=request.user
    #     exam_rslt = Exam_Result.objects.filter(Q(author=user)& Q(Exam_Name = Exam_Name_Details))
    #     get_question = Question_Choice.objects.filter(Exam_Name = Exam_Name_Details)
    #     for exam_rslt2 in exam_rslt:
    #         print("Sınav Adı",exam_rslt2.Exam_Name)
    #         print("Soru İd",exam_rslt2.Question_Id)
    #         print("SORUNUN CEVAP ANAHTARI",exam_rslt2.Question_Key)
    #         print("CEVAP VERİLEN ŞIK",exam_rslt2.author_Key)
    #     for get_question2 in get_question:
    #         if get_question2.pk == exam_rslt2.Question_Id:
    #             print("evet",get_question2.pk)
    #         else:
    #             print("hayır",get_question2.pk)
    #     return render(request,"testing_and_exam/show_exam_result_details.html")

 ###########################################   
#SINAV WIEWS ALANI BİTİŞ

#-------------------------------------------------------------------------------------------------------------------------------------------#  
#TYT WIEWS ALANI BAŞLANGIÇ
@login_required
def tyt(request):

    period_choice = {
        '2017': '10 Haziran 2017',
        '2018': '23 Haziran 2018',
        '2019': '15 Haziran 2019',
        '2020': '27 Haziran 2020',
        '2021': '26 Haziran 2021',
        '2022': '18 Haziran 2022',
        '2023': '17 Haziran 2023',
    }
    if request.user.is_authenticated:
        if request.method == 'GET':

            context={
                "period_choice":period_choice
            }
            # Buraya GET isteğiyle ilgili işlemleri yapabilirsiniz
            # Örneğin, belirli bir sayfayı göstermek için bir template render edebilirsiniz
            return render(request, 'testing_and_exam/tyt.html', context)
        elif request.method == 'POST':
            year_ = request.POST.get('year')
            All_Exam = TYT_Choice.objects.filter(Date_Choice=year_)
            


            unique_exam_names = All_Exam.values('EXAM_Name').distinct()
            first_exams_tyt = [All_Exam.filter(EXAM_Name=exam_name['EXAM_Name']).first() for exam_name in unique_exam_names]



            sinavi_goster = False  # Default value

            for cihan in All_Exam:
                users = cihan.tyt_cozen_kisi.all()
                if request.user in users:
                    sinavi_goster = True
                    #print("TESTİ ÇÖZEN KİŞİNİN ID'Sİ=>", request.user.id, "TESTİN ADI:>", cihan.Exam_Name)
                    break  # Exit loop early since we found a match

            cnt = All_Exam.count()

            context={
                "period_choice":period_choice,
                'first_exams_tyt':first_exams_tyt,
                'sinavi_goster':sinavi_goster,
                'cnt':cnt
            }   
            # Desteklenmeyen bir HTTP metodu durumunda buraya düşün
            return render(request, 'testing_and_exam/tyt.html', context)

    else:
        # Kullanıcı kimlik doğrulaması yapılmamışsa, bir hata mesajı veya giriş sayfasına yönlendirme yapabilirsiniz
        return redirect('quizorder:index')

def show_tyt(request, EXAM_Name):
    if request.user.is_authenticated:
        Exam_Name_Filter = TYT_Choice.objects.filter(Date_Choice=EXAM_Name)
        Exam_Time_All = get_object_or_404(TIMER_S_TYT, Date_Choice=EXAM_Name)

        #Exam_Time_All = TIMER_S.objects.all()
        cnt = Exam_Name_Filter.count()
        context={
            'Exam_Name_Filter':Exam_Name_Filter,
            'cnt':cnt,
            'Exam_Time_All':Exam_Time_All
        }
        return render(request,"testing_and_exam/show_tyt.html",context)
    else:

        return redirect("testing_and_exam:testing_and_exam")
    

def tyt_result_show(request):
    if request.user.is_authenticated:
        user=request.user
        #exam_finif = get_object_or_404(Exam_Table, author=user)
        exam_finif = TYT_Table.objects.filter(author=user).order_by('-id')
        cnt=exam_finif.count()


        context ={
            'exam_finif':exam_finif,
            'cnt':cnt
        }
        return render(request,"testing_and_exam/tyt_result_show.html",context)
    else:
        return redirect('quizorder:index')



def result_tyt(request):
    if request.method == 'POST':
        # AJAX isteği ile gönderilen verileri alma
        selected_choices_str = request.POST.get('selectedChoices', '')
        elapsed_time = request.POST.get('elapsed_time')
        print("süreeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",elapsed_time)
        # elapsed_minutes = request.POST.get('elapsedMinutes')
        # elapsed_seconds = request.POST.get('elapsedSeconds')
        # print(f"Elapsed Minutes: {elapsed_minutes}")
        # print(f"Elapsed Seconds: {elapsed_seconds}")


        try:
            # JSON formatındaki veriyi Python dictionary'ye çevirme
            selected_choices = json.loads(selected_choices_str)
            user=request.user
            cevap_yanlis_sayisi = 0
            cevap_dogru_sayisi = 0
            cevap_bos_sayisi = 0
            ders=""
            # Seçenekleri ekrana yazdırma (örnek olarak, konsola yazdırma)
            for question_id, choice in selected_choices.items():
                print(f"Question ID: {question_id}, Selected Choice: {choice}")
                print(question_id,choice)
                _result_=TYT_Choice.objects.all()

                #_result_=Question_Choice.objects.filter(id=question_id,Answer_Choice=choice)
                _result_true = _result_.filter(Q(id=question_id) & Q(Answer_Choice=choice))
                _result_false = _result_.filter(Q(id=question_id) & ~Q(Answer_Choice=choice))
                
                question_choice = TYT_Choice.objects.get(id=question_id)

                su_an = datetime.now()


                if _result_true.exists():
                    for result in _result_true:
                        print("SSSSSSSSSSSSSSSSSSSSSSSS", result.Answer_Choice)
                        print("Cevap Doğru")
                        _result_save = TYT_Result(
                            author=user,
                            Date_Choice=result.EXAM_Name,
                            Question_Id=question_id,
                            Question_Key=result.Answer_Choice,
                            author_Key=choice,
                            True_Answer=1
                        )
                        question_choice.tyt_cozen_kisi.add(user)
                        question_choice.save()
                        
                        _result_save.save()
                        cevap_dogru_sayisi += 1
                        ders=result.EXAM_Name
                else:
                    if choice == "N":
                        for item3 in _result_false:
                            print("Cevap Boş")
                            _result_save3 = TYT_Result(
                                author=user,
                                Date_Choice=item3.EXAM_Name,
                                Question_Id=question_id,
                                Question_Key=item3.Answer_Choice,
                                author_Key=choice,
                                True_Answer=2
                            )
                            question_choice.tyt_cozen_kisi.add(user)
                            question_choice.save()
                            _result_save3.save()
                            cevap_bos_sayisi += 1
                            ders=item3.EXAM_Name
                    else:
                        if _result_false.exists():
                            for item2 in _result_false:
                                print("Cevap Yanlış")
                                _result_save2 = TYT_Result(
                                    author=user,
                                    Date_Choice=item2.EXAM_Name,
                                    Question_Id=question_id,
                                    Question_Key=item2.Answer_Choice,
                                    author_Key=choice,
                                    True_Answer=0
                                )
                                question_choice.tyt_cozen_kisi.add(user)
                                question_choice.save()
                                _result_save2.save()
                                cevap_yanlis_sayisi += 1
                                ders=item2.EXAM_Name

            print("Cevap Doğru Sayısı:", cevap_dogru_sayisi)
            print("Cevap Yanlış Sayısı:", cevap_yanlis_sayisi)
            print("Cevap Boş Sayısı:", cevap_bos_sayisi)
            _total_ = cevap_bos_sayisi + cevap_dogru_sayisi + cevap_yanlis_sayisi
            exam_table_save=TYT_Table.objects.create(
                author=user,
                Date_Choice=ders,
                Total_Number_Of_Questions=_total_,
                Number_Of_True=cevap_dogru_sayisi,
                Number_Of_False=cevap_yanlis_sayisi,
                Number_Of_Empty=cevap_bos_sayisi,
                Exam_Score=6,
                Exam_Rating=10,
                Completion_Time=elapsed_time,
                #Completion_Time= SINAV BİTİRME SÜRESİ GELECEK
                Exam_Date=su_an,
            )
            exam_table_save.save()
            # Başarılı bir şekilde işlendiğine dair bir JSON yanıt gönderme
            #return redirect('quizorder:index')
            return JsonResponse({'message': 'Veriler başarıyla işlendi.'})
        except json.JSONDecodeError:
            # JSON decode hatası durumunda hata mesajı gönderme
            return JsonResponse({'error': 'Veri çözümlenemedi.'}, status=400)

    # POST isteği değilse veya herhangi bir hata oluşursa boş bir JSON yanıt gönderme
    return JsonResponse({})


def show_tyt_result_details(request,Date_Choice):
    if request.user.is_authenticated:
        user = request.user
        get_questions = TYT_Choice.objects.filter(EXAM_Name=Date_Choice)
        exam_results_list = []  # Create an empty list to store exam results
        for get_question2 in get_questions:
            exam_results = TYT_Result.objects.filter(author_id=user, Question_Id=get_question2.pk, Date_Choice=get_question2.EXAM_Name)
            for exam_rslt2 in exam_results:
                if get_question2.pk == exam_rslt2.Question_Id:
                    print("evet ")
                    exam_results_list.append(exam_rslt2)  # Append each exam result to the list

        context = {
            'exam_results': exam_results_list,
            'get_questions': get_questions,
        }
        
        return render(request, "testing_and_exam/show_tyt_result_details.html", context)

    else:
        return redirect('quizorder:index')

#-------------------------------------------------------------------------------------------------------------------------------------------#  
#TYT WIEWS ALANI BİTİŞ
#-------------------------------------------------------------------------------------------------------------------------------------------#  
#AYT WIEWS ALANI BAŞLANGIÇ
@login_required
def ayt(request):
    period_choice = {
        '2017': '11 Haziran 2017',
        '2018': '24 Haziran 2018',
        '2019': '16 Haziran 2019',
        '2020': '28 Haziran 2020',
        '2021': '27 Haziran 2021',
        '2022': '19 Haziran 2022',
        '2023': '18 Haziran 2023',
    }
    if request.user.is_authenticated:
        if request.method == 'GET':

            context={
                "period_choice":period_choice
            }
            # Buraya GET isteğiyle ilgili işlemleri yapabilirsiniz
            # Örneğin, belirli bir sayfayı göstermek için bir template render edebilirsiniz
            return render(request, 'testing_and_exam/ayt.html', context)
        elif request.method == 'POST':
            year_ = request.POST.get('year')
            All_Exam = AYT_Choice.objects.filter(Date_Choice=year_)


            unique_exam_names = All_Exam.values('EXAM_Name').distinct()
            first_exams_ayt = [All_Exam.filter(EXAM_Name=exam_name['EXAM_Name']).first() for exam_name in unique_exam_names]

            sinavi_goster = False

            for cihan in All_Exam:
                users = cihan.ayt_cozen_kisi.all()
                if request.user in users:
                    sinavi_goster = True
                    #print("TESTİ ÇÖZEN KİŞİNİN ID'Sİ=>", request.user.id, "TESTİN ADI:>", cihan.Exam_Name)
                    break  # Exit loop early since we found a match


            cnt = All_Exam.count()
            for getir in All_Exam:
                print(getir.Question)
            context={
                "period_choice":period_choice,
                'first_exams_ayt':first_exams_ayt,
                'sinavi_goster':sinavi_goster,
                'cnt':cnt
            }   
            # Desteklenmeyen bir HTTP metodu durumunda buraya düşün
            return render(request, 'testing_and_exam/ayt.html', context)

    else:
        # Kullanıcı kimlik doğrulaması yapılmamışsa, bir hata mesajı veya giriş sayfasına yönlendirme yapabilirsiniz
        return redirect('quizorder:index')
    return render(request,"testing_and_exam/ayt.html")


def ayt_show(request, EXAM_Name):
    if request.user.is_authenticated:
        Exam_Name_Filter = AYT_Choice.objects.filter(Date_Choice=EXAM_Name)
        Exam_Time_All = get_object_or_404(AYT_TIMER_S, Date_Choice=EXAM_Name)

        #Exam_Time_All = TIMER_S.objects.all()
        cnt = Exam_Name_Filter.count()
        context={
            'Exam_Name_Filter':Exam_Name_Filter,
            'cnt':cnt,
            'Exam_Time_All':Exam_Time_All
        }
        return render(request,"testing_and_exam/ayt_show.html",context)
    else:

        return redirect("testing_and_exam:testing_and_exam")
    



def ayt_result_show(request):
    if request.user.is_authenticated:
        user=request.user
        #exam_finif = get_object_or_404(Exam_Table, author=user)
        exam_finif = AYT_Table.objects.filter(author=user).order_by('-id')
        cnt=exam_finif.count()


        context ={
            'exam_finif':exam_finif,
            'cnt':cnt
        }
        return render(request,"testing_and_exam/ayt_result_show.html",context)
    else:
        return redirect('quizorder:index')
    


def ayt_result(request):
    if request.method == 'POST':
        # AJAX isteği ile gönderilen verileri alma
        selected_choices_str = request.POST.get('selectedChoices', '')
        elapsed_time = request.POST.get('elapsed_time')
        print("süreeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",elapsed_time)
        # elapsed_minutes = request.POST.get('elapsedMinutes')
        # elapsed_seconds = request.POST.get('elapsedSeconds')
        # print(f"Elapsed Minutes: {elapsed_minutes}")
        # print(f"Elapsed Seconds: {elapsed_seconds}")


        try:
            # JSON formatındaki veriyi Python dictionary'ye çevirme
            selected_choices = json.loads(selected_choices_str)
            user=request.user
            cevap_yanlis_sayisi = 0
            cevap_dogru_sayisi = 0
            cevap_bos_sayisi = 0
            ders=""
            # Seçenekleri ekrana yazdırma (örnek olarak, konsola yazdırma)
            for question_id, choice in selected_choices.items():
                print(f"Question ID: {question_id}, Selected Choice: {choice}")
                print(question_id,choice)
                _result_=AYT_Choice.objects.all()

                #_result_=Question_Choice.objects.filter(id=question_id,Answer_Choice=choice)
                _result_true = _result_.filter(Q(id=question_id) & Q(Answer_Choice=choice))
                _result_false = _result_.filter(Q(id=question_id) & ~Q(Answer_Choice=choice))
                question_choice = AYT_Choice.objects.get(id=question_id)
                

                su_an = datetime.now()


                if _result_true.exists():
                    for result in _result_true:
                        print("SSSSSSSSSSSSSSSSSSSSSSSS", result.Answer_Choice)
                        print("Cevap Doğru")
                        _result_save = AYT_Result(
                            author=user,
                            Date_Choice=result.EXAM_Name,
                            Question_Id=question_id,
                            Question_Key=result.Answer_Choice,
                            author_Key=choice,
                            True_Answer=1
                        )

                        question_choice.ayt_cozen_kisi.add(user)
                        question_choice.save()
                        _result_save.save()
                        cevap_dogru_sayisi += 1
                        ders=result.EXAM_Name
                else:
                    if choice == "N":
                        for item3 in _result_false:
                            print("Cevap Boş")
                            _result_save3 = AYT_Result(
                                author=user,
                                Date_Choice=item3.EXAM_Name,
                                Question_Id=question_id,
                                Question_Key=item3.Answer_Choice,
                                author_Key=choice,
                                True_Answer=2
                            )
                            question_choice.ayt_cozen_kisi.add(user)
                            question_choice.save()
                            _result_save3.save()
                            cevap_bos_sayisi += 1
                            ders=item3.EXAM_Name
                    else:
                        if _result_false.exists():
                            for item2 in _result_false:
                                print("Cevap Yanlış")
                                _result_save2 = AYT_Result(
                                    author=user,
                                    Date_Choice=item2.EXAM_Name,
                                    Question_Id=question_id,
                                    Question_Key=item2.Answer_Choice,
                                    author_Key=choice,
                                    True_Answer=0
                                )
                                question_choice.ayt_cozen_kisi.add(user)
                                question_choice.save()
                                _result_save2.save()
                                cevap_yanlis_sayisi += 1
                                ders=item2.EXAM_Name

            print("Cevap Doğru Sayısı:", cevap_dogru_sayisi)
            print("Cevap Yanlış Sayısı:", cevap_yanlis_sayisi)
            print("Cevap Boş Sayısı:", cevap_bos_sayisi)
            _total_ = cevap_bos_sayisi + cevap_dogru_sayisi + cevap_yanlis_sayisi
            exam_table_save=AYT_Table.objects.create(
                author=user,
                Date_Choice=ders,
                Total_Number_Of_Questions=_total_,
                Number_Of_True=cevap_dogru_sayisi,
                Number_Of_False=cevap_yanlis_sayisi,
                Number_Of_Empty=cevap_bos_sayisi,
                Exam_Score=6,
                Exam_Rating=10,
                Completion_Time=elapsed_time,
                #Completion_Time= SINAV BİTİRME SÜRESİ GELECEK
                Exam_Date=su_an,
            )
            exam_table_save.save()
            # Başarılı bir şekilde işlendiğine dair bir JSON yanıt gönderme
            #return redirect('quizorder:index')
            return JsonResponse({'message': 'Veriler başarıyla işlendi.'})
        except json.JSONDecodeError:
            # JSON decode hatası durumunda hata mesajı gönderme
            return JsonResponse({'error': 'Veri çözümlenemedi.'}, status=400)

    # POST isteği değilse veya herhangi bir hata oluşursa boş bir JSON yanıt gönderme
    return JsonResponse({})




def ayt_show_result_details(request,Date_Choice):
    if request.user.is_authenticated:
        user = request.user
        get_questions = AYT_Choice.objects.filter(EXAM_Name=Date_Choice)
        exam_results_list = []  # Create an empty list to store exam results
        for get_question2 in get_questions:
            exam_results = AYT_Result.objects.filter(author_id=user, Question_Id=get_question2.pk, Date_Choice=get_question2.EXAM_Name)
            for exam_rslt2 in exam_results:
                if get_question2.pk == exam_rslt2.Question_Id:
                    print("evet ")
                    exam_results_list.append(exam_rslt2)  # Append each exam result to the list

        context = {
            'exam_results': exam_results_list,
            'get_questions': get_questions,
        }
        
        return render(request, "testing_and_exam/ayt_show_result_details.html", context)

    else:
        return redirect('quizorder:index')




#-------------------------------------------------------------------------------------------------------------------------------------------#  
#AYT WIEWS ALANI BİTİŞ




#---------------------------------İSTATİSTİK ALANI BAŞLANGIÇ-------------------------------------------------------------------------------#
def show_exam_istatistic(request):
    if request.method == 'POST':
        exam_name = request.POST.get('Exam_Name')  # Get the Exam_Name from POST data
        if exam_name:
            All_Exam_Table = Exam_Table.objects.filter(Exam_Name=exam_name)
            if All_Exam_Table.exists():
                all_exam_table_ = All_Exam_Table.first()  # Assuming there's only one object with the given Exam_Name
                exam_rating = (int(all_exam_table_.Number_Of_True) - int(all_exam_table_.Number_Of_False) - 0.5 * int(all_exam_table_.Number_Of_Empty)) + 0.5 * float(all_exam_table_.Exam_Rating)
                return JsonResponse({'exam_rating': exam_rating})
            else:
                return JsonResponse({'error': 'Sınav bulunamadı.'})
        else:
            return JsonResponse({'error': 'Sınav Adı parametresi eksik.'})
    else:
        return JsonResponse({'error': 'Geçersiz istek yöntemi.'})
    


def show_testing_istatistic(request):
    if request.method == 'POST':
        Testing_Name = request.POST.get('Testing_Name')  # Get the Exam_Name from POST data
        if Testing_Name:
            All_Test_Table = Testing_Table.objects.filter(Testing_Name=Testing_Name)
            if All_Test_Table.exists():
                all_exam_table_ = All_Test_Table.first()  # Assuming there's only one object with the given Exam_Name
                exam_rating = (int(all_exam_table_.Number_Of_True) - int(all_exam_table_.Number_Of_False) - 0.5 * int(all_exam_table_.Number_Of_Empty)) + 0.5 * float(all_exam_table_.Testing_Rating)
                return JsonResponse({'exam_rating': exam_rating})
            else:
                return JsonResponse({'error': 'Sınav bulunamadı.'})
        else:
            return JsonResponse({'error': 'Sınav Adı parametresi eksik.'})
    else:
        return JsonResponse({'error': 'Geçersiz istek yöntemi.'})
    



def show_tyt_istatistic(request):
    if request.method == 'POST':
        Date_Choice = request.POST.get('Date_Choice')  # Get the Exam_Name from POST data
        if Date_Choice:
            All_Test_Table = TYT_Table.objects.filter(Date_Choice=Date_Choice)
            if All_Test_Table.exists():
                all_exam_table_ = All_Test_Table.first()  # Assuming there's only one object with the given Exam_Name
                exam_rating = (int(all_exam_table_.Number_Of_True) - int(all_exam_table_.Number_Of_False) - 0.5 * int(all_exam_table_.Number_Of_Empty)) + 0.5 * float(all_exam_table_.Exam_Rating)
                return JsonResponse({'exam_rating': exam_rating})
            else:
                return JsonResponse({'error': 'Sınav bulunamadı.'})
        else:
            return JsonResponse({'error': 'Sınav Adı parametresi eksik.'})
    else:
        return JsonResponse({'error': 'Geçersiz istek yöntemi.'})





def show_ayt_istatistic(request):
    if request.method == 'POST':
        Date_Choice = request.POST.get('Date_Choice')
        if Date_Choice:
            All_Test_Table = AYT_Table.objects.filter(Date_Choice=Date_Choice)
            if All_Test_Table.exists():
                all_exam_table_ = All_Test_Table.first()
                exam_rating = (int(all_exam_table_.Number_Of_True) - int(all_exam_table_.Number_Of_False) - 0.5 * int(all_exam_table_.Number_Of_Empty)) + 0.5 * float(all_exam_table_.Exam_Rating)
                return JsonResponse({'exam_rating': exam_rating})
            else:
                return JsonResponse({'error': 'Sınav bulunamadı.'}, status=404) # 404 hatası
        else:
            return JsonResponse({'error': 'Sınav Adı parametresi eksik.'}, status=400) # 400 hatası
    else:
        return JsonResponse({'error': 'Geçersiz istek yöntemi.'}, status=405) # 405 hatası






#-------------------------------------------------------------------------------------------------------------------------------------------#  
#KPSS WIEWS ALANI BAŞLANGIÇ



#def kpss(request):
    #return render(request,"testing_and_exam/kpss.html")
#-------------------------------------------------------------------------------------------------------------------------------------------#  
#KPSS WIEWS ALANI BİTİŞ
from doctest import Example
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart, CartExamTitle
from django.http import HttpResponse, JsonResponse
from exam.models import Exam
from question.models import Question
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from user.models import Profile

# Create your views here.
def cart_add(request):
    user = get_object_or_404(Profile, author_id=request.user.id)
     
    if request.user.is_authenticated:
        if user.user_types =="Teacher":
            if request.method == 'POST':
                exam_item_id = request.POST.get('user_id')
                Question_Image = request.FILES.get('Question_Image')

                # Assuming the user is logged in
                print("Exam item ID:", exam_item_id)
                product = get_object_or_404(Question, id=exam_item_id)
                # Create a new cart item
                kaydet = Cart.objects.create(
                author=request.user, 
                exam_items=exam_item_id,
                Lessons=product.Lessons,
                Question=product.Question,
                Answer=product.Answer,
                Classroom=product.Classroom,
                Topics_Name=product.Topics_Name,
                Question_Types=product.Question_Types,
                Level=product.Level,
                Question_Image=product.Question_Image,
                Choice_A =product.Choice_A,
                Choice_B =product.Choice_B,
                Choice_C =product.Choice_C,
                Choice_D =product.Choice_D,
                Choice_E =product.Choice_E,
                )
                kaydet.save()
                return JsonResponse({'success': product.Lessons,'Topics_Name': product.Topics_Name,'Level': product.Level})
            return JsonResponse({'success': False})
        else:
            redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)

# def cart_show(request):
#     cart_shows = Cart.objects.filter(author=request.user).order_by('-created_date')
#     exam_title=CartExamTitle.objects.filter(author=request.user).order_by('-created_date')
#     context={
#         'cart_shows':cart_shows,
#         'exam_title':exam_title
#     }
#     return render(request, 'cart/cart_show.html',context)


def cart_exam_show(request):
    user = get_object_or_404(Profile, author_id=request.user.id)
     
    if request.user.is_authenticated:
        if user.user_types =="Teacher":
    #exam_show = Exam.objects.values('Exam_Title','Topics_Name','id').filter(author=request.user)
    # exam_show = Exam.objects.filter(author=request.user).values('Exam_Title').distinct()
            from django.db.models import Max
            #exam_show = Exam.objects.values('Exam_Title','Topics_Name','id').filter(author=request.user)
            exam_show = Exam.objects.filter(author=request.user).values('Exam_Title').annotate(max_created_date=Max('Created_Date'))
            cnt = exam_show.count()
            context={
                'exam_show':exam_show,
                'cnt':cnt
            }
            return render(request,"cart/exam_show.html",context)
        else:
            redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)

# def exam_edit(request,edit_):
#     print(edit_)
#     edit = Exam.objects.filter(Q(author=request.user) & Q(Exam_Title=edit_))
#     # for edi in edit:
#     #     print("Sınav => ",edi.Question,"Cevap =>",edi.Answer)
#     context={
#         'edit':edit
#     }
#     return render(request,"exam/exam_edit.html",context)


edit_value = None  # Daha yüksek bir kapsamda tanımlanıyor

def exam_edit(request, edit_):
    user = get_object_or_404(Profile, author_id=request.user.id)
     
    if request.user.is_authenticated:
        if user.user_types =="Teacher":

            print(edit_)
            global edit_value  # `edit_` değerini ekrana yazdırın
            edit_value = edit_  # İstenen değeri `edit_degeri` değişkenine atayın
            print("yeni", edit_value)
            edit = Exam.objects.filter(Q(author=request.user) & Q(Exam_Title=edit_))
            context = {
                'edit': edit
            }
            return render(request, "exam/exam_edit.html", context)


        else:
            redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)





def exam_edit_delete(request, id):
    user = get_object_or_404(Profile, author_id=request.user.id)
     
    if request.user.is_authenticated:
        if user.user_types =="Teacher":
            global edit_value  # Daha yüksek kapsamdaki `edit_degeri`'yi kullanın
            print("yeni", edit_value)
            edit_delete = Exam.objects.filter(Q(author=request.user) & Q(Exam_Title=edit_value)& Q(Question_ID=id))
            if edit_delete.exists():
                edit_delete.delete()
                messages.success(request, "Soru silme işlemi başarılı bir şekilde gerçekleştirildi")
            else:
                messages.error(request, "Soru silinemedi.")

            #return render(request, "exam/exam_edit.html")
            return redirect("cart:exam_edit",edit_value)
        else:
            redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)




def exam_delete(request, delete):
    user = get_object_or_404(Profile, author_id=request.user.id)
     
    if request.user.is_authenticated:
        if user.user_types =="Teacher":
            edit_delet = Exam.objects.filter(Q(author=request.user) & Q(Exam_Title=delete))
            if edit_delet.exists():
                edit_delet.delete()
                messages.success(request, "Soru silme işlemi başarılı bir şekilde gerçekleştirildi")
            else:
                messages.error(request, "Soru silinemedi.")

            #return render(request, "exam/exam_edit.html")
            return redirect("cart:cart_exam_show")

        else:
            redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)


def exam_pdf(request,e_title):
    user = get_object_or_404(Profile, author_id=request.user.id)
     
    if request.user.is_authenticated:
        if user.user_types =="Teacher":
            pdf = Exam.objects.filter(Q(author=request.user) & Q(Exam_Title=e_title))
            
            
            context={
                'pdf':pdf,

                
            }
            return render(request,"exam/exam_pdf.html",context)

        else:
            redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
            # Yönlendirme yapın
            return HttpResponseRedirect(redirect_url)
    else:
        redirect_url = reverse('quizorder:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)
from django.shortcuts import render
#from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage  
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from .tokens import account_activation_token  
from .forms import *
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string  
from question.models import Question
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from.models import Profile
from.views import *
from .forms import *
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def User_Register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()  # Save the user first to generate the user ID

            new_user_profile = Profile.objects.create(
                author=user,  # Set the author to the newly created user
                # Add other fields for Profile if needed
            )
            
            new_user_profile.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Aktivasyon bağlantısı e-posta kimliğinize gönderildi'
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'user/Email.html', {'msg': 'Kaydı tamamlamak için lütfen e-posta adresinizi doğrulayın'})
    else:
        form = SignupForm()
    return render(request, 'user/register.html', {'form': form, 'title': 'kayıt ol!'})




def User_Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user:User_Profil',request.user.id)
        else:
            messages.error(request, 'Geçersiz giriş, lütfen kullanıcı adı ve şifreyi kontrol edin.')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})




def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True
        user.save()  
        return render(request,'user/Email.html',{'msg':'E-posta onayınız için teşekkür ederiz. Artık hesabınıza giriş yapabilirsiniz.'})  
    else:  
        return render(request, 'user/Email.html',{'msg':'Etkinleştirme bağlantısı geçersiz!'})  


def User_Logout(request):
    logout (request)
    return redirect("quizbox:index")





@login_required
def user_subscribe_edit(request,pk):
    # Kullanıcıyı çekiyoruz
    user_subscribe = get_object_or_404(UserSubscribeEdit, author=pk)
    
    if request.method == 'POST':
        # Formdan gelen verileri kaydetme
        subscriber_one = request.POST.get('subscriber1')
        subscriber_two = request.POST.get('subscriber2')
        subscriber_three = request.POST.get('subscriber3')
        subscriber_four = request.POST.get('subscriber4')

        # Veritabanında güncelleme yapıyoruz
        user_subscribe.subscriber_one = subscriber_one
        user_subscribe.subscriber_two = subscriber_two
        user_subscribe.subscriber_three = subscriber_three
        user_subscribe.subscriber_four = subscriber_four
        user_subscribe.save()

        # Başarılı kaydetme sonrası bir sayfaya yönlendirme yapabilirsiniz
        return redirect('user:User_Profil', pk=pk)  # Yönlendirilmek istenen sayfanın url name'ini buraya yazın

    # GET isteğinde verileri template'e gönderiyoruz
    context = {
        'user_profil_UserSubscribeEdit': [user_subscribe]
    }
    
    return render(request, 'user/login.html', context)













def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Parola Sıfırlama İsteği"
                email_template_name = "user/password_reset_email.html"
                c = {
                    "email": user.email,
                    "domain": request.META["HTTP_HOST"],
                    "site_name": "Siteniz",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, "quizkutusu.com", [user.email], fail_silently=False)
            return HttpResponse('E-posta ile parola sıfırlama bağlantısı gönderildi.')
        else:
            return HttpResponse('Bu e-posta adresiyle ilişkili bir hesap bulunamadı.')
    return render(request, "user/password_reset_form.html")

from django.utils.encoding import force_str

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomPasswordChangeForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                # Kullanıcının oturumunu güncelleyin
                update_session_auth_hash(request, user)
                return HttpResponse("Parola başarıyla değiştirildi. Tekrardan giriş yapınız.")
                

        else:
            form = CustomPasswordChangeForm(user)
        return render(request, 'user/password_change_form.html', {'form': form})
    else:
        return HttpResponse("Geçersiz parola sıfırlama bağlantısı!")



@login_required
def User_Profil(request, pk):
    # GET işlemi için kullanıcı profilini görüntüleme
    user_profil_UserSubscribeEdit = UserSubscribeEdit.objects.filter(author=pk)

    if request.method == 'GET':
        # 'id' parametresi, kullanıcı profilini görüntülemek istediğiniz kullanıcının benzersiz kimliğini temsil eder.
        # Bu kimliği kullanarak veritabanından ilgili kullanıcıyı almanız gerekiyor.
        user_profile = get_object_or_404(Profile, author_id=pk)
        distinct_topics = Question.objects.filter(author_id=pk).values('Topics_Name').annotate(count=Count('Topics_Name'))

        print("----------------------------------------",user_profile.user_types)


        user_post=Question.objects.filter(author_id=pk)

        for post in user_post:
            # Author'ın avatar fotoğrafını al
            author_avatar = None
            author_profile = Profile.objects.filter(author=post.author).first()  # Author'a ait Profile nesnesini al
            if author_profile:
                post.author_avatar_url = author_profile.avatars.url if author_profile.avatars else None

        topic_count = user_post.values('Topics_Name').distinct().count()
        user_post_count=user_post.count()
        user_followers_count=user_profile.followers.count()
        user_following_count=user_profile.following.count()
        for user in user_post:
            print(user,"nabersssssssssssss")

        return render(request, "user/profil.html", {
            'user_profile': user_profile,
            'topics_count':distinct_topics,
            'topic_count': topic_count,
            'user_post':user_post,
            'user_post_count':user_post_count,
            'user_followers_count':user_followers_count,
            'user_following_count':user_following_count,
            'user_profil_UserSubscribeEdit':user_profil_UserSubscribeEdit

        })

    # POST işlemi için kullanıcı profilini güncelleme
    elif request.method == 'POST':

        yeni_veri = request.POST.get('yeni_veri')
        

        # Veritabanında kullanıcı profilini güncelle (örneğin, yeni_veri ile)
        user_profile = get_object_or_404(Profile, author_id=pk)
        user_profile.field_name = yeni_veri  # field_name, güncellenmesi gereken alan adını temsil eder
        user_profile.save()

        # Kullanıcıyı başka bir sayfaya yönlendir
        return redirect('başka_bir_sayfa_url')

    else:
        # Yanlış bir istek metodu gönderildiğinde buraya düşer
        return HttpResponseNotAllowed(['GET', 'POST'])  # Doğru HTTP yöntemlerini belirtin





from django.http import Http404

def User_Info_Update(request, pk):
    try:
        user = Profile.objects.filter(author_id=pk).first()

        if not user:
            raise Http404

        form = User_Update_Forms(request.POST or None, instance=user, files=request.FILES)

        if request.method == 'POST':
            if form.is_valid():
                update = form.save(commit=False)
                update.author = request.user

                if 'avatars' in request.FILES:
                    update.avatars = request.FILES['avatars']

                if 'biographys' in request.POST:
                    update.biographys = request.POST['biographys']

                # if 'mail_adress' in request.POST:
                #     update.mail_adress = request.POST['mail_adress']

                if 'mobile_phone' in request.POST:
                    update.mobile_phone = request.POST['mobile_phone']

                if 'social_media_facebook' in request.POST:
                    update.social_media_facebook = request.POST['social_media_facebook']

                if 'social_media_twitter' in request.POST:
                    update.social_media_twitter = request.POST['social_media_twitter']

                if 'social_media_instagram' in request.POST:
                    update.social_media_instagram = request.POST['social_media_instagram']

                if 'social_media_tiktok' in request.POST:
                    update.social_media_tiktok = request.POST['social_media_tiktok']

                update.save()

                return redirect('user:User_Profil', pk=pk)
        else:
            form = User_Update_Forms(instance=user)

        return render(request, 'user/profil.html', {'user': user, 'form': form})
        
    except Http404:
        return render(request, '404.html')  # Özel bir 404 sayfasına yönlendirme yapılabilir




def teacher_profiles(request):
    #user_profile=Profile.objects.filter(Q(id = user_id) & Q(user_types = 'Manager') & Q(schools = school))

    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, author_id=request.user)
        print(user_profile.user_types)
        all_profiles =[]
        for schools in user_profile.schools.all():
            school = schools  # Burada school_name, School modelindeki ilgili alan adı olmalıdır.
            print("okul adı======================", school)
            user_profile2=Profile.objects.filter(Q(author_id = request.user) & Q(user_types = 'Teacher') & Q(schools = school))
            if user_profile2:
              #  all_profiles = Profile.objects.filter(schools=school)
                all_profiles = Profile.objects.filter(~Q(author_id=request.user) & Q(schools=school)  )

                print("--------------YEAPS")
            else:
                print('malesef')
                return redirect("quizbox:index")

        #filtere_profiles = Profile.objects.filter(Q(id=user_id) & Q(user_types='Manager')  )
        return render(request, "user/teacher_profiles.html", {
            'user_profile': user_profile,
            'school':school,
            'all_profiles':all_profiles,
            })
    else:
        redirect_url = reverse('quizbox:index')  # 'hata_sayfasi' isimli URL'nin adını projenize göre değiştirin
        # Yönlendirme yapın
        return HttpResponseRedirect(redirect_url)





def User_Logout(request):
    logout (request)
    return redirect("quizbox:index")





def followView(request):
    user_id = request.POST.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Kullanıcı kimliği gerekli.'}, status=400)

    target_user = get_object_or_404(User, id=user_id)
    target_profile = get_object_or_404(Profile, author_id=user_id)
    request_profile = get_object_or_404(Profile, author_id=request.user.id)

    if target_profile.followers.filter(id=request.user.id).exists():
        target_profile.followers.remove(request.user)
        request_profile.following.remove(target_user)
        followed = False
    else:
        target_profile.followers.add(request.user)
        request_profile.following.add(target_user)
        followed = True

    followers_count = target_profile.followers.count()
    following_count = target_profile.following.count()

    return JsonResponse({
        'followed': followed,
        'followers_count': followers_count,
        'following_count': following_count
    })




from django.http import HttpResponseRedirect
from django.urls import reverse

def profile_question_delete(request, pk):
    edit_delete = Question.objects.filter(author=request.user, pk=pk)
    
    if edit_delete.exists():
        edit_delete.delete()
        messages.success(request, "Soru silme işlemi başarılı bir şekilde gerçekleştirildi")
    else:
        messages.error(request, "Soru silinemedi.")

    return redirect("quizbox:index")



def student_works(request):
    return render(request, 'user/student_works.html')
    
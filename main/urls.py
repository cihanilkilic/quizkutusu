from django.contrib import admin
from django.urls import path, include 
from django.conf import settings #add this
from django.conf.urls.static import static #add this
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quizbox.urls')),
    path('user/', include("user.urls")),    
    path('question/', include("question.urls")),    
    path('cart/', include("cart.urls")),
    path('testing_and_exam/', include("testing_and_exam.urls")),
    path('forum/', include("forum.urls")),
    path("chat/", include("chat.urls"))

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from apps.account.views import *
from apps.book.views import *



router = DefaultRouter()
# 书籍url
router.register('book', BookViewSet, basename='book')

# 借阅
router.register('borrow', BorrowViewSet, basename='borrow')

#出版社
router.register('press', PressViewSet, basename='press')
#书籍类别
router.register('category', BookCategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    url(r'media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),


    path('api/', include(router.urls)),
    path('login', LoginView.as_view()),
    # path('logout/', LogoutView.as_view()),
    path('refresh_token/', MyTokenRefreshView.as_view()),
    path('register', RegisterViewSet.as_view({'post': 'create'})),
    # path('check_account/', UsernameCountView.as_view()),
    # path('check_tel/', TelephoneCountView.as_view()),
    # path('images/', ImagesViewSet.as_view())
]


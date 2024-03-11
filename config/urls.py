from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from apps.account.views import *
from apps.book.views import *
from apps.image.views import ClubSwiperViewSet
from utils.function import UploadViewSet
from apps.notice.views import NoticetViewSet
from apps.school.views import FacultyViewSet,MajorViewSet
from apps.message.views import BookMessageThemeViewSet,CommentViewSet,MpttCommentViewSet
from apps.reservation.views import SeatViewSet,ReservationViewSet


router = DefaultRouter()
# 书籍url
router.register('book', BookViewSet, basename='book')

# 借阅
router.register('borrow', BorrowViewSet, basename='borrow')

#出版社
router.register('press', PressViewSet, basename='press')
#书籍一级类别
router.register('category', BookRootCategoryViewSet, basename='category')

# 首页轮播图
router.register('swiper', ClubSwiperViewSet, basename='swiper')

# 通知接口
router.register('notice', NoticetViewSet, basename='swiper')

#上传图片接口
# 富文本图片上传url
router.register('upload', viewset=UploadViewSet, basename='upload')

# 用户信息接口
router.register('account', viewset=AccountViewSet, basename='account')

#图书收藏接口
router.register('collection', viewset=BookCollectionViewSet, basename='collection')

#学院、班级接口
router.register('faculty', viewset=FacultyViewSet, basename='faculty')
router.register('major', viewset=MajorViewSet, basename='major')

#留言相关接口
router.register('message', viewset=BookMessageThemeViewSet, basename='message')
#留言评论相关接口
router.register('comment', viewset=CommentViewSet, basename='comment')
router.register('mptt_comment', viewset=MpttCommentViewSet, basename='mpttcomment')

#座位预约相关接口
#留言评论相关接口
router.register('seat', viewset=SeatViewSet, basename='seat')
router.register('reservation', viewset=ReservationViewSet, basename='reservation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    url(r'media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    path('mini_login/', WechatLoginView.as_view()),
    path('mptt_comment/', MpttCommentViewSet.as_view({
        'post': 'create'
    })),
    path('api/', include(router.urls)),
    path('login', LoginView.as_view()),
    # path('logout/', LogoutView.as_view()),
    path('refresh_token/', MyTokenRefreshView.as_view()),
    path('register', RegisterViewSet.as_view({'post': 'create'})),
    # path('check_account/', UsernameCountView.as_view()),
    # path('check_tel/', TelephoneCountView.as_view()),
    # path('images/', ImagesViewSet.as_view())

]


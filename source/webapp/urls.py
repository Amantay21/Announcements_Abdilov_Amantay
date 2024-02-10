from django.urls import path
from django.views.generic import RedirectView
from webapp.views import IndexView, AnnouncementCreateView, AnnouncementView, AnnouncementUpdateView, \
    AnnouncementDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('announcements/', RedirectView.as_view(pattern_name='webapp:index')),
    path('announcements/add/', AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcement/<int:pk>/', AnnouncementView.as_view(), name='announcement_view'),
    path('announcement/<int:pk>/update/', AnnouncementUpdateView.as_view(), name='announcement_update_view'),
    path('announcement/<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement_delete_view'),
    path('announcement/<int:pk>/comment/add/', CommentCreateView.as_view(), name='comment_add'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update_view'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete_view'),
]

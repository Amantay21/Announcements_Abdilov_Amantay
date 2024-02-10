from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from webapp.models import Comment, Announcements
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from webapp.forms import CommentForm


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'comments/comment_create.html'
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        announcement = get_object_or_404(Announcements, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.announcement = announcement
        comment.author = self.request.user
        comment.save()
        return redirect('webapp:announcement_view', pk=announcement.pk)


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'comments/comment_update.html'
    model = Comment
    form_class = CommentForm
    permission_required = 'webapp.change_comment'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('webapp:announcement_view', kwargs={'pk': self.object.announcement.pk})


class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    permission_required = 'webapp.delete_comment'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:announcement_view', kwargs={'pk': self.object.announcement.pk})

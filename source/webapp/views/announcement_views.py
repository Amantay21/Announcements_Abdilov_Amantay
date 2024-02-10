from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode

from django.db.models import Q
from webapp.models import Announcements
from webapp.forms import AnnouncementForm
from django.views.generic import View, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView


class IndexView(ListView):
    model = Announcements
    template_name = 'announcements/index.html'
    context_object_name = 'announcements'
    paginate_by = 6
    paginate_orphans = 3
    ordering = ('-published_at',)


class AnnouncementView(DetailView):
    model = Announcements
    template_name = 'announcements/announcement_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created')
        return context


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    template_name = 'announcements/announcement_create.html'
    model = Announcements
    form_class = AnnouncementForm

    def form_valid(self, form):
        self.announcement = form.save(commit=False)
        self.announcement.author = self.request.user
        self.announcement.save()
        form.save_m2m()
        return redirect('webapp:announcement_view', pk=self.announcement.pk)


class AnnouncementUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'announcements/announcement_update.html'
    model = Announcements
    form_class = AnnouncementForm
    permission_required = 'webapp.change_announcement'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class AnnouncementDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'announcements/announcement_delete.html'
    model = Announcements
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        return self.request.user.has_perm('webapp.delete_announcement') or self.request.user == self.get_object().author

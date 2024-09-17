from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from blog.models import Blog
from blog.forms import BlogForm


class BlogListView(ListView):
    model = Blog

    def get_context_data(self, *args, **kwargs):
        contex_data = super().get_context_data(*args, **kwargs)
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists():
            blog_list = Blog.objects.all()
        else:
            blog_list = Blog.objects.filter(is_published=True)
        contex_data['blog'] = blog_list
        contex_data['title'] = 'Блоги'
        return contex_data


class BlogCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog')
    permission_required = 'blog.add_blog'
    extra_context = {
        'button_name': 'Создать блог',
        'title': 'Создать Блог'
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.user = self.request.user
        return form


class BlogUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'blog.change_blog'
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog')
    extra_context = {
        'button_name': 'Изменить блог',
        'title': 'Изменить Блог '
    }


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'blog.delete_blog'
    model = Blog
    success_url = reverse_lazy('blog:blog')
    extra_context = {
        'title': 'Удаление Блога '
    }


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_context_data(self, *args, **kwargs):
        contex_data = super().get_context_data(*args, **kwargs)
        blog_list = Blog.objects.get(pk=self.kwargs.get('pk'))
        contex_data['blog'] = blog_list,
        contex_data['title'] = f'Выбранный Блог {blog_list.title}'
        return contex_data

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views_count += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

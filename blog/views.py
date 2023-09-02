from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from pytils.translit import slugify

from blog.models import Public


class PublicListView(ListView):
    model = Public
    # Реализуем выдачу только опубликованных материалов
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(available=True)

        return  queryset




class PublicDetailView(DetailView):
    model = Public

    # Реализуем счетчик просмотра
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object


class PublicCreateView(CreateView):
    model = Public
    fields = ('name', 'description', 'image', 'available',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):  # организация динамических slug для каждого объекта
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:list')


class PublicDeleteView(DeleteView):
    model = Public

    def get_success_url(
            self):  # Переопределение метода, чтобы после удаления показывался каталог публикаций после удаления
        return reverse('blog:list')


class PublicUpdateView(UpdateView):
    model = Public
    fields = ('name', 'description', 'image', 'available',)
    success_url = reverse_lazy('blog:view')

    def form_valid(self, form):  # организация динамических slug для каждого объекта
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):  # перенаправление на отредактированную карточку товара
        return reverse('blog:view', args=[self.kwargs.get('pk')])


def toggle_activity(request, pk):
    product_item = get_object_or_404(Public, pk=pk)
    if product_item.available:
        product_item.available = False
    else:
        product_item.available = True

    product_item.save()

    return redirect(reverse('blog:view'))

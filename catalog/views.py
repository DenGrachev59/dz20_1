from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Category, Product, Version


class IndexView(TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Магазин электроники - Главная'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()[:3]

        return context_data


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Магазин электроники - все наши категории товаров'
    }


class ProductListView(ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        # queryset = queryset.filter(available=True)   # Если раскоментировать будет показывать только активированные товары
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk
        context_data['title'] = f'Магазин электроники - все наши товары в категории {category_item.name}'

        return context_data


class ProductDetailView(DetailView):
    model = Product

    # Реализуем счетчик просмотра
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    login_url = 'users:login'

    # fields = ('name', 'description', 'image', 'category', 'price', 'available',)
    # success_url = reverse_lazy('catalog:category')

    def form_valid(self, form):  # организация динамических slug для каждого объекта
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:category', args=[self.object.category.pk])


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    login_url = 'users:login'



    def get_success_url(
            self):  # Переопределение метода, чтобы после удаления показывалась категория товара после удаления
        return reverse('catalog:category', args=[self.object.category.pk])


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data['formset'] = formset

        return context_data



    def form_valid(self, form):

        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():


            formset.instance = self.object
            formset.save()


        return super().form_valid(form)

    def get_success_url(self):  # перенаправление на отредактированную карточку товара
        return reverse('catalog:view', args=[self.kwargs.get('pk')])


def toggle_activity(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if product_item.available:
        product_item.available = False
    else:
        product_item.available = True

    product_item.save()

    return redirect(reverse('catalog:index'))

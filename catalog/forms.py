from django import forms

from catalog.models import Product, Version  # Subject


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "available":
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ('name', 'description', 'image', 'category', 'price', 'available',)
        # exclude = ('is_active',)

    # Приступаем к стилизации в ручную
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        print(cleaned_data)

        stop_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        if cleaned_data in stop_words:
            raise forms.ValidationError(
                'вы используете  в названии запрещенные слова из списка этого списка: казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        # print (cleaned_data)

        stop_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        if cleaned_data in stop_words:
            raise forms.ValidationError(
                'вы используете в описании запрещенные слова из списка этого списка: казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('product', 'number', 'name', 'available')



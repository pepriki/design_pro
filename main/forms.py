import re

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Category, DesignRequest



class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label='Адрес электронной почты'
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label='Пароль (повторно)',
        widget=forms.PasswordInput,
    )

    consent = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if not re.fullmatch(r'[A-z -]+', username):
            raise ValidationError(
                'Логин должен содержать только латинские буквы и дефис.'
            )

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Этот логин уже занят.')

        return username

    def clean_first_name(self):
        value = self.cleaned_data['first_name']

        if not re.fullmatch(r'[А-яЁё -]+', value):
            raise ValidationError(
                'Имя должно содержать кириллицу, пробелы и дефисы.'
            )

        return value

    def clean_last_name(self):
        value = self.cleaned_data['last_name']

        if not re.fullmatch(r'[А-яЁё -]+', value):
            raise ValidationError(
                'Фамилия должна содержать кириллицу, пробелы и дефисы.'
            )

        return value

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                'Пользователь с такой почтой уже зарегистрирован.'
            )

        return email

    def clean_password1(self):
        password = self.cleaned_data['password1']
        password_validation.validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error(
                'password2',
                'Введённые пароли не совпадают.'
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['name', 'description', 'category', 'image']
        labels = {
            'name': 'Название заявки',
            'description': 'Описание помещения',
            'category': 'Категория дизайна',
            'image': 'Фотография помещения или план',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_image(self):
        image = self.cleaned_data['image']

        allowed_formats = ['JPEG', 'PNG', 'BMP']

        if image.image.format not in allowed_formats:
            raise forms.ValidationError(
                'Допустимые форматы: JPG, JPEG, PNG, BMP.'
            )

        if image.size > 2 * 1024 * 1024:
            raise forms.ValidationError(
                'Размер изображения не должен превышать 2 МБ.'
            )

        return image


class AdminRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['status', 'admin_comment','image', 'design_image']
        labels = {
            'status': 'Новый статус',
            'admin_comment': 'Комментарий администратора',
            'design_image': 'Готовый дизайн',
        }

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        comment = cleaned_data.get('admin_comment')
        design_image = cleaned_data.get('design_image')

        if status == 'in_progress' and not comment:
            self.add_error(
                'admin_comment',
                'Для принятия заявки в работу укажите комментарий.'
            )

        if status == 'completed' and not design_image:
            self.add_error(
                'design_image',
                'Для завершения заявки загрузите готовый дизайн.'
            )

        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Название категории',
        }


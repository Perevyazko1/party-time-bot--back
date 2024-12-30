from django.contrib import admin
from django import forms
from .models import CustomUser,PartyEvent, Advertising, UserCabinet, UserDate

admin.site.register(CustomUser)
admin.site.register(PartyEvent)
admin.site.register(Advertising)
admin.site.register(UserCabinet)
admin.site.register(UserDate)

class UserDateAdminForm(forms.ModelForm):
    class Meta:
        model = UserDate
        fields = '__all__'

    # Кастомное поле для ввода дат в ArrayField
    best_dates = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        help_text="Введите даты через запятую в формате YYYY-MM-DD"
    )
    worst_dates = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        help_text="Введите даты через запятую в формате YYYY-MM-DD"
    )

    # def clean_best_dates(self):
    #     data = self.cleaned_data['best_dates']
    #     if data:
    #         # Преобразуем введённые строки в список дат
    #         try:
    #             return [datetime.strptime(date.strip(), '%Y-%m-%d').date() for date in data.split(',')]
    #         except ValueError:
    #             raise forms.ValidationError("Убедитесь, что даты указаны в формате YYYY-MM-DD, разделённые запятыми.")
    #     return []



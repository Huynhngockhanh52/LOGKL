# forms.py
from django import forms

class LogSettingUploadForm(forms.Form):
    json_file = forms.FileField(required=False)
    json_text = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("json_file")
        text = cleaned_data.get("json_text")

        if not file and not text:
            raise forms.ValidationError("Bạn cần cung cấp một file JSON hoặc nhập JSON vào ô bên dưới.")
        return cleaned_data

from django.forms import ModelForm
from main.models import Shop

class ShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-pink-400 focus:border-pink-400"
            })

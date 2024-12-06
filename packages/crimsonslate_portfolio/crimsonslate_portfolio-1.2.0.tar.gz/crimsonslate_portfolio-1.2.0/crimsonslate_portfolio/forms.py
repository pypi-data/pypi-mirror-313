from django.forms import ModelForm

from crimsonslate_portfolio.models import Media


class MediaUploadForm(ModelForm):
    class Meta:
        model = Media
        fields = [
            "source",
            "thumb",
            "title",
            "subtitle",
            "desc",
            "is_hidden",
            "categories",
        ]


class MediaEditForm(ModelForm):
    class Meta:
        model = Media
        fields = [
            "source",
            "thumb",
            "title",
            "subtitle",
            "desc",
            "is_hidden",
            "categories",
            "date_created",
        ]


class MediaSearchForm(ModelForm):
    class Meta:
        model = Media
        fields = [
            "title",
            "categories",
            "date_created",
        ]

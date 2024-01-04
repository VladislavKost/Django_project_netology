from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ArticleTagsInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_mains = 0
        for form in self.cleaned_data:
            if form.get("is_main", False):
                count_mains += 1
        if count_mains > 1:
            raise ValidationError("Только один тег может быть основным")
        if count_mains == 0:
            raise ValidationError("Необходимо выбрать основной тег")
        return super().clean()


class ArticleTagsInline(admin.StackedInline):
    model = Scope
    formset = ArticleTagsInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "published_at"]
    inlines = [
        ArticleTagsInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]

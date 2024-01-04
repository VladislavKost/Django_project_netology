from django.db import models


class Tag(models.Model):

    name = models.CharField(max_length=50, verbose_name="Название тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name="Название")
    text = models.TextField(verbose_name="Текст")
    published_at = models.DateTimeField(verbose_name="Дата публикации")
    image = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Изображение",
    )
    tags = models.ManyToManyField(Tag, through="Scope")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class Scope(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name="Статья", related_name="scopes"
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, verbose_name="Тег", related_name="scopes"
    )
    is_main = models.BooleanField(default=False, verbose_name="Основной")

    class Meta:
        verbose_name = "Добавить тег"
        verbose_name_plural = "Добавить теги"
        ordering = ["-is_main", "-tag"]
        constraints = [
            models.UniqueConstraint(
                fields=["article", "tag"], name="unique_article_tag"
            )
        ]

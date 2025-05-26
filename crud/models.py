from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint, CheckConstraint
from django.db.models.enums import TextChoices

# ——— Tipos personalizados (ENUMs) —————————————————————————————
class StatusChoices(TextChoices):
    DRAFT     = 'draft',     'Draft'
    PUBLISHED = 'published', 'Published'
    ARCHIVED  = 'archived',  'Archived'

class CategoryChoices(TextChoices):
    STANDARD = 'standard', 'Standard'
    PREMIUM  = 'premium',  'Premium'
    VIP      = 'vip',      'VIP'


# ——— Entidad principal ————————————————————————————————————————
class Product(models.Model):
    # id = AutoField(primary_key=True)  # Django lo crea por defecto
    name        = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        help_text="Nombre único del producto"
    )
    sku         = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        help_text="Stock Keeping Unit"
    )
    status      = models.CharField(
        StatusChoices,
        default=StatusChoices.DRAFT,
        null=False,
    )
    category    = models.CharField(
        CategoryChoices,
        default=CategoryChoices.STANDARD,
        null=False,
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Asegura que el nombre y la categoría formen un par único
            UniqueConstraint(fields=['name', 'category'], name='unique_name_category'),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


# ——— Entidad relacionada —————————————————————————————————————
class Tag(models.Model):
    title       = models.CharField(max_length=50, unique=True, null=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


# ——— Tabla intermedia con datos extra —————————————————————————————
class ProductTag(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_tags'
    )
    tag     = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='product_tags'
    )
    # dato extra: nivel de relevancia de la etiqueta para ese producto
    relevance = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Relevancia (1–10)",
        null=False
    )

    class Meta:
        # impide duplicados del mismo tag en un mismo producto
        constraints = [
            UniqueConstraint(fields=['product', 'tag'], name='unique_product_tag'),
            # un CHECK para que relevance esté entre 1 y 10
            CheckConstraint(check=models.Q(relevance__gte=1, relevance__lte=10),
                            name='check_relevance_range'),
        ]

    def __str__(self):
        return f"{self.tag} → {self.product} ({self.relevance})"


# ——— Relación muchos-a-muchos usando la tabla intermedia ————————
Product.add_to_class(
    'tags',
    models.ManyToManyField(
        Tag,
        through=ProductTag,
        related_name='products'
    )
)


# MODELO PARA EL Índice

class ProductIndex(models.Model):
    id         = models.IntegerField(primary_key=True)
    name       = models.CharField(max_length=100)
    sku        = models.CharField(max_length=30)
    status     = models.CharField(max_length=20)
    category   = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tags       = models.TextField()

    class Meta:
        managed  = False
        db_table = 'product_index'
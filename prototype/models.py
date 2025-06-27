from django.db import models
from django.contrib.auth.models import User

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='img/', blank=True, null=True)

    def __str__(self):
        return self.titulo

class Nota(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='notas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    color = models.CharField(max_length=20, default='green')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Nota de {self.usuario.username} en {self.libro.titulo}'

class ProgresoLibro(models.Model):
    class Categoria(models.TextChoices):
        LEYENDO = 'leyendo', 'Leyendo'
        LEIDO = 'leido', 'Leído'
        POR_LEER = 'por_leer', 'Por Leer'
        QUIERO_LEER = 'qui', 'Quiero Leer'

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pagina_actual = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=20, choices=Categoria.choices, default=Categoria.QUIERO_LEER)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('libro', 'usuario')

    def __str__(self):
        return f'Progreso de {self.usuario.username} en {self.libro.titulo}'
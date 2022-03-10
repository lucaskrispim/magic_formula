from django.db import models

# Create your models here.

class Company(models.Model):
  nome = models.CharField('nome',max_length=30)
  sigla = models.CharField('sigla',max_length=30)
  setor = models.CharField('setor',max_length=30)

  def __str__(self):
    return f"Nome: {self.nome}, Sigla: {self.sigla}, Setor: {self.setor}"
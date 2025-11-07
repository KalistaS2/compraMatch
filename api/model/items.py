from django.db import models

class PcaItem(models.Model):
    id = models.AutoField(primary_key=True)
    descricao_item = models.CharField(max_length=255)
    nome_classificacao_catalogo = models.CharField(max_length=255, null=True, blank=True)
    quantidade_estimada = models.IntegerField(default=0)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unidade_requisitante = models.CharField(max_length=255, null=True, blank=True)
    data_inclusao = models.DateField(null=True, blank=True)
    data_atualizacao = models.DateField(null=True, blank=True)
    data_desejada = models.DateField(null=True, blank=True)
    nome_unidade = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "pca_item"  # equivalente a @Entity(name="pca_item")
        # opcional: verbose_name = "Item PCA"
        # opcional: verbose_name_plural = "Itens PCA"

    def __str__(self):
        return self.descricao_item

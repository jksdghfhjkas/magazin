from django.db import models



class Supplier(models.Model):

    id = models.IntegerField(
        primary_key=True,
        verbose_name="id",
    )
    name = models.CharField(
        max_length=350,
        null=True,
        verbose_name="Название"
    )
    FullName = models.CharField(
        max_length=350,
        null=True,
        verbose_name="Полное название"
    )
    inn = models.CharField(
        max_length=25, 
        null=True,
        verbose_name="ИНН"
    )
    ogrn = models.CharField(
        max_length=25,
        null=True,
        verbose_name="ОРГН"
    )
    address = models.CharField(
        max_length=450, 
        null=True,
        verbose_name="адрес"
    )
    trademark = models.CharField(
        max_length=80,
        null=True,
        verbose_name="торговая марка"
    )
    kpp = models.CharField(
        max_length=50,
        null=True,
        verbose_name="Официальное название"
    )
    registrationDate = models.CharField(
        max_length=20,
        null=True,
        verbose_name="дата регистраций"
    )

    class Meta:
        verbose_name="Поставцик"
        verbose_name_plural="Поставщики"
        ordering = ("id", )


class reviewRatingSupplier(models.Model):

    """ оченка продавца
    data = {
        'feedbacksCount': '32(int)',
        'saleItemQuantity': '432(int)',
        'suppRatio': '432(int)',
        'valuation': '4.3(decimal)'
    }
    """

    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.CASCADE,
        verbose_name="поставщик"
    )

    data = models.JSONField(
        null=True,
        verbose_name="Оценка"
    )

    ProgramLevel = models.CharField(
        max_length=3,
        null=True,
        verbose_name="уровень"
    )

    def __str__(self):
        return f"rating - {self.supplier.id}"


        

    


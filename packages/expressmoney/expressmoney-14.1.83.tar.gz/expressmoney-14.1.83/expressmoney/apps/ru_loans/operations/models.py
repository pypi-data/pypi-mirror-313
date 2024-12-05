from django.db import models


class PayInterests(models.Model):
    created = models.DateTimeField('Создана', auto_now_add=True)
    loan = models.ForeignKey('loans.Loan', models.CASCADE, verbose_name='Займ')
    amount = models.DecimalField('Сумма', max_digits=7, decimal_places=0)
    is_export = models.BooleanField('Выгружать', default=True, help_text='Без галочки: не отправлять данные в 1С')
    comment = models.CharField('Комментарий', max_length=1024, blank=True)

    def save(self, *args, **kwargs):
        pass

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        managed = False
        db_table = 'operations_payinterests'
        verbose_name = 'Погашенные проценты'
        verbose_name_plural = 'Погашенные проценты'


class PayBody(models.Model):
    created = models.DateTimeField('Создана', auto_now_add=True)
    loan = models.ForeignKey('loans.Loan', models.CASCADE, verbose_name='Займ')
    amount = models.DecimalField('Сумма', max_digits=7, decimal_places=0)
    is_export = models.BooleanField('Выгружать"', default=True, help_text='Не отправлять данные в 1С')
    comment = models.CharField('Комментарий', max_length=1024, blank=True)

    def save(self, *args, **kwargs):
        pass

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        managed = False
        db_table = 'operations_paybody'
        verbose_name = 'Погашенное тело'
        verbose_name_plural = 'Погашенное тело'

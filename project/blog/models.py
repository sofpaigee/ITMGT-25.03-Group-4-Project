from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Resource(models.Model):
    SUBJECT_CHOICES = [
        ('MATH 31.1', 'MATH 31.1'),
        ('LAS 21', 'LAS 21'),
        ('MATH 31.2', 'MATH 31.2'),
        ('DECSC 22', 'DECSC 22'),
        ('ITMGT 25.03', 'ITMGT 25.03'),
        ('MATH 31.3', 'MATH 31.3'),
        ('ACCT 115', 'ACCT 115'),
        ('LLAW 113', 'LLAW 113'),
        ('MATH 70.1', 'MATH 70.1'),
        ('ECON 110', 'ECON 110'),
        ('ACCT 125', 'ACCT 125'),
        ('LLAW 115', 'LLAW 115'),
        ('MATH 61.2', 'MATH 61.2'),
        ('DECSC 25', 'DECSC 25'),
        ('ECON 121', 'ECON 121'),
        ('FINN 115', 'FINN 115'),
        ('QUANT 121', 'QUANT 121'),
        ('QUANT 162', 'QUANT 162'),
        ('LAS 111', 'LAS 111'),
        ('MKTG 111', 'MKTG 111'),
        ('QUANT 163', 'QUANT 163'),
        ('LAS 123', 'LAS 123'),
        ('QUANT 192', 'QUANT 192'),
        ('LAS 120', 'LAS 120'),
        ('LAS 140', 'LAS 140'),
        ('OPMAN 125', 'OPMAN 125'),
        ('QUANT 164', 'QUANT 164'),
        ('QUANT 199', 'QUANT 199'),
        ('LAS 197.10', 'LAS 197.10'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES, default='None')
    date_uploaded = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='resource_files')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('resource-detail', kwargs={'pk': self.pk})

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Poll(models.Model):
    """Голосування"""
    title = models.CharField('Назва', max_length=200)
    description = models.TextField('Опис', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Створив')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    is_active = models.BooleanField('Активне', default=True)
    end_date = models.DateTimeField('Дата завершення', null=True, blank=True)

    def __str__(self):
        return self.title
    
    def can_vote(self, user):
        """Чи може користувач голосувати"""
        if not user.is_authenticated:
            return False
        if not self.is_active:
            return False
        if self.end_date and self.end_date < timezone.now():
            return False
        return not Vote.objects.filter(poll=self, user=user).exists()
    
    class Meta:
        verbose_name = 'Голосування'
        verbose_name_plural = 'Голосування'

class Choice(models.Model):
    """Варіант відповіді"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices', verbose_name='Голосування')
    text = models.CharField('Текст варіанту', max_length=200)

    def __str__(self):
        return self.text
    
    @property
    def votes_count(self):
        return self.vote_set.count()
    
    class Meta:
        verbose_name = 'Варіант'
        verbose_name_plural = 'Варіанти'

class Vote(models.Model):
    """Голос користувача"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name='Голосування')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name='Вибір')
    voted_at = models.DateTimeField('Дата голосування', auto_now_add=True)

    class Meta:
        unique_together = ['user', 'poll']
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоси'

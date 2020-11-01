"""Create models."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question model for KU Polls."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date closed')

    def __str__(self):
        """Return question text."""
        return self.question_text

    def was_published_recently(self):
        """Return true."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Return true if question is published."""
        now = timezone.now()
        if now >= self.pub_date:
            return True
        return False

    def can_vote(self):
        now = timezone.now()
        if now >= self.pub_date and now < self.end_date:
            return True
        return False


class Choice(models.Model):
    """Choice model for KU Polls."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.choice_text

    @property
    def votes(self):
        return self.question.vote_set.filter(choice=self).count()

class Vote(models.Model):
     """Vote model for user from KU Polls."""
     question = models.ForeignKey(Question, on_delete=models.CASCADE)
     choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
from django.db import models


class Log(models.Model):

    userId = models.CharField('user_id', max_length=150)
    sessionId = models.CharField('session_id', max_length=150)
    actionTime = models.DateTimeField('action_time')
    actionType = models.CharField('action_type', max_length=150)
    actionProperties = models.TextField('action_properties', max_length=250)

    class Meta:
        db_table = 'logs'
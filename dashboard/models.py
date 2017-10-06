from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    name = models.CharField(max_length=120)
    description = models.TextField()
    author = models.ForeignKey(User)
    status = models.CharField(max_length=20, null=True)
    done_user = models.ForeignKey(User, related_name='marked_done', null=True)
    priority = models.IntegerField(choices=PRIORITY, default=1)

    def list_documents(self):
        return [{'link': d.upload.url, 'filename': d.upload.name}
                for d in self.document_set.all()]


class Document(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

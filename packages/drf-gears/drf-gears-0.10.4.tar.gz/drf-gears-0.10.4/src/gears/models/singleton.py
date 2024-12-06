from django.db import models
from django.db.utils import ProgrammingError
from django.forms import model_to_dict


class SingletonModel(models.Model):
    """Singleton Django Model"""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)
        return self

    @classmethod
    def get(cls, attr: str = None):
        try:
            obj = cls.objects.get()
        except cls.DoesNotExist:
            obj = cls.objects.create()
        except ProgrammingError as e:
            return
        if attr:
            return getattr(obj, attr)
        return obj

    @classmethod
    def update(cls, **kwargs):
        obj = cls.get()
        for k, v in kwargs.items():
            setattr(obj, k, v)
        obj.save()
        return obj

    @classmethod
    def to_dict(cls):
        instance = cls.get()
        return model_to_dict(instance)

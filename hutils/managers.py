
from django.db import models
from model_utils.managers import InheritanceManager, InheritanceQuerySet


class QuerySetManager(models.Manager):
  """
  QuerySetManager can be used to add methods to

  * manager
  * queryset

  Simple use case::

    class Foo(models.Model):
      name = models.CharField(max_length=200)
      members = models.ManyToManyField(User, blank=True, related_name='foos')

      objects = QuerySetManager()

      class QuerySet(models.query.QuerySet):
        def for_user(self, user):
          return self.filter(members__in=user.foos.all)

  """
  use_for_related_fields = True
  def get_query_set(self):
    qs = self.model.QuerySet(self.model, using=self._db)
    return qs
  def __getattr__(self, attr, *args):
    if attr.startswith("_"): # or at least "__"
      raise AttributeError
    return getattr(self.get_query_set(), attr, *args)


class RelatedInheritanceManager(QuerySetManager, InheritanceManager):
  use_for_related_fields = True
  def get_query_set(self):
    return super(RelatedInheritanceManager, self).get_query_set().select_subclasses()



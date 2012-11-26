
from django.test import TestCase
from django.db import models
from hutils.managers import QuerySetManager

class TestModel(models.Model):
  i = models.IntegerField()

  objects = QuerySetManager()

  class QuerySet(models.query.QuerySet):
    def less_than(self, c):
      return self.filter(id__lt=c)


class QuerySetManagerTestCase(TestCase):

  def _setup(self):
    # TODO For some reason model creation does not work in django-nose 1.1
    self.objs = [TestModel.objects.create(i=i) for i in range(3)]

  def _test_get_query_set(self):
    objs = TestModel.objects.less_than(2)
    self.assertEqual(objs.count(), 2)

  def test_attribute_query(self):
    self.assertRaises(AttributeError, lambda: TestModel.objects._foo())



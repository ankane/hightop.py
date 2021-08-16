import django
from django.conf import settings
from django.db import connection, migrations, models
from django.db.migrations.loader import MigrationLoader
from django.db.models.functions import Lower, Upper
from hightop import HightopQuerySet
import logging
import os
import pytest

if os.environ.get('ADAPTER') == 'postgresql':
    database = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hightop_python_test'
    }
elif os.environ.get('ADAPTER') == 'mysql':
    database = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hightop_python_test'
    }
else:
    database = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }

settings.configure(
    DATABASES={
        'default': database
    },
    DEBUG=True
)
django.setup()

logger = logging.getLogger('django.db.backends')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class Visit(models.Model):
    city = models.TextField()
    user_id = models.TextField()

    objects = HightopQuerySet.as_manager()

    class Meta:
        app_label = 'myapp'


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.TextField(null=True)),
                ('user_id', models.TextField(null=True))
            ]
        )
    ]


# probably a better way to do this
migration = Migration('initial', 'myapp')
loader = MigrationLoader(connection, replace_migrations=False)
loader.graph.add_node(('myapp', migration.name), migration)
sql_statements = loader.collect_sql([(migration, False)])

with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS myapp_visit")
    cursor.execute('\n'.join(sql_statements))


def create_city(city, count=1):
    for _ in range(count):
        Visit(city=city).save()


class TestModel(object):
    def setup_method(self, test_method):
        Visit.objects.all().delete()

    def test_top(self):
        create_city('San Francisco', 3)
        create_city('Chicago', 2)
        expected = {
            'San Francisco': 3,
            'Chicago': 2
        }
        assert expected == Visit.objects.top('city')

    def test_limit(self):
        create_city('San Francisco', 3)
        create_city('Chicago', 2)
        create_city('Boston', 1)
        expected = {
            'San Francisco': 3,
            'Chicago': 2
        }
        assert expected == Visit.objects.top('city', 2)

    def test_null_values(self):
        create_city('San Francisco', 3)
        create_city(None, 2)
        expected = {
            'San Francisco': 3
        }
        assert expected == Visit.objects.top('city')

    def test_null_option(self):
        create_city('San Francisco', 3)
        create_city(None, 2)
        expected = {
            'San Francisco': 3,
            None: 2
        }
        assert expected == Visit.objects.top('city', null=True)

    def test_multiple_groups(self):
        Visit(city='San Francisco', user_id='123').save()
        expected = {
            ('San Francisco', '123'): 1
        }
        assert expected == Visit.objects.top(['city', 'user_id'])
        assert expected == Visit.objects.top(('city', 'user_id'))

    def test_expression(self):
        create_city('San Francisco')
        expected = {
            'san francisco': 1
        }
        assert expected == Visit.objects.top(Lower('city'))

    def test_expression_multiple(self):
        create_city('San Francisco')
        expected = {
            ('san francisco', 'SAN FRANCISCO'): 1
        }
        assert expected == Visit.objects.top([Lower('city'), Upper('city')])

    def test_distinct(self):
        Visit(city='San Francisco', user_id='123').save()
        Visit(city='San Francisco', user_id='123').save()
        expected = {
            'San Francisco': 1
        }
        assert expected == Visit.objects.top('city', distinct='user_id')

    def test_distinct_expression(self):
        Visit(city='San Francisco', user_id='A').save()
        Visit(city='San Francisco', user_id='a').save()
        Visit(city='San Francisco', user_id='B').save()
        expected = {
            'San Francisco': 2
        }
        assert expected == Visit.objects.top('city', distinct=Lower('user_id'))

    def test_min(self):
        create_city('San Francisco', 3)
        create_city('Chicago', 2)
        expected = {
            'San Francisco': 3
        }
        assert expected == Visit.objects.top('city', min=3)

    def test_min_distinct(self):
        Visit(city='San Francisco', user_id=1).save()
        Visit(city='San Francisco', user_id=1).save()
        Visit(city='San Francisco', user_id=2).save()
        Visit(city='Chicago', user_id=1).save()
        Visit(city='Chicago', user_id=1).save()
        expected = {
            'San Francisco': 2
        }
        assert expected == Visit.objects.top('city', min=2, distinct='user_id')

    def test_where(self):
        create_city('San Francisco')
        create_city('Chicago')
        expected = {
            'San Francisco': 1
        }
        assert expected == Visit.objects.filter(city='San Francisco').top('city')

    def test_no_columns(self):
        with pytest.raises(ValueError) as error:
            Visit.objects.top([])
        assert 'No columns' == str(error.value)

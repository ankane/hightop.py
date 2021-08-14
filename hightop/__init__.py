from django.db.models import Count, QuerySet
from django.db.models.expressions import Func
from typing import Any, Dict, Optional


class HightopQuerySet(QuerySet):
    def top(self, column: Any, limit: Optional[int] = None, null: bool = False, min: Optional[int] = None, distinct: Any = None) -> Dict[Any, int]:
        columns = list(column) if isinstance(column, list) or isinstance(column, tuple) else [column]
        if len(columns) == 0:
            raise ValueError('No columns')

        result = self
        for i, c in enumerate(columns):
            if isinstance(c, Func):
                name = 'column{}'.format(i)
                result = result.annotate(**{name: c})
                columns[i] = name

        count = Count(distinct, distinct=True) if distinct else Count('*')
        result = result.values(*columns).annotate(count=count).order_by('-count', *columns)

        if not null:
            result = result.exclude(**{column: None for column in columns})

        if min is not None:
            result = result.filter(count__gte=min)

        if limit is not None:
            result = result[:limit]

        # Python 3.6+ maintains insertion order for dict
        # (only an implementation detail in 3.6)
        if len(columns) == 1:
            return {row[columns[0]]: row['count'] for row in result}
        else:
            return {tuple([row[column] for column in columns]): row['count'] for row in result}

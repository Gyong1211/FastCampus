# Django
## Query

### Making queries

###### 모델 정의

```python

from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.headline
```

<br>

### Creating objects

```python
# on ./manage.py shell

>>> from blog.models import Blog
>>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
>>> b.save()
```

위의 예시를 `shell`에서 입력하면 `INSERT` SQL문을 수행한다.  
Django는 `save()`를 호출 할 때까지 데이터베이스에 `b`를 저장하지 않는다.

> 객체를 만들고 저장하는 것을 한 단계로 수행하고자 하면 `create()` 메서드를 사용한다.

#### Saving changes to objects

```python
# on ./manage.py shell

>>> b5.name = 'New name'
>>> b5.save()
```

DB에 이미 저장된 인스턴스 b5가 주어진 상태에서, 위의 예제를 실행하면 b5의 name을 변경하고 `save()`를 호출하면 db에 해당 레코드를 업데이트한다.  
이 때, `save()`는 `UPDATE` SQL문을 수행한다.

#### Saving ForeignKey and ManyToManyField fields
`ForeignKey` 필드를 업데이트 하는 것은 일반 필드를 저장하는 것과 같은 방식이다.

```python
#on ./manage.py shell
>>> from blog.models import Entry
>>> entry = Entry.objects.get(pk=1)
>>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
>>> entry.blog = cheese_blog
>>> entry.save()
```

<br>
하지만 `ManyToMany`는 `save()` 메서드를 사용하지 않고, `add()`메서드를 사용해 관계에 레코드를 추가한다.

```python
>>> from blog.models import Author
>>> joe = Author.objects.create(name="Joe")
>>> entry.authors.add(joe)
```

복수의 레코드를 `ManyToMany` 필드에 한번에 추가하기 위해서는, `add()` 메서드에 여러 인자를 입력해준다.

```python
>>> john = Author.objects.create(name="John")
>>> paul = Author.objects.create(name="Paul")
>>> george = Author.objects.create(name="George")
>>> ringo = Author.objects.create(name="Ringo")
>>> entry.authors.add(john, paul, george, ringo)
```

### Retrieving objects
DB의 객체를 검색하기 위해서는 모델 클래스의 `Manager`를 이용해 `QuerySet`을 생성해야한다.

`QuerySet`은 DB의 objects의 집합을 나타내며, 필터를 가지지 않을 수 있고 여러개의 필터를 가질 수도 있다.

필터는 주어진 매개변수를 기반으로 쿼리셋에 들어갈 쿼리에 조건을 건다. SQL 문에서 `QuerySet`은 `SELECT`문의 역할을 하고, 필터는 `WHERE` 또는 `LIMIT`과 같은 제한절 역할을 한다.

```python
>>> Blog.objects
<django.db.models.manager.Manager object at ...>
>>> b = Blog(name='Foo', tagline='Bar')
>>> b.objects
Traceback:
    ...
AttributeError: "Manager isn't accessible via Blog instances."
```

`Manager`는 모델에 대한 `QuerySet`의 주요 소스이다. `Blog.objects.all()`은 DB의 모든 `Blog` 객체를 포함하는 `QuerySet`을 반환한다.

### Retrieving all objects

테이블에서 모든 개체를 가져오고 싶은 경우, `all()` 메서드를 사용한다.

```python
>>> all_entries = Entry.objects.all()
```

### Retrieving specific objects with filters

조건을 걸어 객체의 일부를 가져오고 싶은 경우, `filter()`와 `exclud()`를 사용한다.

- `filter(**kwargs)` : 지정된 매개변수와 일치하는 객체를 포함한 `QuerySet`을 반환
- `exclude(**kwargs)` : 지정된 매개변수와 일치하지 않는 객체를 포함한 `QuerySet`을 반환

>(**kwargs)는 다음과 같은 형식으로 입력한다.
>`Entry.objects.filter(pub_date__year=2006)`
>
>기본 `Manager` 필드를 이용한 방법은 아래와 같다.
>`Entry.objects.all().filter(pub_date__year=2006)`

##### Chaining filters

`QuerySet`에  필터를 사용한 결과는 `QuerySet`이므로 연쇄적으로 필터를 사용할 수 있다.

```python
>>> Entry.objects.filter(
... 	headline__startswith='What'
... ).exclude(
...		pub_date__gte=datetime.date.today()
... ).filter(
... 	pub_date__gte=datetime(2005,1,30)
... )
```
위 예문의 최종 결과는 2006년 1월 30일과 현재 날짜 사이에 발행된 "What"으로 시작하는 제목이 있는 모든 항목을 포함한 `QuerySet`이다.


### Retrieving a single object with get()
`filter()`는 항목이 1개만 있어도 항상 `QuerySet`을 반환한다.  
만약 일치하는 1개의 `Query`를 얻고싶다면, `Manager`에서 `get()` 메서드를 사용한다.

```python
>>> one_entry = Entry.objects.get(pk=1)
```

### Limiting QuerySets
Python 문법을 사용하여, QuerySet에 `LIMIT`과 `OFFSET`과 같은 SQL문이 적용된 효과를 낼 수 있다.

`LIMIT 5`

```python
>>> Entry.objects.all()[:5]
```

`OFFSET 5 LIMIT 5`

```python
>>>Entry.objects.all()[5:10]
```

> 역방향 정렬(ex: `Entry.objects.all()[-1]`)은 지원되지 않는다.
> 
> step을 사용하는 것도 가능하다
> 
> ```python
> Entry.objects.all()[:10:2]
> ```
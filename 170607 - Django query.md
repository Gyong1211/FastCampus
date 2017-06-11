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

### Field lookups
원하는 field를 조회하기 위해서는 `filter()`, `exclude()`, `get()`을 사용한다.  
키워드 인자로 사용하는 인수는 `field__lookuptype=value`의 형태를 띈다.

```python
Entry.objects.filter(pub_date__lte='2006-01-01'
```

위의 예시를 SQL문으로 바꾸면 아래와 같다.

```SQL
SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01'
```
<br>

###### lookup type

- `exact` : 정확하게 값이 일치하는 객체를 찾음
	
	```python
	Entry.objects.get(headline__exact = "Cat bites dog")
	```
	```
	>>> Blog.objects.get(id__exact=14)  # Explicit form
	>>> Blog.objects.get(id=14)         # __exact is implied
	```
	
- `iexact` : 대소문자를 구분하지 않는 `exact`
- `contains` : 해당 값이 포함된 객체를 찾음
	
	```python
	Entry.objects.get(headline__contains='Lennon')
	```
	```sql
	SELECT ... WHERE headline LIKE '%Lennon%';
	```

- `startswith`, `endswith` : 해당 값으로 시작/끝나는 객체를 찾음
- `istartswith`, `iendswith` : 대소문자를 구분하지 않는 `startswith`, `endswith`

### Lookups that span relationships

Django는 자동으로 relationship을 SQL JOIN으로 처리하면서 해당 관계를 정리해둔다.

해당 관계를 이용해서, 원하는 필드를 찾을 때 까지 두 모델 관련 필드의 이름을 `__`로 구분하여 사용하면 된다.

```python
>>> Blog.objects.filter(entry__headline__contains='Lennon')
```

해당 예제는 헤드라인에 `Lennon`이 포함된 `Entry`를 하나이상 가지고 있는 `Blog` 객체를 가져온다.

#### Spanning multi-valued relationships

```python
Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)
```
두 조건 (`Lennon`을 포함한 헤드라인, `pub_date`의 년도가 2008년인 `Entry`를 가진)을 모두 만족하는 `Entry`를 가진 블로그를 얻기 위해서 `,`를 사용하면 된다.


```python
Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)
```
`Lennon`을 포함한 헤드라인을 가진 `Entry`와 `pub_date`의 년도가 2008년인 `Entry`를 모두 가진 블로그를 얻기 위해서 filter chaining을 사용한다.

### Filters can reference fields on the model

모델의 필드 값과 상수를 비교하는 필터 외에, 같은 모델의 다른 필드와 비교하기 위해서 `F()`를 사용한다.

```python
>>> from django.db.models import F
>>> Entry.objects.filter(n_comments__gt=F('n_pingbacks'))
```

위의 예제는 `n_comments`의 값이 `n_pingbacks`의 값보다 큰 `Entry` 객체를 찾는다.

```python
>>> Entry.objects.filter(n_comments__gt=F('n_pingbacks') * 2)
```
위의 예제처럼 `F()`객체에는 +,-,*,/,모듈러스, 지수연산을 사용할 수 있다.

### Caching and QuerySets

새로 생성 된 QuerySet에서 캐시는 비어 있다.  
QuerySet이 처음 동작할 때(데이터베이스 쿼리가 발생할 때) Django는 쿼리 결과를 QuerySet의 캐시에 저장하고 명시 적으로 요청 된 결과를 반환한다. (예 : QuerySet이 반복되는 경우 다음 요소)

```python
>>> print([e.headline for e in Entry.objects.all()])
>>> print([e.pub_date for e in Entry.objects.all()])
```

캐싱 동작을 염두해야하는 이유는, 위의 예제의 경우, 두개의 QuerySets을 만들고, 동작한 다음 해당 QuerySets를 버린다.

또한 두 요청 사이에 시간차 사이에 데이터가 추가되거나 삭제 되었을 수도 있다.

따라서 이러한 문제를 해결하기 위해서는, Queryset을 먼저 캐싱해 두어야 한다.

```python
>>> queryset = Entry.objects.all()
>>> print([p.headline for p in queryset]) # Evaluate the query set.
>>> print([p.pub_date for p in queryset]) # Re-use the cache from the evaluation.
```
<br>

>Query는 항상 결과를 캐시하지 않는다.
>QuerySet의 일부만 검사하는 경우 매번 DB에 접근한다.

>```python
>>>> queryset = Entry.objects.all()
>>>> print(queryset[5]) # Queries the database
>>>> print(queryset[5]) # Queries the database again
>```
>
> 하지만 한번 캐싱한 다음, 일부를 검사하는 경우, DB대신 캐시에 접근한다.
> 
> ```python
>>>> queryset = Entry.objects.all()
>>>> [entry for entry in queryset] # Queries the database
>>>> print(queryset[5]) # Uses cache
>>>> print(queryset[5]) # Uses cache
>``` 

### Complex lookups with Q objects

`filter()`의 조건에 `AND`나 `OR` 연산을 사용하고 싶은 경우 `Q()`를 사용한다.

```python
Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)
```

위의 예제는 아래 SQL문과 같다.

```sql
SELECT * from polls WHERE question LIKE 'Who%'
    AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')
```

`Q()`와 키워드 인자를 섞어서 사용할 수 있다. 하지만 그런 경우 `Q()`가 키워드 인자보다 앞으로 나와 있어야한다.

```python
Poll.objects.get(
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
    question__startswith='Who',
)

#위의 경우 가능
```

```python
Poll.objects.get(
    question__startswith='Who',
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)
#불가능
```

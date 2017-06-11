# Django
## QuerySet API reference

### QuerySet의 활용

1. Iteration
	
	QuerySet은 순회 가능한 형태를 가진다.

	```python
	for e in Entry.objects.all():
		print(e.headline)
	```
	for문을 이용해 각 Entry를 순회하며 headline을 출력할 수 있다.

2. Slicing

	List형 객체의 슬라이싱과 같다.

3. Pickling/Caching

	`Pickle` : 메모리의 데이터를 영구적으로 저장

	QuerySet을 unpickle하면, 현재 DB에 있는 결과가 아닌 pickle했던 순간의 결과가 나온다.

	만약 나중의 DB에서 QuerySet을 다시 만드는데 필요한 정보만 pickle하고싶다면, query를 pickle하면 된다.

	```python
	>>> import pickle
	>>> query = pickle.loads(s)     # Assuming 's' is the pickled string.
	>>> qs = MyModel.objects.all()
	>>> qs.query = query            # Restore the original 'query'.
	```

4. repr()

	QuerySet은 repr()을 호출할 때 평가되어, 데이터베이스에 대한 접근을 하고 데이터를 캐싱한다.

5. len()

	len()을 호출하면, QuerySet이 평가되고, list와 마찬가지로 길이를 반환한다.
	> 단순히 쿼리셋의 길이를 알고 싶은 경우 SQL 문의 SELECT COUNT (*)를 사용하여 DB 수준에서 카운트를 처리하는 것이 훨씬 효율적이다.
	>Django는 이와 같은 count() 메소드를 지원한다.
	
6. list()

	QuerySet을 list()를 사용해 호출하면, 강제적으로 평가된다.
	```python
	entry_list = list(Entry.objects.all())
	```
	
7. bool()

	QuerySet을 `bool()`,`or`,`and`,`if`같은 boolean context를 이용해 테스트를 하면, 쿼리가 실행된다.
	
	하나 이상의 결과가 있다면, True가 반환되고, 그렇지 않으면 False가 반환된다.
	
	```python
	if Entry.objects.filter(headline="Test"):
   print("There is at least one Entry with the headline Test")
   ```
   

### QuerySet API

QuerySet를 사용할 때는 주로 filter 옵션들을 많이 이용한다. 대부분의 QuerySet 메소드들의 수행 결과는 새로운 QuerySet를 반환한다.

QuerySet 클래스에는 내부적으로 활용할 수 있는 두개의 속성이 있다.

 - ordered : QuerySet이 정렬되어 있다면(order\_by()절이나 기본 정렬이 된 모델) True, 아니라면 False를 반환

 - db : 현재 QuerySet이 사용하는 db의 정보를 반환

 
### Methods that return new QuerySets

#### filter()
주어진 lookup parameter와 일치하는 객체가 포함된 새 QuerySet을 반환한다.

복합적인 조건을 만들기 위해서는 Q object를 이용한다.

```python
Post.objects.filter(title__startswith='First')
```
위 예제는 title이 First로 시작하는 Post 객체가 포함된 QuerySet을 반환한다.

#### exclude()
주어진 lookup parameter와 일치하지 않는 객체가 포함된 새 QuerySet을 반환한다.

```python
Post.objects.exclude(title__startswith='First')  
```
위 예제는 title이 First로 시작하지 않는 Post 객체가 포함된 새 QuerySet을 반환한다.

#### annotate()
쿼리에 사용자가 원하는 내용의 주석을 추가한다.  
주석을 지정할 때 사용된 키워드 인자는 주석을 호출하는 별칭으로 사용된다. 

아래의 예제는 데이터가 몇 개 존재하는지 개수를 반환하는 count 함수를 이용하여 annotate해주고 이를 \_\_count로 접근할 수 있다.

```python
>>> from django.db.models import Count
>>> q = Blog.objects.annotate(Count('entry'))
>>> q[0].name
'Blogasaurus'
>>> q[0].entry__count
42
```

주석을 호출하는 별칭을 따로 지정해 줄 수 있다.

```python
>>> q = Blog.objects.annotate(number_of_entries=Count('entry'))
# The number of entries on the first blog, using the name provided
>>> q[0].number_of_entries
42
```

#### order_by()
주어진 field를 기준으로 QuerySet을 정렬한다.  
field명 앞에 아무것도 붙지 않은 경우에 오름차순으로 정렬, `-`가 붙은 경우는 내림차순 정렬을 한다.

```python
Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')
```
위 예제의 경우, pub\_date를 기준으로 내림차순으로 정렬하고, pub\_date가 같은 경우는 headline을 기준으로 오름차순으로 정렬한다.

```python
Entry.objects.order_by('?')
```
`?`를 사용하면 랜덤으로 정렬한다.

```python
Entry.objects.order_by('blog__name', 'headline')
```
다른 모델에 있는 필드를 기준으로 정렬할 경우, double underscore(`__`)를 사용한다.

```python
Entry.objects.order_by('blog')
Entry.objects.order_by('blog__id')
```

Meta.ordering으로 특별히 정렬기준을 정해주지 않으면 두 구문의 결과는 같다.  
(기본 정렬 방식을 primary key 기준으로 한다.)


>```python
>Entry.objects.order_by('blog')
>Entry.objects.order_by('blog__name')
>```
>Meta.ordering이 'name'인 경우는 위 두 구문의 결과가 같다.

```python
Entry.objects.order_by(Coalesce('summary', 'headline').desc())
```

```python
Entry.objects.order_by(Lower('headline').desc())
```

`asc()`나 `desc()`를 사용해서 오름/내림차순 정렬을 할 수 있다.

>order\_by를 체이닝해서 사용하는 경우, 맨 마지막의 order\_by만 적용되고, 앞은 다 무시된다.
>
>```python
>Entry.objects.order_by('headline').order_by('pub_date')
>```
>위 예시는 pub_date를 기준으로 오름차순 정렬된다.

#### reverse
QuerySet의 순서를 반대로 바꿔준다.

```python
my_queryset.reverse()[:5]
```
위 예제는 my_queryset의 기존 정렬 순서를 반대로 바꾼 뒤, 처음부터 5개의 데이터를 꺼낸다.  
즉, 마지막 my_queryset의 마지막 5개의 데이터를 꺼내는 효과가 있다.

> ordering을 명시해주지 않으면 reverse는 동작하지 않는다.

#### distinct()
SQL 쿼리에서 SELECT DISTINCT를 사용하는 새 QuerySet을 반환한다. 즉, 조회결과에서 중복되는 행을 제거한다. 

#### values()

```python
# This list contains a Blog object.
>>> Blog.objects.filter(name__startswith='Beatles')
<QuerySet [<Blog: Beatles Blog>]>

# This list contains a dictionary.
>>> Blog.objects.filter(name__startswith='Beatles').values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
```

QuerySet을 모델 인스턴스가 아닌 딕셔너리로 반환한다.


```python
>>> Blog.objects.values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
>>> Blog.objects.values('id', 'name')
<QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>
```

value()의 위치 인자(*field)로 필드명을 적어주면, 해당하는 필드명만 딕셔너리 형태로 반환한다

#### value_list()

```python
>>> Entry.objects.values_list('id', 'headline')
[(1, 'First entry'), ...]
>>> from django.db.models.functions import Lower
>>> Entry.objects.values_list('id', Lower('headline'))
[(1, 'first entry'), ...]
```

value()와 유사하지만, 딕셔너리 대신 튜플로 반환한다.

```python
>>> Entry.objects.values_list('id').order_by('id')
[(1,), (2,), (3,), ...]

>>> Entry.objects.values_list('id', flat=True).order_by('id')
[1, 2, 3, ...]
```
1개의 값만 반환하는 경우에도 튜플로 반환하는데, flat=True 속성을 줄 경우, 단일 값만 반환하게 된다.

#### dates()

QuerySet의 필드 중에, datetime.date형 데이터를 반환한다.  
첫 번째 인자에 field name, 두 번째 인자에는 `year`, `month`, `day`중에 원하는 값을 입력한다.  
정렬은 `ACS`와 `DESC`를 사용할 수 있으며, 입력하지 않은 경우, `ACS`로 정렬된다.


#### datetimes()

dates()와 유사하게, datetime.datetime형 데이터를 반환한다.  
두 번째 인자에 `hour`, `minute`, `second`를 추가로 사용할 수 있다.

#### all()

현재의 QuerySet (또는 QuerySet 서브 클래스)의 복사본을 반환한다.

#### union()

SQL의 UNION 연산자를 사용하여 두 개 이상의 QuerySet 결과를 결합한다.

```python
>>> qs1.union(qs2, qs3)
```

기본적으로 UNION은 고유한 값(중복되지 않은 값)만 선택한다. 중복된 값을 허용하려면 all=True 옵션을 사용한다.

#### intersection()

SQL의 INTERSECT 연산자를 사용하여 두 개 이상의 QuerySets의 공유 요소를 반환한다.

```python
>>> qs1.intersection(qs2, qs3)
```

#### difference()

SQL의 EXCEPT를 사용해, QuerySet에는 있지만 일부 다른 QuerySet에는 없는 요소만 반환한다.

```python
>>> qs1.difference(qs2, qs3)
```

#### select_related()

외래 키 관계 또는 일대일 관계를 따르는 QuerySet을 반환 해, 해당 쿼리를 실행할 때에 관련된 객체 데이터를 미리 선택헤둔다.

복잡한 쿼리인 경우에 성능을 향상시킬 수 있지만, 차후에 외래 키의 데이터베이스 쿼리를 사용하지 않게 된다. (캐싱한 정보를 사용한다.)

```python
# Hits the database.
e = Entry.objects.get(id=5)

# Hits the database again to get the related Blog object.
b = e.blog
```

```python
# Hits the database.
e = Entry.objects.select_related('blog').get(id=5)

# Doesn't hit the database, because e.blog has been prepopulated
# in the previous query.
b = e.blog
```
 위 두 예시는 같아보이지만, 첫 번째 예시는 DB에 2번 접근하는 반면, 두 번째 예시는 처음 1번만 DB에 접근한다.
 
#### prefetch_related()

select\_related()가 SQL문의 SELECT문을 이용해 외래키, 일대일 관계를 따르는 경우에만 사용이 가능하다면, prefetch\_related()는 JOIN을 이용해 외래키 및 일대일 관계 이외에도 다대다 및 다대일 관계에도 사용이 가능하다.


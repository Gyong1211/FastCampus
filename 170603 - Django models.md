# Django

## Introduction to models

### Models

- 각 모델은 django.db.models.Model의 하위 클래스다.
- 모델의 각 속성은 데이터베이스의 필드를 나타낸다.
- Django는 모델을 통해 자동으로 생성된 데이터 베이스에 액세스 할 수 있는 API를 제공한다.

<br>
###### Example
```python
from django.db iport models

class Person(models.Model):
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30)
```

`first_name`과 `last_name`은 모델의 field다.  
각 필드는 클래스의 속성과 같으며, 데이터 베이스의 column에 매핑된다.

위의 모델을 생성하면 다음과 같은 SQL이 구성된다.

```sql
CREATE TABLE myapp_person (
	"id" serial NOT NULL PRIMARY KEY,
	"first_name" varchar(30) NOT NULL
	"last_name" varchar(30) NOT NULL
);
```

### Using models

모델을 사용하기 위해서는 `settings.py` 파일 내`INSTALLED_APP`에 해당 model이 있는 app을 추가해줘야 한다.

```python
INSTALLED_APP = [
	#...
	'myapp'
	#....
]
```

INSTALLED_APP에 새로운 app을 추가한 경우, manage.py에서 migrate와 makemigrations로 마이그레이션을 수행해야한다.

### Fields

모델에서 가장 중요하고, 필수적인 부분이 바로 필드다.  
필드는 클래스의 속성에 의해 지정된다.

### Field types
모델의 각 필드는 해당 클래스의 인스턴스여야 한다.  
Django는 필드 클래스 유형을 사용해 몇가지를 결정한다.

- DB에 저장할 데이터의 종류 (ex: INTEGER, VARCHAR, TEXT)
- Form field를 렌더링 할 때 사용할 HTML 위젯 (ex: `<input type ="text">`, `<select>`)
- 장고 관리자 및 자동생성 양식에서 사용되는 최소한의 유효성 요구사항

### Field options
각 필드는 특정한 arguments set을 갖는다.  
예를 들어, `CharField`는 DB의 VARCHAR 필드에 저장되는 데이터의 최대 길이를 제한하는 `max_length` argument를 필요로 한다.

<b>자주 쓰이는 옵션들</b>

- null  
	null 속성이 True인 경우, Django는 해당 값을 null로 DB에 저장한다. (Default = False)
	
- blank  
	blank 속성이 True인 경우, 빈 값이 저장될 수 있다. (Default = False)
	
	>null과 blank는 다르다.  
	>null = 값이 없음
	>blank = 빈 값을 가짐
	
	
- choices  
	iterable한 리스트형 객체가 있을 때, widget의 기본 폼을 text box 대신 select box로 변경하고, 주어진 리스트 내의 값만 선택할 수 있게 한다.
	
	###### example
	```python
	YEARS_IN_SCHOOL_CHOICES = (
		('FR','Freshman'),
		('SO','Sophomore'),
		('JR','Junior'),
		('SR', 'Senior'),
		('GR', 'Graduate'),
	)
	```
	
	튜플의 첫 번째 값이 DB에 저장되며, 두 번째 값이 form의 widget에 표시 된다.
	
	```python
	from django.db import models
	
	class Person(models.Model):
   		SHIRT_SIZES = (
			('S', 'Small'),
			('M', 'Medium'),
			('L', 'Large'),
		)
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    ```
    
	```python
	>>> p = Person(name="Fred Flintstone", shirt_size="L")
	>>> p.save()
	>>> p.shirt_size
	'L'
	>>> p.get_shirt_size_display()
	'Large'
	```
	p.shirt_size는 튜플의 첫번째 값인 `L`을 갖게 되고, `get_shirt_size_display` 메서드를 사용해 표시되는 값을 불러올 수 있다.
	
- default  
	필드의 기본 값을 정의할 수 있다. 특정 값 또는 호출 가능한 객체가 올 수 있다.

- help_text  
	form widget과 함께 표시되는 추가적인 '도움말' 텍스트
	
- <b>primary_key</b>  
	이 값이 True가 된다면, 해당 필드는 해당 모델의 primary key 값으로 지정된다.

- unique  
	해당 필드는 중복되지 않는 값을 가지게 된다.

### Automatic primary key fields
Django는 기본적으로 각 모델에 해당 필드를 생성한다.

```python
id = models.AutoField(primary_key=True)
```
사용자가 primary key를 특정 필드에 지정하고 싶다면, 필드에 해당 속성을 넣어주면 된다.  
Django는 사용자가 primary key를 지정했다고 판단하면, 자동으로 생성되는 id 열을 추가하지 않는다.

### Verbose field names
`ForeignKey`, `ManyToManyField`와 `OneToOneField`를 제외한 각 필드 유형은, 첫 번째 위치 인자를 `Verbose name`으로 가질 수 있다.

```python
first_name = models.CharField("person's first name", max_length=30)
```
위의 예제에서, `first_name`의 `verbose name`은 `"person's first name"`이다. (지정한 경우)

```python
first_name = models.CharField(max_length=30)
```
위의 예제에서, `first_name`의 `verbose name`은 `first_name`이다. (지정하지 않은 경우)

<br>

`ForeignKey`, `ManyToManyField`와 `OneToOneField`은, 첫 번째 인자로 model class를 필요로 한다.  
따라서 `verbose name`을 지정하고 싶다면, verbose_name 키워드 인자를 사용해야 한다.

```python
poll = models.ForeignKey(
	Poll,
	on_delete = models.CASCADE,
	verbose_name = "the related poll",
)
sites = models.ManyToManyField(Site, vebose_name = "list of sites")
place = models.OneToOneField(
	Place,
	on_delete=modles.CASCADE,
	verbose_name = "related place",
)
```

vebose_name을 설정할 때, 첫 문자를 대문자로 사용하지 않는 것이 규칙이다.  
Django는 필요한 첫 문자를 자동으로 대문자로 만들어준다.

### Relationships
#### Many-to-one relationships
```python
class Manufacturere(models.Model):
	#...
	pass
	
class Car(models.Model):
	manufacturer = models.ForeignKey(
		Manufacturer,
		on_delete=models.CASCADE,
	)
	#...
	
```
재귀 관계(다대일 관계가 있는 객체)와 아직 정의되지 않은 모델과의 관계를 생성할 수 있다.  
위의 예시에서, Car는 ForeignKey 필드 값의 참조를 Manufacturer로 한다.  
즉, 예시의 Many-to-one은 Car-to-Manufacturer이다. 다양한 Car는 하나의 Manufacturer의 정보를 가진다.

#### Many-to-many relationships

```python
class Topping(models.Model):
	#...
	pass

class Pizza(models.Model):
	#...
	toppings = models.ManyToManyField(Topping)
	
```
어떤 모델에 ManyToManyField가 있던지는 문제가 되지 않지만, 두 모델중 하나의 모델에만 사용해야 한다.  

일반적으로 ManyToManyField 인스턴스는 편집할 객체에 있어야한다.  
위의 예시에서, 여러개의 피자에 토핑을 넣는 것보다 피자에 여러가지의 토핑을 넣는 것이 자연스럽다.  
(토핑은 정해져 있고, 피자의 종류에 따라 토핑을 추가하는 방식이 자연스럽지 않은가?!)  
따라서 위와 같은 방식을 사용하면, 사용자가 원하는대로 pizza에 토핑을 추가할 수 있다.

#### Extra fields on many-to-many relationships

피자와 토핑을 매칭하는 것과 같은 단순한 다대다 관계를 처리할 경우에는 표준 ManyToManyField만 있으면 충분하다.  
하지만 때로 두 모델 간의 관계 데이터를 연결해야 할 경우도 존재한다.

예를 들어 음악가가 속한 음악 그룹을 tracking하는 응용프로그램이 있다고 생각하자.  
음악가와 음악 그룹 사이에는 many-to-many 관계가 있을 것이고, 그 관계를 나타내기 위해서는 ManyToManyField를 사용한다.  
그룹에 가입한 날짜와 같은 멤버쉽에 대한 세부정보는 어떻게해야할까?

이러한 상황에서 Django는 다대다 관계를 관리할 때 사용될 intermediate 모델을 `throughTo` argument를 사용해 지정할 수 있다.

```python
class Person(models.Model):
	name = models.CharField(max_length=128)
	
class Group(models.Model):
	name = models.CharField(max_length=128)
	members = models.ManyToManyField(Person, through='Membership')
	
class Membership(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	date_joined = models.DateField()
	invite_reason = models.CharField(max_length=64)
	
```

intermediate 모델을 설정할 때, 다대다 관계와 관련된 `ForeignKey`를 명시적으로 지정한다.  
이 명시적 선언은 두 모델이 관련되는 방식을 정의한다.

> Intemediate 모델의 제한사항
> 
> - Intermediate 모델에는 소스 모델에 대한 외래 키가 하나만 포함되어야한다. (위 예에서는 Group이 소스 모델)
> - 또는 Django가 `ManyToManyField.through_fields`를 사용하여 관계에 사용해야하는 외래 키를 명시 적으로 지정해야한다.  
> 둘 이상의 외부 키가 있고 `through_fields`가 지정되지 않은 경우 유효성 검증 오류가 발생한다. 비슷한 제한이 대상 모델에 대한 외래 키에도 적용된다. (위 예에서는 Person이 대상 모델)
> - Intermediate 모델을 통해 다대다 관계를 갖는 모델의 경우 동일한 모델에 대한 두 개의 외래 키가 허용되지만 다 대다 관계의 두 (다른) 측면으로 처리된다.  
> 두 개 이상의 외래 키가있는 경우 위와 같이 `through_fields`도 지정해야한다. 그렇지 않으면 유효성 검사 오류가 발생한다.
> - Many-to-many relationship을 설정할때, symmetrical 속성은 <b>무조건 False</b>로 지정해줘야한다.

```python
>>> ringo = Person.objects.create(name="Ringo Starr")
>>> paul = Person.objects.create(name="Paul McCartney")
>>> beatles = Group.objects.create(name="The Beatles")
>>> m1 = Membership(person=ringo, group=beatles,
...     date_joined=date(1962, 8, 16),
...     invite_reason="Needed a new drummer.")
>>> m1.save()
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>]>
>>> ringo.group_set.all()
<QuerySet [<Group: The Beatles>]>
>>> m2 = Membership.objects.create(person=paul, group=beatles,
...     date_joined=date(1960, 8, 1),
...     invite_reason="Wanted to form a band.")
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>]>
```

일반적인 many-to-many 필드와 다르게, intermediate 모델을 설정한 경우 relationship을 생성할 때 `add()`, `create()`와 `set()`은 사용할 수 없다.

```python
>>> # The following statements will not work
>>> beatles.members.add(john)
>>> beatles.members.create(name="George Harrison")
>>> beatles.members.set([john, paul, ringo, george])
```

Intermediate 모델이 존재하기 때문에, 위의 예시와 같이 개인과 그룹 간의 관계만 생성할 수 없다.  
Membership 모델에 필요한 Person과 Group간 관계에 대한 모든 세부 정보를 지정해줘야 한다.  
`add()`나 `create()`는 이러한 세부사항을 지정하는 방법을 제공하지 않기 때문에 사용할 수 없다.

동일한 이유로 `remove()` 메서드 또한 사용할 수 없다.  
중간 모델에 의해 정의 된 사용자 정의 테이블을 통해 (model1, model2) 쌍의 고유성을 적용하지 않으면 `remove()` 호출은 어떤 중간 모델 인스턴스를 삭제해야하는지에 대한 충분한 정보를 제공하지 않는다.

```python
>>> Membership.objects.create(person=ringo, group=beatles,
...     date_joined=date(1968, 9, 4),
...     invite_reason="You've been gone for a month and we miss you.")
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>, <Person: Ringo Starr>]>
>>> # 아래의 remove() 메서드는 작동하지 않는다.
>>> beatles.members.remove(ringo)

```

하지만, `clear()` 메서드는 모든 many-to-many relationship을 삭제하기 때문에 동작한다.

```python
>>> # 비틀즈 해.체
>>> beatles.members.clear()
>>> # clear 메서드는 intermediate 모델 인스턴스를 삭제한다.
>>> Membership.objects.all()
<QuerySet []>
```

Intermediate 모델의 인스턴스를 작성하여 다대다 관계를 설정하면 쿼리를 실행할 수 있다.

```python
# Find all the groups with a member whose name starts with 'Paul'
>>> Group.objects.filter(members__name__startswith='Paul')
<QuerySet [<Group: The Beatles>]>
```

intermediate 모델의 속성에 대해서도 쿼리를 실행할 수 있다.

```python
# Find all the members of the Beatles that joined after 1 Jan 1961
>>> Person.objects.filter(
...     group__name='The Beatles',
...     membership__date_joined__gt=date(1961,1,1))
<QuerySet [<Person: Ringo Starr]>
```

물론 Membership 모델에 직접적으로 쿼리를 수행할 수도 있다.

```python
>>> ringos_membership = Membership.objects.get(group=beatles, person=ringo)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
```

위와 동일한 정보에 접근하는 또 다른 방법으로는 Person객체에서 many-to-many relationship에 역방향으로 쿼리를 실행하는 것이다.

```python
>>> ringos_membership = ringo.membership_set.get(group=beatles)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
```

### One-to-one relationships

일대일 관계를 정의하기 위해서는 OneToOneField를 사용한다.
어떤 한 객체의 기본 키에서 다른 객체로 확장할 때 사용하면 유용하다.  
예를 들어 "장소" 데이터베이스를 구축했다고 생각하면, "레스토랑" 모델을 생성할 때 필드를 복제하는 방법을 사용하지 않고, OneToOneField Place를 사용할 수 있다.

```python
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return "%s the place" % self.name

class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name

class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):              # __unicode__ on Python 2
        return "%s the waiter at %s" % (self.name, self.restaurant)
```

### Models across files

```python
from django.db import models
from geography.models import ZipCode

class Restaurant(models.Model):
    # ...
    zip_code = models.ForeignKey(
        ZipCode,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
```
다른 app 내에 있는 model과 연결하는 것도 가능하다.

### Field name restrictions

Django는 필드 이름에 2가지 제한사항을 둔다.

1. 파이썬 예약어는 사용할 수 없다.
	
	```python
	class Example(models.Model):
    pass = models.IntegerField() # 'pass' is a reserved word!
    ```

2. 쿼리 조회 구문이 작동하는 방식에 사용되는 더블 언더스코어(\_\_)는 사용할 수 없다.
	
	```python
	class Example(models.Model):
    foo__bar = models.IntegerField() # 'foo__bar' has two underscores!
    ```

### Meta options
`class Meta`를 사용하면, 모델에 메타 데이터를 제공할 수 있다.

```python
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"
```

모델 메타 데이터는 "필드가 아닌 모든 것"이다.  
(위 예시의 정렬 옵션(`ordering`)이나, DB 테이블 이름, 사람이 읽을 수 있는 단일 혹은 복수의 이름(`verbose_name` and `verbose_name_plural`)과 같은)  
생성 시 아무 것도 필요하지 않으며 클래스 메타를 모델에 추가하는 것은 선택 사항이다.  
가능한 모든 메타 옵션의 전체 목록은 모델 옵션 참조에서 찾을 수 있다.


### Model attribute
모델의 가장 중요한 속성은 <b>Manager</b>이다.  
Django 모델 DB 쿼리 연산을 제공하고, DB에서 인스턴스를 검색하는데 사용하는 인터페이스가 Manager이다.

### Model method
모델에 사용자 정의 메서드를 정의하여 row-level의 기능을 object에 추가한다.(즉 하나의 레코드를 관리한다고 생각하자!)  
Manager 메서드는 table 단위의 작업을 수행하기 위한 것이지만, 모델 메서드는 특정 모델 인스턴스에서 작동해야 한다. (한번 더 말하자면 하나의 레코드를 관리한다고 생각하면 편할것 같다.)

```python
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        "Returns the person's baby-boomer status."
        import datetime
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)
```

### Overriding predefined model methods

때때로 `save()` 및 `delete()`를 사용하는 작업 방식을 변경하고 싶은 경우가 있다.  
이 method의 수행 작업을 바꾸기 위해 override를 사용해 자유롭게 변경할 수 있다.  
내장 된 메서드를 재정의하기위한 고전적인 사용 사례는 아래의 예를 통해 살펴보자.

```python
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        do_something()
        super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.
        do_something_else()
```
위와 같이 `save()` 메서드를 override하면, 사용자가 원하는 수행 작업을 추가 할 수 있다.

또한 조건에 따라 저장이 되지 않게 할 수도 있다.

```python
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        if self.name == "Yoko Ono's blog":
            return # Yoko shall never have her own blog!
        else:
            super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.
```
위의 예시에서, Blog 클래스의 인스턴스를 생성할 때, name 속성이 "오노 요코의 블로그"인 경우 저장이 방지된다.

위의 두 예제에서 중요한 점은 superclass 메서드를 호출하는 것이다. super를 이용해 원래의 save 메서드를 호출하여 객체가 DB에 저장될 수 있게 한다.

만약 superclass 메서드를 추가하지 않는다면, 원래 `save()` 메서드의 동작이 작동되지 않아 DB에 데이터를 저장하지 않게된다.


### Model inheritance
Django의 모델 상속은 일반적으로 Python의 클래스 상속과 거의 동일하게 작동한다.  
하지만 기본 클래스가 django.db.models.Model을 서브클래스화 해야한다는 차이점이 있다.

부모 모델이 자체 DB 테이블을 보유할 것인지, 또는 자식 모델을 통해서만 볼 수 있는 공통정보를 보유할 것인지의 여부만 결정하여 작성하면 된다.

### Abstract base classes
Abstract base 클래스는 공통된 정보를 다른 여러 모델에 넣으려 할 때 유용하다.  
기본 클래스를 작성하고, Meta 클래스에 `abstract = True`라는 옵션을 넣어주면 해당 모델은 데이터베이스를 생성하지 않는다. 대신 자식 클래스에 작성된 필드가 추가된다.  
(즉, 모델을 생성할 때 사용할 기본 뼈대를 미리 만들어 둔다고 생각하면 된다.)

```python
from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
```

위의 예제에서, `Student` 모델은 `name`, `age`와 `home_group` 3개의 필드를 가지게 된다.
`CommonInfo` 모델은 보통의 Django 모델처럼 사용될 수 없다. 추상화 모델이므로 DB를 생성할 수 없고 manager가 없어 직접 인스턴스화 하거나 저장할 수 없다.

#### Meta inheritance

```python
from django.db import models

class CommonInfo(models.Model):
    # ...
    class Meta:
        abstract = True
        ordering = ['name']

class Student(CommonInfo):
    # ...
    class Meta(CommonInfo.Meta):
        db_table = 'student_info'
```
위 예제에서 Student의 db_table은 정렬 기준을 따로 설정하지 않아도 ordering =['name']을 갖는다.

#### Related_name & related\_query\_name

```python
from django.db import models

class Base(models.Model):
    m2m = models.ManyToManyField(
        OtherModel,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        abstract = True

class ChildA(Base):
    pass

class ChildB(Base):
    pass
```

위 예시에서, `common.ChildA.m2m` 필드의 역방향 이름은 `common_childa_related`이고, 역방향 쿼리 이름은 `common_childas`이다.  
`common.ChildB.m2m` 필드의 역방향 이름은 `common_childb_related`이고 역방향 쿼리 이름은 `common_childbs`가 된다.  
마지막으로, `rare.ChildB.m2m` 필드의 역 이름은 `rare_childb_related`이고 역방향 쿼리 이름은 `rare_childbs`이다.  
`%(class)s` 및 `%(app_label)s` 부분을 사용하여 related\_name 또는 related\_query\_name을 구성하는 방법은 사용자의 몫이지만 사용하지 않으면 장고는 시스템 검사 (또는 마이그레이션 실행)를 수행 할 때 오류를 발생시킨다.

Inheritance 기본 클래스의 필드에 `related_name` 속성을 지정하지 않은 경우 기본 역방향 이름은 필드를 직접 선언 한 경우와 마찬가지로 `_set`이 하위 클래스의 이름에 붙게된다.  
예를 들어, 위 코드에서 `related_name` 속성을 생략하면 ManyToManyField의 역방향 이름은 ChildA의 경우 `childa_set`이 되고, ChildB 필드의 경우 `childb_set`이 된다.


#### Multi-table inheritance

```python
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
```

Multi-table inheritance에서, 상속하거나 상속받는 모델은 각자의 DB table을 가진다.  
자식 모델에만 있는 데이터는 자식 모델의 DB table에 저장되고, 상속받는 부분은 부모 모델의 DB table에 저장되고 자식 모델은 링크를 가지게 된다. 이때 링크는 자동으로 생성된 OneToOneField를 사용한다.

#### Meta and multi-table inheritance
multi-table inheritance의 경우 각각의 DB table을 가지기 때문에, 자식 모델은 부모 모델의 Meta 클래스를 상속받지 않는 것이 맞다.  

```python
class ChildModel(ParentModel):
    # ...
    class Meta:
        # Remove parent's ordering effect
        ordering = []
```
위의 예시와 같이, Meta class의 ordering을 빈 값으로 지정해 주면, 부모 모델의 것을 상속받지 않는다.

### Proxy models
multi-table 상속을 사용하는 경우 각각의 자식 클래스마다 DB table이 생성된다. 하지만 가끔 부모 모델의 메서드만 재정의 한다던가 새로 추가하고 싶은 경우엔 모델은 상속받으면서, 자식모델은 테이블을 만들 필요가 없는 경우다.  
따라서 부모 클래스만 만든다.

```python
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class MyPerson(Person):
    class Meta:
        proxy = True

    def do_something(self):
        # ...
        pass
```
MyPerson은 Person을 상속받지만, table이 별도로 생성되지 않는다.  
이때, Person과 MyPerson은 같은 데이터를 가진다.(같은 Person 테이블을 사용한다)

```python
>>> p = Person.objects.create(first_name="foobar")
>>> MyPerson.objects.get(first_name="foobar")
<MyPerson: foobar>
```

프록시 모델을 사용하여 모델의 기본 순서를 다르게 정의 할 수도 있다. Person 모델을 항상 정렬하고 싶지 않을때, 프록시를 사용하면 아래의 예제와 같이 last_name을 기준으로 정렬할 수 있다.

```python
class OrderedPerson(Person):
    class Meta:
        ordering = ["last_name"]
        proxy = True
```  
<br>

>프록시는 추상 클래스가 아닌 클래스 하나만을 상속받을 수 있다.

### Multiple inheritance
Django에서도 Python과 마찬가지로 여러 부모 모델에서 상속을 받을 수 있다. 여러 모델에서 특정 이름이 겹쳐서 상속이 되는 경우 (예를 들어 Meta 클래스) 첫 번째 부모 만 사용되며 다른 모든 부모는 무시된다.

```python
class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    ...

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    ...

class BookReview(Book, Article):
    pass
```

여러 모델에서 일반적인 `id` primary key field를 상속받게 되면, error가 발생된다.  
Multiple inheritance를 사용하려면 기본 모델에서 AutoField를 명시적으로 지정해주면 된다.  
(위의 예제에서 `book_id`와 `article_id`)
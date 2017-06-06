# Django
## Model field reference

### Field options

아래에 나열하는 옵션은 필드 유형에서 선택적으로 사용할 수 있다.

#### null  
`null` 옵션이 True인 경우, DB에는 해당 값을 빈 값으로 저장한다.  
(Default = False)

>CharField와 TextField에는 null=True 대신, blank=True 속성을 사용하는 것이 좋다.


#### blank
`null`은 데이터베이스와 관련이 있고, `blank`는 유효성 검사와 관련이 있다. `blank` 속성이 True인 경우, 양식 유효성 검사에서 빈 값을 입력할 수 있다.


#### choices
`choices` 옵션을 사용할 경우, 아래의 예시와 같이 순회가능한(iterable) 2개의 항목을 가진 객체가 필요하다.

```python
YEAR_IN_SCHOOL_CHOICES = (
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
)
```
choices 옵션을 사용하면, form widget은 `text field` 대신 `select box`가 된다.

```python
from django.db import models

class Student(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )

    def is_upperclass(self):
        return self.year_in_school in (self.JUNIOR, self.SENIOR)
```

#### db_column
`db_colum` 옵션을 사용한 경우, DB에 저장될 column의 이름을 지정할 수 있다.  
해당 옵션을 사용하지 않는 경우, 필드의 이름을 사용한다.

#### db_index
`db_index` 옵션이 True인 경우, DB에서 해당 필드를 위한 index를 생성한다.

#### default
`default` 옵션은 해당 필드에 기본값을 부여한다. 호출이 가능한 객체를 사용하면, 새로운 객채가 생성 될 때마다 호출한다.

>기본값으로는 변경이 불가능한 객체만 사용이 가능하다. (model instance, list, set 등은 사용이 불가능하다.)

#### editable
`editable` 옵션이 False인 경우, admin이나 다른 ModelForm에서 표시되지 않는다. 또한 모델 유효성 검사 대상에서 제외된다. 기본값은 True이다.

#### error_messages
`error_messages`옵셔을 사용하면 필드에서 발생시키는 기본 오류 메시지를 override 할 수 있다.

#### help_text
help_text 옵션을 사용하면, form widget에 추가적으로 도움말을 넣을 수 있다.

#### primary_key
`primary_key` 옵션을 아무런 field에도 True로 지정하지 않으면, Django에서 자동으로 primary_key값을 AutoField로 생성한다.

>해당 속성이 True인 경우는 `null=False`, `unique=True`임을 의미한다.  
>하나의 객체는 하나의 primary_key만 가질 수 있다.

#### unique
`unique` 옵션이 True인 경우 해당 field는 테이블 전체에서 고유한 값을 가져야 한다.  
(예를 들자면 ID와 같이)  

>`unique=True`는 index 생성을 의미하므로, `db_index`를 따로 지정할 필요가 없다.


#### unique_for_date
`unique_for_date` 옵션에 DateField 또는 DateTimeField의 이름을 입력하여 field를 생성하면, 해당 Field는 DateField 또는 DateTimeField가 동일한 Field에 대해 unique한 값을 가져야 한다.

예를 들어, unique_for_date="pub_date"인 title field가 있으면, 동일한 title과 동일한 pub_date를 가진 두개의 레코드를 입력할 수 없다.

#### unique_for_month
`unique_for_date`와 비슷하게 해당 옵션을 가지는 field는 month를 기준으로 unique한 값을 가져야 한다.

#### unique_for_year
`unique_for_date`와 비슷하게 해당 옵션을 가지는 field는 year를 기준으로 unique한 값을 가져야 한다.

#### verbose_name
`verbose_name`옵션은 사람이 읽을 수 있는 field의 이름을 지정한다.  
만약 해당 옵션을 지정하지 않으면, field의 이름을 이용해서 자동으로 해당 값을 생성한다.

#### validators
'validators`는 해당 필드의 value에 대해서 검사를 시행한다.

<br>
<hr>
<br>

### Field types

#### AutoField
`class AutoField(**options)`

사용 가능한 ID에 따라 자동으로 증가하는 `IntegerField`이다.

#### BigAutoField
`class BigAutoField(**options)`

64bit 정수를 사용하는 `IntegerField`이다. 숫자의 크기를 제외하고 `AutoField`와 매우 유사하다.

#### BinaryField
`class BinaryField(**options)`

binary 데이터로 저장되는 field.  
오직 byte 할당만 가능하며, binaryfiled queryset에 filtering을 할 수 없고, ModelForm에 포함시킬 수 없다는 제약사항이 있다.

#### BoleanField
`class BooleanField(**options)`

True와 False 값을 가지는 field.  
기본 form widget은 `CheckboxInput`이다.  
만약 null 값을 가질 수 있게 하려면, `NullBooleanField`를 사용해야 한다.
`BooleanField`의 기본값은 default를 설정하지 않은 경우 `None`이다.

#### CharField
`class CharField(max_length=None, **options)`

짧은 string부터 긴 string 값을 가지는 field.  
많은 양의 텍스트인 경우, 해당 필드 대신 `TextField`를 사용한다.  
기본 form widget은 `TextInput`이며, 반드시 `max_length` argument를 지정해야 한다.

#### CommaSeparatedIntegerField
`class CommaSeparatedIntegerField(max_length=None, **options)`  

Comma(`,`)로 구분된 integer field.  
`CharField`와 마찬가지로, 반드시 `max_length` argument를 지정해야 한다.

#### DateField
`class DateField(auto_now=False, auto_now_add=False, **options)`

Python에서 datetime.date 인스턴스로 표현되는 날짜 field.

#### DateTimeField
`class DateTimeField(auto_now=False, auto_now_add=False, **options)`

Python에서 datetime.datetime 인스턴스로 표현되는 Date와 Time field

#### DemicalField
`class DecimalField(max_digits=None, decimal_places=None, **options)`

Python에서 Demical 인스턴스로 나타나는 고정 소수점 이하의 10진수 field.  
`max_digits`와 `demical_place` 두 가지 필수 argument가 있다.  
`max_digits` : 허용 최대 자릿수. `demical_place`보다 크거나 같아야 한다.
`demical_place`: 소수의 자릿수

> 소수점 2자리까지 표현하는 1000미만의 수를 표현하는 예시:  
> `models.DecimalField(..., max_digits=5, decimal_places=2)`


#### DurationField
`class DurationField(**options)`

Python에서 timedelta 인스턴스로 나타나는 기간을 저장하는 field.

#### EmailField
`class EmailField(max_length=254, **options)`

`EmailValidator`를 이용해 입력된 값이 Email 주소인지 유효성을 검사하는 `CharField`

#### FloatField
`class FloatField(**options)`

Python에서 float 인스턴스로 나타나는 부동 소수점 숫자 field.  
기본 form widget은 localize를 False로 지정한 경우 `NumberInput`이며, 그 외의 경우 `TextInput`이다.

#### ImageField
`class ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)`

`FileField`의 모든 특성과 메서드를 상속하지만, 업로드 된 객체가 image인지 유효성을 검사한다.

#### IntegerField
`class IntegerField(**ooptions)`

-2147483648~2147483647까지의 정수를 입력받는 field.  
기본 form widget은 localize가 False인 경우 `NumberInput`이며, 그 외의 경우 `TextInput`이다.

#### GenericIPAddressField
`class GenericIPAddressField(protocol=’both’, unpack_ipv4=False, **options)`

string 형식의 IPv4 또는 IPv6 주소 field.  
기본 form widget은 `TextInput`이다.

#### NullBooleanField
`class NullBooleanField(**options)`

NULL 값을 허용하는 `BooleanField`.  
기본 form widget은 `NullBooleanSelect`이다.

#### PositiveIntegerField
`class PositiveIntegerField(**options)`

0과 2147483647까지 양의 정수를 갖는 `IntegerField`.

#### PositiveSmallIntegerField
`class PositiveSmallIntegerField(**options)`

`PositiveIntegerField`와 비슷하게, 0과 32767까지 양의 정수를 갖는 field.

#### SlugField
`class SlugField(max_length=50, **options)`

`Slug`는 글자, 숫자, 언더스코어(\_) 또는 하이푼(-)만 포함된 짧은 labe이다. 일반적으로 URL에 사용된다.

`CharField`와 마찬가지로 `max_length`를 지정해야 한다.

#### SmallIntegerField
`class SmallIntegerField(**options)`

`IntegerField`와 비슷하지만 -32768부터 32767까지의 정수를 갖는 `IntegerField`

#### TextField
`class TextField(**options)`

큰 텍스트를 가지는 field.  
기본 form widget은 `Textarea`이다.

`max_length`을 지정하면, 자동 생성 form field에 적용된다. 하지만 DB에서는 해당 속성이 지정되지 않는다.  
DB에 해당 속성을 지정하고 싶다면 `CharField`를 사용해야한다.

#### TimeField
`class TimeField(auto_now=Flase, auto_now_add=False, **options)`

Python에서 datetime.time 인스턴스로 나타나는 시간 field.  
`DateField`와 동일한 자동 채우기 옵션을 사용한다.

#### UUIDField
`class UUIDField(**options)`

unique한 식별자를 저장하기 위한 field. Python의 UUID class를 사용한다.  
PostgreSQL에서 사용되면 uuid 데이터 유형에 저장되고, 그 외의 경우 char(32) 유형에 저장된다.

>해당 field는 primary_key 대신 사용할 수 있는 좋은 방법이다.
>
>```python
>import uuid
>from django.db import models
>
>class MyUUIDModel(models.Model):
>id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
>    # other fields
>```

<br>
<hr>
<br>

### Relationship fields

#### ForeignKey
`class ForeignKey(othermodel, ondelete, **options)`

mto relationship을 정의할 때, 해당 class가 어느 모델과 related한 지 알 수 있는 위치 인자가 필요하다.

recursive relationship의 경우, 위치 인자에 'self'를 사용한다.

```python
models.ForeignKey('self', on_delete=models.CASCADE).
```

아직 정의되지 않은 모델과의 관계를 작성해야 하는 경우, 모델 오브젝트 자체가 아닌 모델의 이름을 사용할 수 있다.

```python
from django.db import models

class Car(models.Model):
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.CASCADE,
    )
    # ...

class Manufacturer(models.Model):
    # ...
    pass
```

위의 예시에서 `Manufacturer`는 `Car`보다 아래에서 정의되었다.  
먼저 정의된 `Car`는 `Manufacturer`와의 관계를 정의하기 위해 모델의 이름인 `'Manufacturer'`를 사용하였다.

<br>

```python
#products/model.py

from django.db import models

class AbstractCar(models.Model):
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)

    class Meta:
        abstract = True
```

```python
#production/models.py

from django.db import models
from products.models import AbstractCar

class Manufacturer(models.Model):
    pass

class Car(AbstractCar):
    pass

# Car.manufacturer will point to `production.Manufacturer` here.
```

위와 같이 abstract 모델에 정의된 관계(`Car(AbstractCar)`)에서, abstract 모델(`AbstractCar`)은 구체적인 모델(`Car`)로 서브클래스화 된다. (abstract 모델의 app_label과 관계 없는 경우)

<br>

```python
class Car(models.Model):
    manufacturer = models.ForeignKey(
        'production.Manufacturer',
        on_delete=models.CASCADE,
    )
```
다른 app에서 정의 된 모델을 참조하려면 app_label을 명시적으로 지정해야 한다.  
위의 예제에서, `Car`는 `production`이라는 다른 app에 정의된 `Manufacturer` 모델을 참조한다.

#### Arguments

##### ForeignKey.on_delete
ForeignKey로 참조한 객체가 삭제된 경우, 해당 객체를 어떻게 처리할 지 결정하는 옵션이다.

 - CASCADE : 참조한 객체가 삭제된 경우, 해당 객체도 삭제한다.
 - PROTECT : 참조하는 객체가 있는 경우, 참조된 객체의 삭제를 막는다.
 - SET_NULL : 참조한 객체가 삭제된 경우, 해당 객체의 ForeignKey를 null로 설정한다. (null 옵션이 True인 경우에만)
 - SET_DEFAULT : 참조한 객체가 삭제된 경우, 해당 객체의 ForeignKey를 default 값으로 설정한다. (ForeignKey의 default 값을 먼저 설정해야 한다.)
 - SET() : 참조한 객체가 삭제된 경우, SET()에 전달된 값으로 설정한다.
 - DO_NOTHING : 아무런 행동도 하지 않는다. 만약 DB 백엔드가 참조 무결성을 적용하면 Integrity Error가 발생한다.

##### ForeignKey.limit_choices_to
필드가 ModelForm이나 admin을 이용해 렌더링 될 때, 해당 필드에 대해 사용 가능한 객체를 제한한다. (기본적으로 쿼리셋의 모든 객체를 선택할 수 있다.)  
딕셔너리나 쿼리 오브젝트, 호출가능한 반환값을 주는 딕셔너리와 쿼리 오브젝트를 사용할 수 있다.

```python
staff_member = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={'is_staff': True},
)
```
위의 예제에서, ModelForm의 해당 필드가 is_staff = True인 User만 나열한다.

```python
def limit_pub_date_choices():
    return {'pub_date__lte': datetime.date.utcnow()}

limit_choices_to = limit_pub_date_choices
```
위의 예제에서 `limit_choice_to`가 쿼리 오브젝트를 반환하면, ModelAdmin에서 필드가 `raw_id_fields`에 나열되지 않은 경우에 admin이 사용할 수 있는 선택 항목을 제한한다.


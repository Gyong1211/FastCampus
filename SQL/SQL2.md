# SQL

## 주요 명령어

### SELECT TOP

```sql
SELECT TOP number|percent column_name(s)
FROM table_name
WHERE condition;
```
특정 개수(number) 혹은 전체 데이터에서의 비율(percent)로 출력할 레코드의 개수를 선택할 수 있다.

--

### 











### LIKE Operator
특정 문자열을 포함한 레코드를 찾을 때 사용한다.

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name LIKE pattern;
```


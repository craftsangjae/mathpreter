# Latex 기반 수식 인터프리터, Mathpreter

## Goal

> Latex 문법과 유사하게 이루어진 수식 전용 인터프리터

## Examples

1. 사칙 연산

```shell
>> 1 + 3^3 * 5 + 2/5 
136.4
```

2. 지수 함수 / 로그 함수

```shell
>> 5*\exp^3
100.42768461593832 

>> \log_2 5
2.321928094887362
```

3. sum / prod 연산

````shell
>> \sum_{k=1}^{5} {k+5}
40

>> \prod_{k=1}^{3} {2*k}
48
````

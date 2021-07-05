# Text_mining__project
본 프로젝트에서는 텍스트 마이닝 기법 중 하나인 TF-IDF 가중치를 이용하여 제공된 트위터 데이터들을 분석하고 개별 트윗마다 핵심어를 추출함으로써 트윗들 사이의 유사도를 구할
수 있는 프로그램을 작성한다. 또한 트위터 분석을 위해 비정형 데이터를 다루기 쉬운 NoSQL 기반 데이터베이스인 MongoDB를 사용함으로써 NoSQL 데이터베이스의 사용법을 익힐 뿐 아니라 관계형 데이터베이스와 NoSQL 데이터베이스간의 차이점을 인식하는 것을 목적으로 한다.

# Environment
1. OS : Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-193-generic x86_64)
2. tweet 문서 필요

# How to run
```
> python DBprj#3_20160641.py
```

# 프로그램 수행 예시

## 1) 형태소 분석 및 불용어 처리
4. MorpAnalysis를 선택하면 모든 트윗에 대해 형태소열을 데이터베이스에 저장하게 된다. 이후 사용자로부터 입력받은 Id를 기준으로 해당 Id의 형태소들을 출력해준다. 

![image](https://user-images.githubusercontent.com/70252973/123907005-29947a00-d9b0-11eb-85e1-741c4017a016.png)

## 2) Word Count 구하기
1. WordCount를 선택하면 모든 트윗에 대해 포함되어 있는 고유한 개별 단어들의 빈도수를 측정한다. 이후 사용자로부터 입력 받은 id를 기준으로 해당 id의 word_count 리스트를 출력해준다. 

![image](https://user-images.githubusercontent.com/70252973/123907036-36b16900-d9b0-11eb-82d3-3519bee413e2.png)

## 3) TF-IDF 구하기

5. TF-IDF를 선택하면 트윗의 Object ID를 입력받게 된다. 이후 입력 받은 id 를 기준으로 해당 id의 단어들의 tf-idf 가중치 상위 10개를 출력한다. 이는 6. Calculating TF-IDF 메뉴를 완료한 후 수행되어야 한다.
![image](https://user-images.githubusercontent.com/70252973/123907082-4b8dfc80-d9b0-11eb-9131-3c0dd4ff2fb1.png)

## 4) 문서 유사도 구하기
3. Similarity를 선택하면 비교할 두 개의 Object ID를 입력받게 된다. 이후 입력받은 두개의 id를 기준으로 해당 id의 문서간의 유사도를 구하여 출력하게 된다. 

![image](https://user-images.githubusercontent.com/70252973/123907100-55affb00-d9b0-11eb-9032-17483300ab19.png)


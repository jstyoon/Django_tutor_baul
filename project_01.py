
# 데이터 
my_station = ['야탑', '모란', '이매', '선릉', '한티', '왕십리']

# 주어진 데이터를 반복문으로 모두 출력하는 station_list 함수 정의
def station_list(station_list):
    for station in station_list:
        print(station)
        

station_list(my_station)  # station_list 함수 작성

# 주어진 데이터를 반복문과 조건문을 사용하여
# '선릉'만 출력 하는 station_point 함수 정의
def station_point(station_list):
    for station in station_list:
        if station == '선릉':
            print(station)
            

station_point(my_station)  # station_point 함수 작성

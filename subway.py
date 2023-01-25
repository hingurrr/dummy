#지하철
import asyncio
import pyodide
from pyodide.http import pyfetch, FetchResponse
from typing import Optional, Any
import json
import datetime
import random
import time
tt =Element('section_time')
token_html = Element('token')
bt_1 = Element('add_text')
count_list = []
output_text = Element("output_text")
count_num = 1
close_token = 0
error_code = Element("error_code")
time_counter = Element("time_counter")
station_info = "중곡"
이용횟수 = 48
num_time =1


# html 에서 생성한 ID "add_text" 의 버튼이 눌렸을 때 호출될 함수

async def time_count(num_time):
       
    for count_num in range(num_time,0,-1):
        time_counter.element.innerText = (f"{count_num}초 후 {station_info}역 정보를 가져옵니다.")
        if count_num == 1:
            break
        await asyncio.sleep(1)
        

def close_act(*args:Any): 
    global close_token
    close_token =1
    global station_info
    station_info = ""
    
    
def function_add_text(*args:Any):
# output_text 객체의 text 값을 input_text의 값으로 지정
   
    global close_token
    close_token = 0
    global station_info
    station_info = "길동"
    global count_num
    count_num += 1
    if count_num%2!=0:
        station_info = "중곡"
        next_data="길동"
    output_text.element.innerText =(station_info)

    if count_num%2==0:
        next_data = "중곡"
    bt_1.element.innerText =(f"{next_data}역 확인하기")

    


# 함수가 실행된 후 input_text의 값을 초기화

async def req_json(url):
    now = datetime.datetime.now()
    list = {'0': station_info + '역 진입', '1': station_info + '역 도착', '2': station_info + '역 출발', '3': '전역출발',
                '4': '전역진입', '5': '전역도착', '99': '운행중'}
    find_data = {'길동': '0', '중곡': '1','군자(능동)':'1'}
    try:
        response = await pyodide.http.pyfetch(url, method='GET')

        if 이용횟수 < 48:
    # response = await pyfetch(url="https://jsonplaceholder.typicode.com/todos/1", method="GET")
            out_data = await response.json()
            #파싱
            
            json_data = out_data['realtimeArrivalList']
            
            for x in json_data:
                trainLineNm = x['trainLineNm']  # 도착지방면
                location = trainLineNm.find('-')
                trainLineNm = trainLineNm[0:location - 1]
                subwayList = x['subwayList']  # 호선 구분 100+x
                statnNm = x['statnNm']  # 지하철역명
                
                ordkey = x[
                    'ordkey']  # 도착예정열차순번(상하행코드(1자리), 순번(첫번째, 두번째 열차 , 1자리), 첫번째 도착예정 정류장 - 현재 정류장(3자리), 목적지 정류장, 급행여부(1자리))
                barvlDt = x['barvlDt']  # 도착남은시간 (단위 : 초)
                btrainNo = x['btrainNo']  # 열차번호
                arvlMsg2 = x['arvlMsg2']  # 도착예정
                arvlMsg3 = x['arvlMsg3']  # 현재위치
                arvlCd = x['arvlCd']  # (0:진입, 1:도착, 2:출발, 3:전역출발, 4:전역진입, 5:전역도착, 99:운행중)
                recptnDt = x['recptnDt']  # 정보 조회시간
                arvlCd = list[arvlCd]

                year = recptnDt[0:4]
                month = recptnDt[5:7]
                day = recptnDt[8:10]
                hour = recptnDt[11:13]
                min = recptnDt[14:16]
                sec = recptnDt[17:19]
                past = datetime.datetime(int(year), int(month), int(day), int(hour), int(min), int(sec))
                num_subway = ordkey[1:2]
                diff = now - past
                # seconds 통해 시간 차이 정보를 초 단위로 가져올 수 있다.
                
                if ordkey[0:1] == find_data[station_info]:
                    if num_subway=="1":
                    # 상행
                    
                        output = "\n"+ trainLineNm, num_subway + '번째열차\n남은 예정시간 :', str(int(barvlDt) - diff.seconds) + "초\n",arvlMsg2, "\n현재위치 :", arvlMsg3, "\n열차 상황 :", arvlCd
                        left_time = str(int(barvlDt) - diff.seconds) + "초"
                        left_time_1 = Element('left_time')
                        left_time_1.element.text =left_time
                        # st_info = Element('station_info').element.text =station_info
                        arvlCd_html = Element('arvlCd').element.text =arvlCd
                        arvlMsg3_html = Element('arvlMsg3').element.text =arvlMsg3
                        tt.element.innerText =(arvlMsg2)          
        
    except Exception as e:
        error_code.element.innerText =(f"json err: {str(e)}")
def counting_used():
    day = datetime.datetime.now().day
    try:
        if count_list[0]==day:  
            change_x = count_list[1]
            change_x += 1
            count_list[1] = change_x           
            return count_list[1]
        elif count_list[0]!=day:
            del count_list[1]
            del count_list[0]
            count_list.append(day)
            count_list.append(1)
            return count_list[1]
    except IndexError as e:
        count_list.append(day)
        count_list.append(1)
        
        return count_list[1]

async def 지하철():
    import datetime
    
    api_token = counting_used()
   
    if api_token >= 1000:
        api_key = '7268667a6a72757032314d4e775141'
    
    else:
        api_key = "73634352447275703130335464717766"
    
    count = 0
    
    
    url = f'http://swopenAPI.seoul.go.kr/api/subway/{api_key}/json/realtimeStationArrival/0/10/{station_info}'
    error_code.element.innerText = url
    
    global 이용횟수
    global close_token
    await req_json(url)
    이용횟수 +=1
    if 이용횟수 >48:
        close_token = 1
    else:
        global num_time
        num_time = 5
        


async def cl():
    global 이용횟수
    이용횟수 = 0
  
    if token_html.element.innerText != "종료":
        token_html.element.innerText =("종료")
        tt.element.innerText =("서비스를 이용하시려면 버튼을 눌러주세요.")
        time_counter.clear()
        Element('left_time').clear()
        Element('arvlCd').clear()
        Element('arvlMsg3').clear()
        Element('error_code').clear()
        bt_1.element.innerText = ('시작')
        
    
    
    
async def run_prec():
    token_html.element.innerText =("실시간")
    try:
        await 지하철()
        await time_count(num_time)
        
    except Exception as e:
        error_code.element.innerText =(f"지하철 오류 {str(e)}{close_token}")
        await asyncio.sleep(1)

async def main():
    try:
        while True:
            await asyncio.sleep(0.3)
           
            if close_token == 1:
                await cl()   
                  
            elif close_token == 0:
                await run_prec()
    except Exception as e:
        error_code.element.innerText =(f"main error{str(e)}")

asyncio.ensure_future(main())
# run_code()
# 지하철이 끝날 때까지 기다림
                       # 이벤트 루프를 닫음 
# # asyncio.ensure_future(지하철())


 
####

#지하철
import asyncio
from pyodide.http import pyfetch, FetchResponse
from typing import Optional, Any
import json
import datetime

async def request(url: str, method: str = "GET", body: Optional[str] = None,
                  headers: Optional[dict[str, str]] = None, **fetch_kwargs: Any) -> FetchResponse:
    now = datetime.datetime.now()
    station_info = "길동"
    list = {'0': station_info + '역 진입', '1': station_info + '역 도착', '2': station_info + '역 출발', '3': '전역출발',
                '4': '전역진입', '5': '전역도착', '99': '운행중'}
    """
    Async request function. Pass in Method and make sure to await!
    Parameters:
        url: str = URL to make request to
        method: str = {"GET", "POST", "PUT", "DELETE"} from `JavaScript` global fetch())
        body: str = body as json string. Example, body=json.dumps(my_dict)
        headers: dict[str, str] = header as dict, will be converted to string...
            Example, headers=json.dumps({"Content-Type": "application/json"})
        fetch_kwargs: Any = any other keyword arguments to pass to `pyfetch` (will be passed to `fetch`)
    Return:
        response: pyodide.http.FetchResponse = use with .status or await.json(), etc.
    """
    find_data = {'길동': '0', '중곡': '1','군자(능동)':'1'}
    kwargs = {"method": method, "mode": "cors"}  # CORS: https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
    if body and method not in ["GET", "HEAD"]:
        kwargs["body"] = body
    if headers:
        kwargs["headers"] = headers
    kwargs.update(fetch_kwargs)

    response = await pyfetch(url=url, method=method)
    # response = await pyfetch(url="https://jsonplaceholder.typicode.com/todos/1", method="GET")
    output = await response.json()

    
    #파싱
    
    json_data = output['realtimeArrivalList']
    
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
            # 상행
            
            output = "\n"+ trainLineNm, num_subway + '번째열차\n남은 예정시간 :', str(int(barvlDt) - diff.seconds) + "초\n",arvlMsg2, "\n현재위치 :", arvlMsg3, "\n열차 상황 :", arvlCd
            left_time = str(int(barvlDt) - diff.seconds) + "초"
            left_time_1 = Element('left_time')
            left_time_1.element.text =left_time
            arvlCd_html = Element('arvlCd').element.text =arvlCd
            arvlMsg3_html = Element('arvlMsg3').element.text =arvlMsg3
            arvlMsg2_html = Element('arvlMsg2').element.text =arvlMsg2
         
    
    
    return output

async def 지하철():
    import datetime
    
    api_key = "73634352447275703130335464717766"
    count = 0
    station_info = '길동'
    
    url = 'http://swopenAPI.seoul.go.kr/api/subway/' + api_key + '/json/realtimeStationArrival/0/10/' + station_info
    task1 = asyncio.create_task(request(url=url,method='GET'))
    await task1


while True:
    지하철()
    time.sleep(1) 




 
####

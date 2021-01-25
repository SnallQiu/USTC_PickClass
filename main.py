# -*- coding: utf-8 -*-
# @Time    : 2021/1/25 16:00
# @Author  : qiuqc@mail.ustc.edu.cn
# @FileName: ustc抢课.py

import requests
import threading
import time, json
from config import *
url = "https://jw.ustc.edu.cn/ws/for-std/course-select/add-request"
drop_url = 'https://jw.ustc.edu.cn/ws/for-std/course-select/add-drop-response'
all_class_url = "https://jw.ustc.edu.cn/ws/for-std/course-select/addable-lessons"

class_dict = {}

sss = """authority: jw.ustc.edu.cn
method: POST
path: /ws/for-std/course-select/add-request
scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
cache-control: no-cache
content-length: 98
content-type: application/x-www-form-urlencoded; charset=UTF-8
cookie: {}
origin: https://jw.ustc.edu.cn
pragma: no-cache
referer: https://jw.ustc.edu.cn/for-std/course-select/{}/turn/381/select
sec-ch-ua: "Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"
sec-ch-ua-mobile: ?0
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36
x-requested-with: XMLHttpRequest""".format(cookie, student_id)
dp_row_header = """authority: jw.ustc.edu.cn
method: POST
path: /ws/for-std/course-select/add-drop-response
scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
cache-control: no-cache
content-length: 63
content-type: application/x-www-form-urlencoded; charset=UTF-8
cookie: {}
origin: https://jw.ustc.edu.cn
pragma: no-cache
referer: https://jw.ustc.edu.cn/for-std/course-select/{}/turn/381/select
sec-ch-ua: "Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"
sec-ch-ua-mobile: ?0
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36
x-requested-with: XMLHttpRequest""".format(cookie, student_id)

def deal_row(s):
    return {i.split(": ")[0].strip(): i.split(": ")[1] for i in s.split("\n")}

headers = deal_row(sss)
dp_headers = deal_row(dp_row_header)

def get_allclass():
    c = requests.post(all_class_url, headers=headers, data={"turnId":"381", "studentId":student_id})
    all_data = json.loads(c.text)

    for each in all_data:
        class_dict[each["code"]] = each["id"], each["course"].get("nameZh", "")

get_allclass()

def ppp(course_id, index):
    while True:
        form_d = """studentAssoc: {}
        lessonAssoc: {}
        courseSelectTurnAssoc: 381
        scheduleGroupAssoc: 
        virtualCost: 0""".format(student_id, class_dict[course_id][0])
        dp_form_row = """studentId: {}
        requestId: {}"""
        form_data = deal_row(form_d)
        c = requests.post(url, headers=headers, data=form_data)
        dp_form_data = deal_row(dp_form_row.format(student_id, c.text))
        d = requests.post(drop_url, headers=dp_headers, data=dp_form_data)
        data = json.loads(d.text)
        if data["success"]:
            print("恭喜你， {}选课成功！！！！".format(class_dict[course_id][1]))
            return True
        else:
            print("{}选课失败 TAT : {}".format(class_dict[course_id][1], data["errorMessage"]["text"]))
            time.sleep(hz)


if __name__ == "__main__":
    threads = []
    for i in range(len(course_ids)):
        task = threading.Thread(target=ppp, args=(course_ids[i], i, ))
        threads.append(task)
        task.start()
    for task in threads:
        task.join()
    print("全部抢完")



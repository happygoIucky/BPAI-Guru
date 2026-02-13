# coding:utf-8
# Install Dependency, pip3 install --upgrade byteplus-sdk
# Documentation : https://docs.byteplus.com/en/docs/byteplus-vision/dreamactor-m2-0-introduction

from __future__ import print_function
import time
import json
from byteplus_sdk.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('') # Enter your own Access Key (AK)
    visual_service.set_sk('') # Enter your own Secret Key (SK)
    
    # Request Body (Check interface documentation and copy the required parameters) 
    # https://docs.byteplus.com/en/docs/byteplus-vision/dreamactor-m2-0-api-document
    req_body = {
        "req_key": "dreamactor_m20_gen_video_cvtob", # 
        "image_urls": ["https://sf16-resources.bytepluscdn.com/obj/byteplus-public-aiso/cloud-universal-doc/upload_3c9a3a3a30ad420105024b6d6d882fee.jpeg"],
        "video_url": "https://sf16-resources.bytepluscdn.com/obj/byteplus-public-aiso/cloud-universal-doc/upload_1245a943232e4a7801f3e4dfba953ba5.mp4",
        #"cut_result_first_second_switch": True,  #Whether to crop the first second of the output video (there is a 1-second transition at the beginning of the output video; this parameter can be used to crop it)
    }
    resp = visual_service.cv_sync2async_submit_task(req_body)
    print(resp)

    # Polling query section
    print("----- polling task status -----")
    task_id = resp['data']['task_id']
    print(f"Task ID: {task_id}")
    while True:
        get_result = visual_service.cv_sync2async_get_result({"req_key": "dreamactor_m20_gen_video_cvtob", "task_id": task_id})     # 
        #print(get_result)
        status = get_result['code']
        if status == 10000:
            task_status=get_result['data']['status']
            if task_status == "done":
                print("----- task succeeded -----")
                print(f"Result: {json.loads(get_result['data']['resp_data'])['video_url']}")
                #resp_data is a serialized JSON string. The resp_data.video_url indicates the generated video URL.
                break
            elif task_status == "generating" or task_status == "in_queue":
                print(f"Current status: {task_status}, Retrying after 5 seconds...")
                time.sleep(5)
                continue
            else:
                print(f"Current status: {task_status}")
                break
        else:
            print(f"----- Task failed with error: {status} -----")
            break

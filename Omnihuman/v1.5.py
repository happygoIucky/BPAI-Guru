# coding:utf-8
# install this dependency , pip3 install --upgrade byteplus-sdk
# Documentation: https://docs.byteplus.com/en/docs/byteplus-vision/omnihuman1_5overview

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
    # https://docs.byteplus.com/en/docs/byteplus-vision/omnihuman-video_generation
    req_body = {
        "req_key": "realman_avatar_picture_omni15_cv", # 
        "image_url": "https://sf16-resources.bytepluscdn.com/obj/byteplus-public-aiso/cloud-universal-doc/upload_4186eb9fd131c774f2733851d387cf61.PNG",
        "audio_url": "https://sf16-resources.bytepluscdn.com/obj/byteplus-public-aiso/cloud-universal-doc/upload_bbbec653ed512bac17224f76249321b3.MP3",
        #"mask_url": "https://xxxxx;...", #List of mask image URLs to specify a specific subject in the image to speak. Separate multiple mask image URLs with semicolons (;) if there are any.
        # // You can obtain the subject’s mask image via Step 2: Subject Detection and pass it in using string type.
        # // Step 2 doc: https://docs.byteplus.com/en/docs/byteplus-vision/omnihuman-subject_detection
        
        #"seed": -1, #Random seed (used as the basis for determining the initial diffusion state). Default value: -1 (random).
        #"prompt": "A man is speaking", #Text prompt for video generation. Only supports Chinese, English, Japanese, Korean, Mexican Spanish, and Indonesian.
        #"pe_fast_mode": False, #When enabled, it will speed up generation by sacrificing some effects. Default Value: False (fast mode is disabled by default)
        #"output_resolution": 720, #Output video resolution. Default value: 1080. Optional values: 720, 1080.
        #"callback_url": "https://YOUR-CALLBACK-URL"    #Callback notification address for the results.
        #"callback_auth_info": "YOUR-CALLBACK-AUTH-INFO" #Reserved fields for callback authentication purposes.
    }
    resp = visual_service.cv_submit_task(req_body)
    #print(resp)

    # Polling query section
    print("----- polling task status -----")
    task_id = resp['data']['task_id']
    print(f"Task ID: {task_id}")
    while True:
        get_result = visual_service.cv_get_result({"req_key": "realman_avatar_picture_omni15_cv", "task_id": task_id})     # 
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

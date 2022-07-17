import requests

base_url = "http://127.0.0.1:5000/"

# task 1
URL = f"{base_url}page/"
body = {"name": "OurMedia France"}
result = requests.post(url=URL, json=body)

print("Task 1")
print("OurMedia France page has been created")
print(f"API response : \n {result.text}")


# task 2
URL = f"{base_url}video/"
our_media_page_id = result.json()['id']

print("Task 2")
body_video_a = {"title": "video A", "page_id": our_media_page_id}
result_a = requests.post(url=URL, json=body_video_a)
print("Video A has been created")
print(f"API response : \n {result_a.text}")

body_video_b = {"title": "video B", "page_id": our_media_page_id}
result_b = requests.post(url=URL, json=body_video_b)
print("Video B has been created")
print(f"API response : \n {result_b.text}")


# task 3
URL = f"{base_url}videos_insights/"
video_id_a = result_a.json()['id']
video_id_b = result_b.json()['id']

body_video_insight = {
        "videos_insights": [
            {
                "video_id": video_id_a,
                "likes": 10,
                "views": 20
            },
            {
                "video_id": video_id_b,
                "likes": 30,
                "views": 600
            }
        ]
    }
result = requests.post(url=URL, json=body_video_insight)

print("Task 3")
print("Videos insights have been created")
print(f"API response : \n {result.text}")


# task 4
URL = f"{base_url}video/{video_id_b}"
result = requests.delete(url=URL)

print("Task 4")
print("Video B has been deleted")
print(f"API response : \n {result.text}")

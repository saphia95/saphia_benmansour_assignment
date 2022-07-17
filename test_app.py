import requests
import unittest
import sqlite3
import os

base_url = "http://127.0.0.1:5000/"


def get_connection_setup():
    database_test_name = 'database.db'
    os.system(f"python init_db.py {database_test_name}")
    conn = sqlite3.connect(database_test_name)
    conn.row_factory = sqlite3.Row
    return conn


class TestPages(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection_setup()

    def test_create_page(self):
        URL = f"{base_url}page/"
        name = "OurMedia France"
        body = {"name": name}
        result = requests.post(url=URL, json=body)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()['id'], 1)
        self.assertEqual(result.json()['name'], name)


class TestVideos(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection_setup()

    def test_create_video_with_existing_page(self):

        # create page 1
        URL = f"{base_url}page/"
        name = "OurMedia France"
        body = {"name": name}
        requests.post(url=URL, json=body)

        # create video in page 1
        URL = f"{base_url}video/"
        title = "video A"
        page_id = 1

        body_video_a = {"title": title, "page_id": page_id}
        result = requests.post(url=URL, json=body_video_a)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()['title'], title)
        self.assertEqual(result.json()['page_id'], 1)

    def test_create_video_without_page_fail(self):
        URL = f"{base_url}video/"
        title = "video A"
        page_id = 1

        body_video_a = {"title": title, "page_id": page_id}
        result = requests.post(url=URL, json=body_video_a)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.text, f'Page id {page_id} do not exist')

    def test_delete_video(self):

        # create page 1
        URL = f"{base_url}page/"
        name = "OurMedia France"
        body = {"name": name}
        requests.post(url=URL, json=body)

        # create video
        URL = f"{base_url}video/"
        title = "video A"
        page_id = 1

        body_video_a = {"title": title, "page_id": page_id}
        result = requests.post(url=URL, json=body_video_a)
        video_id = result.json()['id']

        # delete video
        URL = f"{base_url}video/{video_id}"
        requests.delete(url=URL)

        cursor = self.conn.cursor()

        result = cursor.execute(f"SELECT id from videos;")
        videos_ids = [id[0] for id in result]

        self.assertTrue(video_id not in videos_ids)


class TestVideoInsights(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection_setup()

        # create page
        URL = f"{base_url}page/"
        name = "OurMedia France"
        body = {"name": name}
        result = requests.post(url=URL, json=body)
        page_id = result.json()['id']

        # create video
        URL = f"{base_url}video/"
        title = "video A"

        body_video_a = {"title": title, "page_id": page_id}
        result = requests.post(url=URL, json=body_video_a)
        self.video_id = result.json()['id']

    def test_create_video_insight(self):
        likes = 10
        views = 20

        body_video_insight = {
            "videos_insights": [
                {
                    "video_id": self.video_id,
                    "likes": likes,
                    "views": views
                }
            ]
        }
        URL = f"{base_url}videos_insights/"
        result = requests.post(url=URL, json=body_video_insight)

        video_insight = result.json()['videos_insights'][0]

        self.assertEqual(result.status_code, 200)
        self.assertEqual(video_insight['id'], self.video_id)
        self.assertEqual(video_insight['likes'], likes)
        self.assertEqual(video_insight['views'], views)


if __name__ == '__main__':
    unittest.main()

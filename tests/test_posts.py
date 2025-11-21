import unittest
from datetime import datetime as dt

from app import create_app, db
from app.posts.models import Post

class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        with self.app.app_context():
            response = self.client.post("/posts/create", data={
                "title": "My first post",
                "content": "This is TDD!",
                "category": "news",
                "is_active": "y",
                "publish_date": dt.utcnow().strftime("%Y-%m-%dT%H:%M")
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            # Перевіряємо, що пост створено
            post = db.session.query(Post).filter_by(title="My first post").first()
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD!")
            self.assertEqual(post.category, "news")
            self.assertTrue(post.is_active)

from bot_config import NUMBER_OF_USERS, MAX_LIKES_PER_USER, MAX_POST_PER_USER
from typing import NamedTuple
import requests
import random
import string
import json

HOST = "http://localhost:8000/"
REGISTER_URL = HOST + "register/"
CREATE_POST_URL = HOST + "post/"
LIKE_ANALYTICS = HOST + "analytics/"


class User(NamedTuple):
    username: str
    token: str


def main():
    print("Creating users...")
    users = signup(NUMBER_OF_USERS)
    print("-" * 100)
    print("Created users:", ", ".join(x.username for x in users))
    print("-" * 100)
    print("Posting...")
    posts = generate_post(users, MAX_POST_PER_USER)
    print(f"Created {len(posts)} posts")
    print("-" * 100)
    print("Liking...")
    generate_likes(posts, users, MAX_LIKES_PER_USER)

    print("-" * 100)
    print("Total post liked:", total_likes())


def randname():
    return randstr(random.randint(4, 6))


def randstr(length):
    letters = string.ascii_lowercase
    result = "".join(random.choice(letters) for i in range(length))

    return result


def signup(n):
    users = []
    for i in range(n):
        try:
            user_token = _signup()
            users.append(User(*user_token))
        except AssertionError:
            pass

    return users


def total_likes():
    headers = {"Content-Type": "application/json"}
    resp = requests.get(LIKE_ANALYTICS, headers=headers)
    resp_body = resp.json()

    return len(resp_body)


def _signup():
    data = {"username": randname(), "password": randstr(8)}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(REGISTER_URL, headers=headers, data=json.dumps(data))

    assert resp.status_code == 201

    resp_body = resp.json()

    return (resp_body.get("user").get("username"), resp_body.get("access"))


def generate_post(users: [User], n: int):
    posts = []
    for user in users:
        for i in range(random.randint(1, n)):
            post_id = create_post(user.token)
            posts.append(post_id)

    return posts


def create_post(token: str):
    data = {"title": randstr(10), "text": randstr(10)}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    resp = requests.post(CREATE_POST_URL, headers=headers, data=json.dumps(data))
    resp_body = resp.json()
    return resp_body.get("id")


def generate_likes(posts: [int], users: [User], n: int):
    for user in users:
        for i in range(random.randint(1, n)):
            random_post = random.choice(posts)
            print("Liking post:", random_post)
            like_post(user.token, random_post)


def like_post(token, id):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    requests.post(HOST + f"posts/{id}/like/", headers=headers)


if __name__ == "__main__":
    main()

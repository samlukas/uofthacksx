import datetime
import firebase_admin
from firebase_admin import credentials, db
import uuid

cred = credentials.Certificate("firebase_certificate/certificate.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://uoftthacksx-default-rtdb.firebaseio.com/'})


def create_thread(thread_name: str) -> str:
    """Create a new thread with a random ID, return thread ID
    """

    ref = db.reference('/threads')
    thread_ref = ref.child(thread_name)
    thread_ref.set({'thread_name': thread_name, 'time': str(datetime.datetime.now())})

    return thread_name


def create_post(username: str, post_text: str, thread_id: str):
    """Create a new post at the given thread ID, return post ID
    """

    ref = db.reference('/threads')
    thread_ref = ref.child(thread_id)
    posts_ref = thread_ref.child('posts')

    posts_ref.push().set({
        'username': username,
        'message': post_text,
        'time': str(datetime.datetime.now())
    })


def retrieve_posts(thread_id: str):
    """Retrieve all the posts associated with the thread_id
    """

    ref = db.reference('threads/' + thread_id + '/posts')


    return ref.get()


def retrieve_threads():
    """Retrieve all currently stored threads
    """

    ref = db.reference('threads')

    return ref.get()

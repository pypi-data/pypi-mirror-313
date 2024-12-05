from mmisp.db.models.post import Post


def generate_post() -> Post:
    return Post(
        date_created="2023-11-16 00:33:46",
        date_modified="2023-11-16 00:33:46",
        user_id=1,
        contents="my comment",
        post_id=0,
        thread_id=1,
    )

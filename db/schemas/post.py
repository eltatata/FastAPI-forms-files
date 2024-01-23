def post_schema(post) -> dict:
    return {
        "id": str(post["_id"]),
        "name": post["name"],
        "description": post["description"],
        "filename_server": post["filename_server"]
    }


def posts_schema(posts) -> list:
    return [post_schema(post) for post in posts]
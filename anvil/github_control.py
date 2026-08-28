from dataclasses import dataclass


@dataclass(frozen=True)
class GithubMessage:
    comment_id: int
    body: str


def parse_comments(payload: list[dict[str, object]], after_id: int) -> list[GithubMessage]:
    messages = []
    for item in payload:
        comment_id = int(item["id"])
        body = str(item.get("body", ""))
        if comment_id > after_id and body.startswith("CGPT_"):
            messages.append(GithubMessage(comment_id, body))
    return sorted(messages, key=lambda item: item.comment_id)

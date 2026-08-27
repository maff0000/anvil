def clean_tags(tags: list[str]) -> list[str]:
    return [tag.strip() for tag in tags if tag]

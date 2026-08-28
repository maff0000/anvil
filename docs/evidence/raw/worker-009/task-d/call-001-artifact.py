def escape_markdown_text(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Input must be a string")
    
    result = value.replace('\\', '\\\\')
    for char in '*_`[]()#':
        result = result.replace(char, '\\' + char)
    return result

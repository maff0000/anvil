def escape_markdown_text(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Expected str")
    
    # Escape backslashes first to prevent double-escaping
    value = value.replace("\\", "\\\\")
    
    # Escape specific markdown characters: *, _, `, [, ], (, ), #
    for char in ['*', '_', '`', '[', ']', '(', ')', '#']:
        value = value.replace(char, "\\" + char)
        
    return value

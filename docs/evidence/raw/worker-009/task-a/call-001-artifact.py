def normalize_model_identifier(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Input must be a string")
    
    normalized = " ".join(value.split())
    
    if not normalized:
        raise ValueError("Empty normalized value")
        
    return normalized

"""
Core functionality for text segmentation using Jina API
"""

import os
import requests
from typing import List, Dict, Union, Optional

class SegmentationError(Exception):
    """Custom exception for segmentation errors"""
    pass

def _get_api_key() -> str:
    """Get Jina API key from environment variable"""
    api_key = os.getenv('JINA_API_KEY')
    if not api_key:
        raise SegmentationError(
            "JINA_API_KEY environment variable not set. "
            "Please set it with your API key from Jina."
        )
    return api_key

def _call_jina_api(text: str, max_chunk_size: int) -> Dict:
    """
    Call Jina API to segment text
    
    Args:
        text: The text to segment
        max_chunk_size: Maximum size for each chunk in tokens
        
    Returns:
        Dict containing API response
        
    Raises:
        SegmentationError: If API call fails
    """
    url = 'https://segment.jina.ai/'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_get_api_key()}"
    }
    data = {
        "content": text,
        "return_chunks": True,
        "max_chunk_length": max_chunk_size
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise SegmentationError(f"API call failed: {str(e)}")

def _optimize_chunks(result: Dict, max_chunk_size: int) -> List[Dict[str, Union[str, int]]]:
    """
    Optimize chunks by merging smaller segments while respecting max size
    
    Args:
        result: API response containing chunks and positions
        max_chunk_size: Maximum allowed chunk size in tokens
        
    Returns:
        List of dictionaries, each containing 'text' and 'tokens' keys
    """
    if not result or 'chunks' not in result or 'chunk_positions' not in result:
        return []
    
    chunks = result['chunks']
    positions = result['chunk_positions']
    optimized = []
    
    if not chunks:
        return []
    
    current_chunk = {
        'text': chunks[0],
        'tokens': positions[0][1] - positions[0][0]
    }
    
    for i in range(1, len(chunks)):
        next_tokens = positions[i][1] - positions[i][0]
        if current_chunk['tokens'] + next_tokens <= max_chunk_size:
            current_chunk['text'] = current_chunk['text'] + chunks[i]
            current_chunk['tokens'] += next_tokens
        else:
            optimized.append(current_chunk)
            current_chunk = {
                'text': chunks[i],
                'tokens': next_tokens
            }
    
    optimized.append(current_chunk)
    return optimized

def segment_text(text: str, max_chunk_size: Optional[int] = 1500) -> List[Dict[str, Union[str, int]]]:
    """
    Segment text into chunks using Jina API
    
    Args:
        text: The text to segment
        max_chunk_size: Maximum size for each chunk in tokens (default: 1500)
        
    Returns:
        List of dictionaries, each containing:
            - 'text': The segment text
            - 'tokens': Number of tokens in the segment
        
    Raises:
        SegmentationError: If segmentation fails or API key is not set
    """
    if not text:
        return []
        
    if not isinstance(text, str):
        raise SegmentationError("Input must be a string")
        
    if not isinstance(max_chunk_size, int) or max_chunk_size <= 0:
        raise SegmentationError("max_chunk_size must be a positive integer")
    
    result = _call_jina_api(text, max_chunk_size)
    return _optimize_chunks(result, max_chunk_size)

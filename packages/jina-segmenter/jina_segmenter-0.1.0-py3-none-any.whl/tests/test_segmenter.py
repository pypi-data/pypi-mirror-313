"""
Tests for the jina_segmenter package
"""

import os
import pytest
from jina_segmenter import segment_text
from jina_segmenter.segmenter import SegmentationError

def test_missing_api_key():
    """Test behavior when API key is not set"""
    if 'JINA_API_KEY' in os.environ:
        del os.environ['JINA_API_KEY']
    
    with pytest.raises(SegmentationError):
        segment_text("Test text")

def test_invalid_input():
    """Test behavior with invalid input"""
    os.environ['JINA_API_KEY'] = 'dummy_key'
    
    with pytest.raises(SegmentationError):
        segment_text(None)
    
    with pytest.raises(SegmentationError):
        segment_text("")
    
    with pytest.raises(SegmentationError):
        segment_text("text", max_chunk_size=0)
    
    with pytest.raises(SegmentationError):
        segment_text("text", max_chunk_size=-1)
    
    with pytest.raises(SegmentationError):
        segment_text("text", max_chunk_size="1700")

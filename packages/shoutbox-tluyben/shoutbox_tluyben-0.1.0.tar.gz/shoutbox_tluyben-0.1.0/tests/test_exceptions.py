"""Tests for the Shoutbox exceptions"""

import pytest
from shoutbox.exceptions import ShoutboxError, ValidationError, APIError

def test_shoutbox_error():
    """Test base ShoutboxError"""
    error = ShoutboxError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)

def test_validation_error():
    """Test ValidationError"""
    error = ValidationError("Invalid email")
    assert str(error) == "Invalid email"
    assert isinstance(error, ShoutboxError)
    
    # Test with detailed validation errors
    error = ValidationError({
        'email': 'Invalid format',
        'subject': 'Required field'
    })
    assert 'Invalid format' in str(error)
    assert 'Required field' in str(error)

def test_api_error():
    """Test APIError"""
    # Test with status code only
    error = APIError("API request failed", 400)
    assert str(error) == "API request failed"
    assert error.status_code == 400
    assert error.response_body is None
    
    # Test with response body
    response_body = {
        'error': 'Bad Request',
        'message': 'Invalid parameters'
    }
    error = APIError("API request failed", 400, response_body)
    assert error.status_code == 400
    assert error.response_body == response_body
    
    # Test inheritance
    assert isinstance(error, ShoutboxError)

def test_error_handling_chain():
    """Test error handling chain and inheritance"""
    try:
        raise ValidationError("Test validation error")
    except ShoutboxError as e:
        assert isinstance(e, ValidationError)
        assert str(e) == "Test validation error"
    
    try:
        raise APIError("Test API error", 500)
    except ShoutboxError as e:
        assert isinstance(e, APIError)
        assert e.status_code == 500

def test_error_with_cause():
    """Test errors with underlying cause"""
    original_error = ValueError("Original error")
    
    try:
        try:
            raise original_error
        except ValueError as e:
            raise ShoutboxError("Wrapped error") from e
    except ShoutboxError as e:
        assert isinstance(e.__cause__, ValueError)
        assert str(e.__cause__) == "Original error"

def test_api_error_response_handling():
    """Test APIError with different response formats"""
    # Test with string response
    error = APIError("API error", 400, "Invalid request")
    assert error.response_body == "Invalid request"
    
    # Test with dict response
    response = {
        'error': 'ValidationError',
        'details': {
            'field': 'email',
            'message': 'Invalid format'
        }
    }
    error = APIError("API error", 400, response)
    assert error.response_body == response
    
    # Test with None response
    error = APIError("API error", 500)
    assert error.response_body is None

def test_validation_error_details():
    """Test ValidationError with detailed error information"""
    # Single field error
    error = ValidationError({
        'email': 'Invalid email format'
    })
    assert 'email' in str(error)
    assert 'Invalid email format' in str(error)
    
    # Multiple field errors
    error = ValidationError({
        'email': 'Invalid email format',
        'subject': 'Subject is required',
        'to': ['First recipient invalid', 'Second recipient invalid']
    })
    error_str = str(error)
    assert 'email' in error_str
    assert 'subject' in error_str
    assert 'to' in error_str
    assert 'First recipient invalid' in error_str
    
    # Nested errors
    error = ValidationError({
        'attachments': {
            0: {'filename': 'Required field'},
            1: {'content': 'Invalid content'}
        }
    })
    error_str = str(error)
    assert 'attachments' in error_str
    assert 'filename' in error_str
    assert 'content' in error_str

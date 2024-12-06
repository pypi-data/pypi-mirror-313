import pytest
from src import Context
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import weakref

def test_context_delete():
    context = Context()
    context["key1"] = "value1"
    del context["key1"]
    assert context.get("key1", None) is None

def test_context_clear():
    context = Context()
    context["key1"] = "value1"
    context["key2"] = "value2"
    context.clear()
    assert context.get("key1", None) is None
    assert context.get("key2", None) is None

def test_context_contains():
    context = Context()
    context["key1"] = "value1"
    assert "key1" in context
    assert "nonexistent" not in context

def test_context_multiple_types():
    context = Context()
    test_values = {
        "string": "value",
        "integer": 42,
        "float": 3.14,
        "list": [1, 2, 3],
        "dict": {"a": 1},
        "none": None
    }
    
    for key, value in test_values.items():
        context[key] = value
        assert context.get(key) == value 

def test_context_concurrent_access():
    context = Context()
    num_threads = 10
    iterations = 100
    
    def worker(thread_id):
        for i in range(iterations):
            key = f"key_{thread_id}_{i}"
            context[key] = i
            assert context.get(key) == i
            del context[key]
            assert key not in context
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker, i) for i in range(num_threads)]
        for future in futures:
            future.result()

def test_context_concurrent_same_key():
    context = Context()
    num_threads = 5
    iterations = 2
    key = "shared_key"
    
    def writer():
        for i in range(iterations):
            context[key] = i
            time.sleep(0.001)  # Force thread interleaving
    
    def reader():
        for _ in range(iterations):
            value = context.get(key)
            assert isinstance(value, (type(None), int))
            time.sleep(0.001)  # Force thread interleaving

    threads = ([threading.Thread(target=writer) for _ in range(num_threads)] + 
               [threading.Thread(target=reader) for _ in range(num_threads)])
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def test_context_large_data():
    context = Context()
    large_list = list(range(10000))
    large_dict = {str(i): i for i in range(10000)}
    
    context["large_list"] = large_list
    context["large_dict"] = large_dict
    
    assert context.get("large_list") == large_list
    assert context.get("large_dict") == large_dict

def test_context_nested_structures():
    context = Context()
    nested_data = {
        "level1": {
            "level2": {
                "level3": [1, 2, {"key": "value"}]
            }
        }
    }
    
    context["nested"] = nested_data
    retrieved = context.get("nested")
    assert retrieved == nested_data
    assert retrieved is not nested_data  # Verify deep copy

def test_context_key_types():
    context = Context()
    
    with pytest.raises(TypeError):
        context[123] = "value"  # Non-string key
    
    with pytest.raises(TypeError):
        context.get(123)  # Non-string key
    
    with pytest.raises(TypeError):
        del context[123]  # Non-string key

def test_context_empty_key():
    context = Context()
    
    context[""] = ""
    assert context.get("") == ""
    del context[""]
    assert "" not in context
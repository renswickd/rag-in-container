# Development Guide

## Project Setup

1. Clone repository
2. Install dependencies
3. Configure environment
4. Create directories

## Adding Components

### Frontend
```python
# Example component
def render_new_component():
    st.markdown("New Component")
```

### Pipeline
```python
# Example processor
class NewProcessor:
    def process(self, data):
        return processed_data
```

### Graph
```python
# Example node
def new_node(state):
    return {"result": process(state)}
```

## Testing

### Running Tests
```bash
pytest tests/
```

### Adding Tests
```python
def test_new_feature():
    assert feature_works()
```
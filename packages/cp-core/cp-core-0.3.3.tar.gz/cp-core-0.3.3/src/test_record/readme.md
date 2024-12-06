# Test Record

记录测试结果。

可以使用`allure`来替代。实际上，我没想清楚这部分怎么处理。

## Usage

```python
from test_record import TestRecord

# Create a temporary directory
temp_dir = tempfile.mkdtemp(dir="./tmp")

tr = TestRecord()
```

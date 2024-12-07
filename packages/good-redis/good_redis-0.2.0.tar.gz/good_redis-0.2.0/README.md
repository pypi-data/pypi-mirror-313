# good-redis

Fast-depends compatible Redis client - sync and async versions

Also adds "prioritized queue" redis commands

### Prioritized Stream Implementation in Redis Client Library

The `Prioritized Stream` is a custom data structure implemented using Redis, backed by Lua scripts to handle operations with priority-based ordering. The key features and behaviors of this prioritized stream are outlined below:

#### Key Components

1. **Redis Keys**:
   - `:ps:keys`: Set containing all active prioritized stream names.
   - `<name>:t`: Hash table where each key corresponds to a specific item, and its value represents the stored data.
   - `<name>:s`: Sorted set where the score represents the priority of each key.
   - `<name>:exc`: Set of keys that are excluded from re-adding, typically after being processed and removed.
   - `<name>:exp`: Sorted set for tracking the expiration of keys.

2. **Lua Scripts**:
   - **`psadd`**: Adds a key-value pair to the stream with a specified priority score. The item is added only if it’s not in the exclusion or expiration sets.
   - **`pspull`**: Retrieves a specified number of items from the stream in order of highest priority. The items can be purged (removed) or retained with their priority decreased, and they can also be gated (prevented from being re-added).
   - **`psdecrementall`**: Decreases the priority of all items in the stream by a specified amount.

#### Stream Operations

1. **Add Items (`psadd` and `psaddmany`)**:
   - **`psadd(name, key, value, score, readd=False)`**: Adds a single item to the stream.
     - If `readd=True`, the item is removed from the exclusion and expiration sets before being added.
   - **`psaddmany(name, items, readd=False)`**: Adds multiple items to the stream in a single pipeline operation.

2. **Retrieve and Process Items (`pspull`)**:
   - **`pspull(name, count=1, purge=True, gate=False, expire_at=timedelta(minutes=1440))`**: Retrieves up to `count` items from the stream, ordered by priority.
     - **`purge`**: If `True`, removes the items from the stream after retrieval. If `False`, decreases their priority and retains them in the stream.
     - **`gate`**: If `True`, adds retrieved items to the exclusion set, preventing them from being re-added.
     - **`expire_at`**: Sets the expiration timestamp for the retrieved items.

3. **Manage Stream Items**:
   - **`pskeys(name)`**: Retrieves all keys from the stream's sorted set.
   - **`psvalues(name)`**: Retrieves all values from the stream's hash table.
   - **`psdelete(name)`**: Deletes the entire stream, removing associated keys, sorted sets, and exclusion sets.
   - **`psincrement(name, key, score)`**: Increments the priority score of a specific key.
   - **`psdeletebelowthreshold(name, threshold, gate=False)`**: Removes all items with a priority score below a specified threshold.
     - **`gate`**: If `True`, adds the removed items to the exclusion set.
   - **`pslen(name)`**: Returns the total number of items in the stream.
   - **`psget(name, key)`**: Retrieves the value associated with a specific key.
   - **`psdecrement_all(name, decrement)`**: Decrements the priority score of all items in the stream by a specified value.

4. **Expiration Management**:
   - **`psexpire()`**: Removes expired items from all active prioritized streams based on the current timestamp.

#### Usage Scenarios

- **Task Queues**: The prioritized stream can be used to implement task queues where tasks with higher priorities are processed first.
- **Rate Limiting**: Items can be gated and expired to prevent frequent re-processing.
- **Deferred Processing**: Items with lower priority can be retained and re-processed later when their priority increases.

This prioritized stream implementation allows for efficient management of time-sensitive and prioritized workloads in a Redis-backed environment, leveraging the power of Lua scripts for atomic and complex operations.

### 1. **Adding Items to the Stream**

```python
from fast_depends import inject

@inject
def add_items_to_stream(
    redis: Redis = RedisProvider(),
):
    # Add a single item to the stream
    redis.psadd(name="task_queue", key="task_1", value="Process data", score=10)

    # Add multiple items to the stream
    items = [
        ("task_2", "Send email", 8),
        ("task_3", "Generate report", 12),
    ]
    redis.psaddmany(name="task_queue", items=items)

    # Re-add an item that was previously excluded
    redis.psadd(name="task_queue", key="task_1", value="Process data", score=15, readd=True)

add_items_to_stream()
```

```python
from fast_depends import inject

@inject
async def add_items_to_stream_async(
    rc: AsyncRedis = AsyncRedisProvider(),
):
    async with rc as redis:
        # Add a single item to the stream
        await redis.psadd(name="task_queue", key="task_1", value="Process data", score=10)

        # Add multiple items to the stream
        items = [
            ("task_2", "Send email", 8),
            ("task_3", "Generate report", 12),
        ]
        await redis.psaddmany(name="task_queue", items=items)

        # Re-add an item that was previously excluded
        await redis.psadd(name="task_queue", key="task_1", value="Process data", score=15, readd=True)

await add_items_to_stream_async()
```

### 2. **Retrieving and Processing Items from the Stream**

```python
from fast_depends import inject

@inject
def process_items_from_stream(
    redis: Redis = RedisProvider(),
):
    # Pull one item with the highest priority, remove it from the stream after processing
    item = redis.pspull(name="task_queue", count=1, purge=True)
    print(item)

    # Pull two items without removing them, but decrement their priority
    items = redis.pspull(name="task_queue", count=2, purge=False)
    print(items)

process_items_from_stream()
```

```python
from fast_depends import inject

@inject
async def process_items_from_stream_async(
    rc: AsyncRedis = AsyncRedisProvider(),
):
    async with rc as redis:
        # Pull one item with the highest priority, remove it from the stream after processing
        item = await redis.pspull(name="task_queue", count=1, purge=True)
        print(item)

        # Pull two items without removing them, but decrement their priority
        items = await redis.pspull(name="task_queue", count=2, purge=False)
        print(items)

await process_items_from_stream_async()
```

### 3. **Incrementing the Priority of a Specific Item**

```python
from fast_depends import inject

@inject
def increment_priority(
    redis: Redis = RedisProvider(),
):
    # Increment the priority score of a specific task
    redis.psincrement(name="task_queue", key="task_2", score=5)

increment_priority()
```

```python
from fast_depends import inject

@inject
async def increment_priority_async(
    rc: AsyncRedis = AsyncRedisProvider(),
):
    async with rc as redis:
        # Increment the priority score of a specific task
        await redis.psincrement(name="task_queue", key="task_2", score=5)

await increment_priority_async()
```

### 4. **Deleting Items Below a Certain Priority Threshold**

```python
from fast_depends import inject

@inject
def delete_below_threshold(
    redis: Redis = RedisProvider(),
):
    # Delete all tasks with a priority score below 10
    redis.psdeletebelowthreshold(name="task_queue", threshold=10)

delete_below_threshold()
```

```python
from fast_depends import inject

@inject
async def delete_below_threshold_async(
    rc: AsyncRedis = AsyncRedisProvider(),
):
    async with rc as redis:
        # Delete all tasks with a priority score below 10
        await redis.psdeletebelowthreshold(name="task_queue", threshold=10)

await delete_below_threshold_async()
```

### 5. **Viewing All Keys and Values in the Stream**

```python
from fast_depends import inject

@inject
def view_keys_and_values(
    redis: Redis = RedisProvider(),
):
    # Retrieve all keys in the sorted set (in order of priority)
    keys = redis.pskeys(name="task_queue")
    print(keys)

    # Retrieve all values in the hash table
    values = redis.psvalues(name="task_queue")
    print(values)

view_keys_and_values()
```

```python
from fast_depends import inject

@inject
async def view_keys_and_values_async(
    rc: AsyncRedis = AsyncRedisProvider(),
):
    async with rc as redis:
        # Retrieve all keys in the sorted set (in order of priority)
        keys = await redis.pskeys(name="task_queue")
        print(keys)

        # Retrieve all values in the hash table
        values = await redis.psvalues(name="task_queue")
        print(values)

await view_keys_and_values_async()
```

### 6. **Decrementing the Priority of All Items in the Stream**

```python
from fast_depends import inject

@inject
def decrement_all_priorities(
    redis: Redis = RedisProvider(),
):
    # Decrease the priority of all items by 2
    redis.psdecrement_all(name="task_queue", decrement=2)

decrement_all_priorities()
```

```python
from fast_depends import inject

@inject
async def decrement_all_priorities_async(
    rc: AsyncRedis = AsyncRedisProvider(),
):
    async with rc as redis:
        # Decrease the priority of all items by 2
        await redis.psdecrement_all(name="task_queue", decrement=2)

await decrement_all_priorities_async()
```

### 7. **Handling Expired Items**

```python
from fast_depends import inject

@inject
def handle_expired_items(
    redis: Redis = RedisProvider(),
):
    # Remove all expired items from all prioritized streams
    redis.psexpire()

handle_expired_items()
```

```python
from fast_depends import inject

@inject
async def handle_expired_items_async(
    rc: AsyncRedis = AsyncRedisProvider(),
):
    async with rc as redis:
        # Remove all expired items from all prioritized streams
        await redis.psexpire()

await handle_expired_items_async()
```

These examples demonstrate how to utilize the prioritized stream functionality in a dependency injection style with `fast-depends`. This approach makes it easy to manage Redis clients and stream operations in both synchronous and asynchronous contexts.
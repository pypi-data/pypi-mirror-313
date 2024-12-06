import pytest
from src.core.task import task, Task, TaskStatus, TaskProgress
from src.core.io import InputSchema, OutputSchema
from src.core.context import Context
import asyncio

@pytest.mark.asyncio
async def test_task_basic_execution():
    @task(
        name="test_task",
        description="A test task",
        requires=InputSchema({"input": str}),
        provides=OutputSchema({"output": str})
    )
    async def sample_task(context: Context):
        context["output"] = f"Processed: {context['input']}"

    context = Context()
    context["input"] = "test"
    
    task_instance = Task(
        name="test_task",
        func=sample_task,
        description="Test task",
        parameters={},
        requires=sample_task._requires,
        provides=sample_task._provides
    )
    
    assert task_instance.status == TaskStatus.PENDING
    await task_instance.execute(context)
    assert task_instance.status == TaskStatus.COMPLETED
    assert context["output"] == "Processed: test"

@pytest.mark.asyncio
async def test_task_with_parameters():
    @task(
        name="parameterized_task",
        parameters={"multiplier": 2},
        requires=InputSchema({"number": int}),
        provides=OutputSchema({"result": int})
    )
    async def math_task(context: Context, multiplier: int):
        context["result"] = context["number"] * multiplier

    context = Context()
    context["number"] = 5
    
    task_instance = Task(
        name="math_task",
        func=math_task,
        description="Math operation",
        parameters={"multiplier": 2},
        requires=math_task._requires,
        provides=math_task._provides
    )
    
    await task_instance.execute(context)
    assert context["result"] == 10

@pytest.mark.asyncio
async def test_task_missing_required_parameter():
    @task(
        name="task_with_required_param",
        requires=InputSchema({}),
        provides=OutputSchema({"output": str})
    )
    async def param_task(context: Context, required_param: str):
        context["output"] = required_param

    context = Context()
    task_instance = Task(
        name="param_task",
        func=param_task,
        description="Task with required parameter",
        parameters={},  # Missing required_param
        requires=param_task._requires,
        provides=param_task._provides
    )
    
    with pytest.raises(ValueError, match="Required parameter 'required_param' not provided"):
        await task_instance.execute(context)

@pytest.mark.asyncio
async def test_task_failure_handling():
    @task(
        name="failing_task",
        requires=InputSchema({}),
        provides=OutputSchema({"output": str})
    )
    async def failing_task(context: Context):
        raise ValueError("Task failed intentionally")

    context = Context()
    task_instance = Task(
        name="failing_task",
        func=failing_task,
        description="Failing task",
        parameters={},
        requires=failing_task._requires,
        provides=failing_task._provides
    )
    
    with pytest.raises(ValueError, match="Task failed intentionally"):
        await task_instance.execute(context)
    assert task_instance.status == TaskStatus.FAILED

def test_task_decorator_validation():
    # Test non-async function
    with pytest.raises(ValueError, match="must be async"):
        @task(name="sync_task")
        def sync_task(context: Context):
            pass

    # Test missing context parameter
    with pytest.raises(ValueError, match="must have 'context' parameter"):
        @task(name="invalid_task")
        async def invalid_task(wrong_param: str):
            pass

    # Test invalid return value
    with pytest.raises(ValueError, match="should not return any value"):
        @task(name="returning_task")
        async def returning_task(context: Context) -> str:
            return "value"

def test_task_progress():
    progress = TaskProgress(name="test_task", status=TaskStatus.RUNNING)
    assert progress.name == "test_task"
    assert progress.status == TaskStatus.RUNNING

@pytest.mark.asyncio
async def test_task_concurrent_execution():
    @task(
        name="concurrent_task",
        requires=InputSchema({"input": int}),
        provides=OutputSchema({"output": int})
    )
    async def concurrent_task(context: Context):
        await asyncio.sleep(0.1)  # Simulate work
        context["output"] = context["input"] * 2

    # Create multiple contexts and tasks
    contexts = [Context() for _ in range(3)]
    tasks = []
    
    for i, ctx in enumerate(contexts):
        ctx["input"] = i
        task_instance = Task(
            name=f"concurrent_task_{i}",
            func=concurrent_task,
            description="Concurrent task",
            parameters={},
            requires=concurrent_task._requires,
            provides=concurrent_task._provides
        )
        tasks.append(task_instance.execute(ctx))
    
    # Execute tasks concurrently
    await asyncio.gather(*tasks)
    
    # Verify results
    for i, ctx in enumerate(contexts):
        assert ctx["output"] == i * 2

@pytest.mark.asyncio
async def test_task_schema_validation():
    @task(
        name="schema_task",
        requires=InputSchema({"number": int, "text": str}),
        provides=OutputSchema({"result": str})
    )
    async def schema_task(context: Context):
        num = context["number"]
        text = context["text"]
        context["result"] = f"{text}: {num}"

    context = Context()
    context["number"] = "not_an_integer"  # Wrong type
    context["text"] = "test"
    
    task_instance = Task(
        name="schema_task",
        func=schema_task,
        description="Schema validation task",
        parameters={},
        requires=schema_task._requires,
        provides=schema_task._provides
    )
    
    with pytest.raises(TypeError):
        await task_instance.execute(context)
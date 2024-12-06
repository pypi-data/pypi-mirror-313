import pytest
from src import (
    Workflow, 
    Context, 
    TaskStatus,
    WorkflowException
)
from src.core.io import InputSchema, OutputSchema, Input, Output
from src.serialization.workflow_serializer import WorkflowSerializer
import tempfile
import os
import json

# Create workflow instance for test tasks
workflow = Workflow("test_workflow", InputSchema({}), OutputSchema({}))

@workflow.task(
    provides=OutputSchema({"simple_output": str})
)
async def simple_task(context: 'Context'):
    context["simple_output"] = "simple task complete"

@workflow.task(
    requires=InputSchema({"input": int}),
    provides=OutputSchema({"param_output": int}),
    parameters={"multiplier": int}
)
async def task_with_params(context: 'Context', multiplier: int):
    value = context.get("input", 0)
    context["param_output"] = value * multiplier

@workflow.task(
    requires=InputSchema({"input": str}),
    provides=OutputSchema({"processed_data": str})
)
async def task_with_deps(context: 'Context'):
    input = context.get("input")
    context["processed_data"] = f"processed_{input}"

@workflow.task(
    description="Task that raises an error"
)
async def task_with_error(context: 'Context'):
    raise ValueError("Task error")

@workflow.task(
    provides=OutputSchema({"input": str})
)
async def provider_task(context: 'Context'):
    context["input"] = "raw_data"

@workflow.task(
    provides=OutputSchema({"first": str})
)
async def first_task(context: 'Context'):
    first_task.execution_order.append("first")
    context["first"] = "done"

@workflow.task(
    requires=InputSchema({"first": str}),
    provides=OutputSchema({"second": str})
)
async def second_task(context: 'Context'):
    second_task.execution_order.append("second")
    context["second"] = "done"

first_task.execution_order = []
second_task.execution_order = []

@pytest.fixture
def temp_filepath():
    """Fixture to provide a temporary file path."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        filepath = tmp.name
    yield filepath
    # Cleanup after test
    if os.path.exists(filepath):
        os.unlink(filepath)

async def test_simple_workflow_serialization(temp_filepath):
    """Test serialization of a simple workflow with one task."""
    input_schema = InputSchema({})
    output_schema = OutputSchema({"simple_output": str})
    workflow = Workflow("simple_workflow", input_schema, output_schema)
    workflow.task(name="simple_task", provides=OutputSchema({"simple_output": str}))(simple_task)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)
    loaded_workflow = WorkflowSerializer.load_workflow(temp_filepath)

    assert loaded_workflow.name == workflow.name
    assert len(loaded_workflow.tasks) == 1
    assert "simple_task" in loaded_workflow.tasks

    # Create input data and execute workflow
    input = Input({})
    output = await loaded_workflow.execute(input=input)

    assert output["simple_output"] == "simple task complete"

async def test_workflow_with_parameters(temp_filepath):
    input_schema = InputSchema({"input": int})
    output_schema = OutputSchema({"param_output": int})
    workflow = Workflow("param_workflow", input_schema, output_schema)
    workflow.task(
        name="task_with_params",
        requires=InputSchema({"input": int}),
        provides=OutputSchema({"param_output": int}),
        parameters={"multiplier": 2}
    )(task_with_params)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)
    loaded_workflow = WorkflowSerializer.load_workflow(temp_filepath)

    input = Input({"input": 5})
    output = await loaded_workflow.execute(input=input)

    assert output["param_output"] == 10

async def test_workflow_with_dependencies(temp_filepath):
    input_schema = InputSchema({})
    output_schema = OutputSchema({"processed_data": str})
    workflow = Workflow("dep_workflow", input_schema, output_schema)

    workflow.task(name="provider_task", provides=OutputSchema({"input": str}))(provider_task)
    workflow.task(
        name="task_with_deps",
        requires=InputSchema({"input": str}),
        provides=OutputSchema({"processed_data": str})
    )(task_with_deps)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)
    loaded_workflow = WorkflowSerializer.load_workflow(temp_filepath)

    input = Input({})
    output = await loaded_workflow.execute(input=input)

    assert output["processed_data"] == "processed_raw_data"

def test_invalid_file_loading():
    with pytest.raises(FileNotFoundError):
        WorkflowSerializer.load_workflow("nonexistent_file.json")

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"invalid json content")
        filepath = tmp.name

    try:
        with pytest.raises(json.JSONDecodeError):
            WorkflowSerializer.load_workflow(filepath)
    finally:
        os.unlink(filepath)

async def test_error_handling_in_loaded_workflow(temp_filepath):
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("error_workflow", input_schema, output_schema)
    workflow.task()(task_with_error)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)
    loaded_workflow = WorkflowSerializer.load_workflow(temp_filepath)

    with pytest.raises(ValueError, match="Task error"):
        input = Input({})
        await loaded_workflow.execute(input=input)

def test_serialized_file_format(temp_filepath):
    input_schema = InputSchema({})
    output_schema = OutputSchema({"param_output": int})
    workflow = Workflow("test_workflow", input_schema, output_schema)
    workflow.task(
        requires=InputSchema({"input": int}),
        provides=OutputSchema({"param_output": int}),
        parameters={"multiplier": 2}
    )(task_with_params)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)

    with open(temp_filepath, 'r') as f:
        data = json.load(f)

    assert "name" in data
    assert "tasks" in data
    assert "task_with_params" in data["tasks"]
    
    task_data = data["tasks"]["task_with_params"]
    required_fields = {"name", "parameters", "requires", "provides", 
                      "status", "callable_module", "callable_name"}
    for field in required_fields:
        assert field in task_data

async def test_multiple_tasks_order(temp_filepath):
    first_task.execution_order = []
    second_task.execution_order = []
    
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("order_workflow", input_schema, output_schema)

    workflow.task(provides=OutputSchema({"first": str}))(first_task)
    workflow.task(
        requires=InputSchema({"first": str}),
        provides=OutputSchema({"second": str})
    )(second_task)

    WorkflowSerializer.save_workflow(workflow, temp_filepath)
    loaded_workflow = WorkflowSerializer.load_workflow(temp_filepath)

    input = Input({})
    await loaded_workflow.execute(input=input)

    assert first_task.execution_order == ["first"]
    assert second_task.execution_order == ["second"]
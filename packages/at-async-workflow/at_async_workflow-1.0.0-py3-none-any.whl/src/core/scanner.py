from typing import List, Dict, Any
import os
import inspect
import json
from pathlib import Path
from .io import InputSchema, OutputSchema
from .task import Task
from ..utils.logging import setup_logger
import importlib.util

logger = setup_logger(__name__)

class WorkflowScanner:
    """Scanner for workflow tasks in a directory."""
    
    @staticmethod
    def scan_directory(directory: str) -> List[Dict[str, Any]]:
        """
        Scan a directory for all functions decorated with @workflow.task and serialize them.
        
        Args:
            directory: The directory path to scan
            
        Returns:
            List of serialized task definitions
        """
        tasks = []
        directory_path = Path(directory)
        
        # Walk through all Python files in the directory
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    
                    try:
                        # Get the module name relative to the scan directory
                        rel_path = file_path.relative_to(directory_path.parent)
                        module_path = str(rel_path).replace(os.sep, '.')[:-3]  # Remove .py
                        
                        # Import the module dynamically
                        spec = importlib.util.spec_from_file_location(module_path, str(file_path))
                        if spec is None or spec.loader is None:
                            continue
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # Inspect all module members
                        for name, obj in inspect.getmembers(module):
                            if inspect.isfunction(obj) and hasattr(obj, '_is_workflow_task'):
                                task_info = WorkflowScanner._serialize_task(obj)
                                tasks.append(task_info)
                                logger.debug(f"Found task: {name} in {file_path}")
                                
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {str(e)}")
                        
        return tasks

    @staticmethod
    def _serialize_task(func) -> Dict[str, Any]:
        """
        Serialize a single task function into the required format.
        
        Args:
            func: The task function to serialize
            
        Returns:
            Dictionary containing the serialized task information
        """
        # Get function signature
        sig = inspect.signature(func)
        
        # Get task decorator metadata
        description: str = getattr(func, '_description', None) or func.__doc__ or ""
        requires: InputSchema = getattr(func, '_requires', {})
        provides: OutputSchema = getattr(func, '_provides', {})
        parameters: Dict[str, Any] = getattr(func, '_parameters', {})
        task_name: str = getattr(func, '_name', func.__name__)
        
        # Build parameters list
        param_list = []
        for name, param in sig.parameters.items():
            if name == 'context':  # Skip context parameter
                continue
                
            param_info = {
                "name": name,
                "type": WorkflowScanner._get_type_str(param.annotation),
            }
            
            # Add default value if specified in parameters
            if name in parameters:
                param_info["value"] = parameters[name]
                
            param_list.append(param_info)
        
        # Build requires list
        requires_list = [
            {"name": key, "type": WorkflowScanner._get_type_str(type_)}
            for key, type_ in requires.items()
        ]
        
        # Build provides list
        provides_list = [
            {"name": key, "type": WorkflowScanner._get_type_str(type_)}
            for key, type_ in provides.items()
        ]
        
        return {
            "name": task_name,
            "description": description,
            "parameters": param_list,
            "requires": requires_list,
            "provides": provides_list
        }

    @staticmethod
    def _get_type_str(type_annotation) -> str:
        """
        Convert a type annotation to its string representation.
        
        Args:
            type_annotation: The type annotation to convert
            
        Returns:
            String representation of the type
        """
        if type_annotation == inspect.Parameter.empty:
            return "Any"
        return type_annotation.__name__
# from langroid.agent.tool_message import ToolMessage
# from langroid.agent.task import Task
# from typing import Any
#
# class TypedTask:
#     def __init__(self, Task: Task, input_type: Any, output_type: Any):
#         self.Task = Task
#         self.input_type = input_type
#         self.output_type = output_type
#
#     def run(self, input: Any) -> Any:
#         if not isinstance(input, self.input_type):
#             raise ValueError(f"Input must be of type {self.input_type}")
#         output = self.Task.run(input)
#         if not isinstance(output, self.output_type):
#             raise ValueError(f"Output must be of type {self.output_type}")
#         return output
#
#

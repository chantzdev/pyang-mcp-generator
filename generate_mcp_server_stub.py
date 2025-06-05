import importlib
import inspect
import argparse
from pathlib import Path

def generate_get_config_tool(module_name: str, output_path: str):
    mod = importlib.import_module(module_name)

    # Find top-level class (from pyangbind)
    top_classes = [name for name, obj in inspect.getmembers(mod)
                   if inspect.isclass(obj) and hasattr(obj, "_pyangbind_elements")]

    if not top_classes:
        raise ValueError(f"No PyangBind-compatible class found in module '{module_name}'")

    class_name = top_classes[0]
    func_name = f"get_{class_name.lower()}"

    print(f"[INFO] Generating tool '{func_name}' from class: {class_name} in module: {module_name}")

    code = f'''from mcp.server.fastmcp import FastMCP
from {module_name} import {class_name}
from pyangbind.lib.serialise import pybindJSONEncoder
import json

mcp = FastMCP("{class_name} MCP")

current_config = {class_name}()

@mcp.tool()
def {func_name}() -> str:
    return json.dumps(current_config, cls=pybindJSONEncoder, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio")
'''

    Path(output_path).write_text(code)
    print(f"[SUCCESS] Generated MCP server at: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an MCP server from pyangbind module")
    parser.add_argument("--module", required=True, help="The Python module (e.g., example_bindings)")
    parser.add_argument("--output", default="generated_mcp_server.py", help="Output MCP server file")

    args = parser.parse_args()
    generate_get_config_tool(args.module, args.output)

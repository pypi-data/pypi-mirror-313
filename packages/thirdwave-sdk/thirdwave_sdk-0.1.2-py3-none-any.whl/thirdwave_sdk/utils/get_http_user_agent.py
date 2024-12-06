import platform
import tomli
import os

SDK_NAME="thirdwave-python-sdk"

def get_http_user_agent() -> str:
    pyproject_path = os.path.abspath("../../../pyproject.toml")

    with open(pyproject_path, "rb") as f:
        pyproject_data = tomli.load(f)
        
        python_version = platform.python_version()
        os_info = f"{platform.system}; {platform.machine()}"
        sdk_version = pyproject_data.get("tool", {}).get("poetry", {}).get("version")
        
        if not sdk_version:
            raise ValueError("Version not found in pyproject.toml")
        
        return f"{SDK_NAME}/{sdk_version} Python/{python_version} ({os_info})"

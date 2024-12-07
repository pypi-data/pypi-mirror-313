import re
import sys
import subprocess

# Colin Li @ 202305
# Constant Setup for Optuna
PH = "<**>"
ERROR_CODE_FILE_OPTUNA = (
    "/home/cdsw/.local/lib/python<**>/site-packages/sqlalchemy/util/typing.py"
)

ERROR_CODE_TEXT_OPTUNA = """
\s*from typing_extensions import \(
\s*dataclass_transform as dataclass_transform,.*
\s*\)
"""
FIXED_CODE_TEXT_OPTUNA = """

    import sys
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "typing_extensions",
        "/home/cdsw/.local/lib/python<**>/site-packages/typing_extensions.py"
    )
    typing_extensions = importlib.util.module_from_spec(spec)
    sys.modules["typing_extensions"] = typing_extensions
    spec.loader.exec_module(typing_extensions)
    dataclass_transform = typing_extensions.dataclass_transform
    
"""
M_READ_SUCC_OPTUNA = "Source of error was found successfully!"
M_READ_FAIL_OPTUNA = "Source of error was not found."
M_FIND_SUCC_OPTUNA = "Error code was found successfully!"
M_FIND_FAIL_OPTUNA = "Error code was not found."
M_FIX_SUCC_OPTUNA = "Optuna import error was fixed successfully!"
M_FIX_FAIL_OPTUNA = "Optuna import error was not fixed."


def fix_cdsw_import_error(package_name, py_version: str):
    """Fix known issues that arise when importing specific packages in CDSW

    Author:
        Colin Li @ 2023-06

    Args:
        package_name (str): Name of the package (current only support optuna)

        py_version (str): Python version of environment with issue
    """
    # Check
    if sys.platform != "linux":
        raise OSError("Please only run this function in CDSW (Linux)")

    # Setup
    if package_name == "optuna":
        # Dependencies
        install_1 = subprocess.run(
            ["pip", "install", "--upgrade", "typing_extensions"],
            capture_output=True,
            text=True,
        )
        if install_1.returncode:
            raise IOError("Installation of typing_extensions is failed.")
        else:
            print("Installation of typing_extensions is successful!")

        # Optuna
        install_2 = subprocess.run(
            ["pip", "install", "optuna"], capture_output=True, text=True
        )
        if install_2.returncode:
            raise IOError("Installation of optuna is failed.")
        else:
            print("Installation of optuna is successful!")

        # Workaround
        fp = ERROR_CODE_FILE_OPTUNA.replace(PH, py_version)
        error = ERROR_CODE_TEXT_OPTUNA.replace(PH, py_version)
        replace = FIXED_CODE_TEXT_OPTUNA.replace(PH, py_version)

        try:
            with open(fp, "r") as file_in:
                script = file_in.read()
                print(M_READ_SUCC_OPTUNA)
        except:
            print(M_READ_FAIL_OPTUNA, "\n", M_FIX_FAIL_OPTUNA)
            return None

        # Workaround
        if re.search(error, script):
            print(M_FIND_SUCC_OPTUNA)
            try:
                script_new = re.sub(error, replace, script)
                print(script_new)
                with open(fp, "w") as file_out:
                    file_out.write(script_new)
                print(M_FIX_SUCC_OPTUNA)
                return True
            except:
                print(M_FIX_FAIL_OPTUNA)
                print()
                return None
        else:
            print(M_FIND_FAIL_OPTUNA, M_FIX_FAIL_OPTUNA)
            return None


if __name__ == "__main__":
    pass

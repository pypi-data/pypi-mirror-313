# Read the pyproject.toml file and extract the version
with open("pyproject.toml", "r") as f:
    lines = f.readlines()
    for line in lines:
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', "")
            break
    else:
        raise ValueError("Version not found in pyproject.toml")

# Write the version to __version__ in __init__.py
with open("ml3_platform_sdk/__init__.py", "w") as f:
    f.write(f'__version__ = "{version}"\n')
    print('Updated ml3_platform_sdk/__init__.py with version: ', version)

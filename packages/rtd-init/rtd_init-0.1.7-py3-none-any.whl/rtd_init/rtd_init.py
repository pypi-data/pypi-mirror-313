import os

def create_project_files():
    # Define file paths
    rtd_yaml_path = "readthedocs.yaml"
    requirements_path = os.path.join("source", "requirements.txt")

    # Content for readthedocs.yaml
    rtd_yaml_content = """
version: 2

# Set the OS, Python version and other tools you might need
build:
os: ubuntu-22.04
tools:
    python: "3.12"
    # You can also specify other tool versions:
    # nodejs: "20"
    # rust: "1.70"
    # golang: "1.20"

# Build documentation in the "docs/" directory with Sphinx
sphinx:
configuration: source/conf.py


# Optionally build your docs in additional formats such as PDF and ePub
# formats:
#   - pdf
#   - epub

# Optional but recommended, declare the Python requirements required
# to build your documentation
# See https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html
python:
install:
    - requirements: source/requirements.txt
"""

    requirements_contents  = """
sphinx==7.1.2
sphinx-copybutton
furo
sphinx-design
"""
    # Ensure the source directory exists
    os.makedirs(os.path.dirname(requirements_path), exist_ok=True)

    # Write the readthedocs.yaml file
    with open(rtd_yaml_path, "w") as rtd_file:
        rtd_file.write(rtd_yaml_content)

    # Write an empty requirements.txt file
    with open(requirements_path, "w") as req_file:
        req_file.write(requirements_contents)

    print(f"Files created:\n- {rtd_yaml_path}\n- {requirements_path}")

if __name__ == "__main__":
    create_project_files()

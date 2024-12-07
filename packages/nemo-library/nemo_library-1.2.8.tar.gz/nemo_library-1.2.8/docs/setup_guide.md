
# Guide to Using the nemo_library

The **nemo_library** is a powerful Python library designed to automate various tasks. To use it, you'll need an environment where you can write and execute Python code. This step-by-step guide explains how to set everything up, even if you're new to programming or Python.

---

## 1. Set Up Your Development Environment

We recommend using [Visual Studio Code (VS Code)](https://code.visualstudio.com/download). It is free, beginner-friendly, and available for Windows, macOS, and Linux.

### Install Visual Studio Code
1. Visit [https://code.visualstudio.com/download](https://code.visualstudio.com/download).
2. Download the version suitable for your operating system.
3. Follow the installation instructions provided by the installer.

### Install Python Extension
1. Open VS Code after installation.
2. Navigate to the **Extensions** view (icon with four squares in the left sidebar).
3. Search for `Python` and install the official extension by Microsoft.

---

## 2. Create a Virtual Environment with Conda

To ensure the **nemo_library** works correctly and to avoid conflicts with other Python installations on your system, we’ll create a virtual environment using **Conda**.

### Install Conda
1. Visit the official Conda installation page: [https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html).
2. Download and install Miniconda or Anaconda for your operating system.
3. Follow the installation instructions provided on the website.

### Create a Conda Environment
1. Open a terminal (Command Prompt, PowerShell, or your system’s terminal).
2. Run the following command to create a new environment with Python 3.13:
   ```bash
   conda create -n nemo_env python=3.13
   ```
   Replace `nemo_env` with any name you prefer for your environment.

3. Activate the environment by running:
   ```bash
   conda activate nemo_env
   ```

---

## 3. Set Up Your Project in Visual Studio Code

1. **Create a New Project Folder**:
   - Open VS Code and select **File** > **Open Folder…** to create or open a folder for your project.
   - This folder will serve as the workspace for your Python scripts.

2. **Open the Integrated Terminal**:
   - Go to **View** > **Terminal** in VS Code.
   - Activate your Conda environment in the terminal:
     ```bash
     conda activate nemo_env
     ```

---

## 4. Install the nemo_library

1. Ensure your Conda environment is activated.
2. Run the following command in the terminal to install the **nemo_library**:
   ```bash
   pip install nemo-library
   ```
3. Verify the installation by running:
   ```bash
   python -c "import nemo_library; print('nemo_library installed successfully!')"
   ```

---
## 5. Configure the nemo_library

please create a file "config.ini". This is an example for the content:
```
[nemo_library]
nemo_url = https://enter.nemo-ai.com
tenant = <your tenant>
userid = <your userid>
password = <your password>
environment = [prod|dev|demo]
hubspot_api_token = <your API token, if you are going to use the HubSpot adapter, blank if not used>
```

If you don't want to pass userid/password in a file (which is readable to everybody that has access to the file), you can use Windows Credential Manager or MacOS key chain to store your password. Please use "nemo_library" as "Program name". As an alternative, you can programmatically set your password by using this code

```python
from nemo_library.sub_password_handler import *

service_name = "nemo_library"
username = "my_username"
password = "my_password"

pm = PasswordManager(service_name, username)

# Set password
pm.set_password(password)
print(f"Password for user '{username}' in service '{service_name}' has been stored.")

# Retrieve password
retrieved_password = pm.get_password()
if retrieved_password:
    print(f"The stored password for user '{username}' is: {retrieved_password}")
else:
    print(f"No password found for user '{username}' in service '{service_name}'.")
```

## 6. Start Using the nemo_library

1. **Create a New Python Script**:
   - In your project folder, create a new file called `main.py`.

2. **Write Your First Code**:
   - Open the file and add the following code:
     ```python
     from nemo_library import NemoLibrary

     nl = NemoLibrary()
     print(nl.getProjectList())
     ```

3. **Run the Script**:
   - Save the file and execute it in the terminal by typing:
     ```bash
     python main.py
     ```

---

## Summary

With these steps, you have set up everything you need to start using the **nemo_library**. If you encounter any issues, double-check the steps or refer to the [official Python documentation](https://docs.python.org/3/) and [Conda documentation](https://docs.conda.io).

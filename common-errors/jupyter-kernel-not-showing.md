# Jupyter Kernel Not Showing in VS Code or Notebook

## ❗ Problem

After creating a virtual environment and installing Jupyter, the kernel does not appear in the Jupyter "Change Kernel" list, or selecting it runs the global Python instead of the project’s `.venv`.


## ✅ Solution

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```
2. **Install ipykernel**:
    ```bash
   pip3 install ipykernel
   ```
3. **Register the kernel with a unique name**:
    ```bash
    python -m ipykernel install --user \
  --name=venv_2_pandas_basics \
  --display-name "Python (2 - Pandas Basics)"
    ```
4. **Restart Jupyter Notebook or VS Code**:
    - Fully close and reopen the notebook or VS Code window.
    - Then select the new kernel from the list.
5. **Verify it's working**:
    ```python
    import sys
    print(sys.executable)
    ```
    It should point to the .venv/bin/python inside your project folder.


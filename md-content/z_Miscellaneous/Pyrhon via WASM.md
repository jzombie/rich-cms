# Python via WASM

Running Python in WebAssembly (WASM) is a growing field with several stable implementations available. Here are some notable options:

1. **Pyodide**:
   - **Description**: Pyodide is a project that brings the Python runtime to the browser via WebAssembly. It includes the Python interpreter and a host of scientific libraries such as NumPy, SciPy, and Pandas.
   - **Stability**: Pyodide is actively maintained and widely used in the community, making it one of the most stable options for running Python in WASM.
   - **Usage**: It is commonly used for running Python code directly in the browser and can be integrated into web applications.
   - **Website**: [Pyodide](https://pyodide.org/en/stable/)

2. **PyScript**:
   - **Description**: PyScript builds on top of Pyodide and allows you to run Python scripts in HTML files, providing a way to integrate Python and JavaScript seamlessly in web applications.
   - **Stability**: PyScript is also under active development and leverages the stability of Pyodide for executing Python code.
   - **Usage**: It is designed to be easy to use, enabling the inclusion of Python code in web pages in a manner similar to JavaScript.
   - **Website**: [PyScript](https://pyscript.net/)

3. **wasm3**:
   - **Description**: wasm3 is a high-performance WebAssembly interpreter that supports various languages, including Python, through its integration with other projects.
   - **Stability**: Known for its speed and efficiency, wasm3 is a reliable choice for running WebAssembly modules.
   - **Usage**: While not specifically focused on Python, it can be used as a backend for projects that execute Python in a WASM context.
   - **Website**: [wasm3](https://github.com/wasm3/wasm3)

4. **MicroPython and WASM**:
   - **Description**: MicroPython, a lean implementation of Python for microcontrollers, can also be compiled to WebAssembly. This allows running MicroPython in web browsers.
   - **Stability**: MicroPython is well-maintained, and its WebAssembly port is stable, though more lightweight compared to full Python implementations.
   - **Usage**: Suitable for lightweight applications where full Python features are not required.
   - **Website**: [MicroPython](https://micropython.org/)

These implementations provide various options depending on the specific requirements and constraints of your project. Pyodide and PyScript are particularly user-friendly for web integration, while wasm3 and MicroPython offer more specialized use cases.

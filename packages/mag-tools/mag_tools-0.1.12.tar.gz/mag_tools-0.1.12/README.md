# 基本库 Mag_Tools
## 安装依赖库
- Rust编译器
    访问 Rust 官网 并下载适用于 Windows 的安装程序，或者直接运行以下命令：
    ```Bash
        Invoke-WebRequest -Uri https://sh.rustup.rs -OutFile rustup-init.exe
    ```
    ```Bash
        .\rustup-init.exe
    ```
   添加 Rust 编译器的路径（通常是 C:\Users\你的用户名\.cargo\bin）
- 安装依赖项
  ```Bash
    pip install --upgrade pip
    pip install maturin
  ```
## 发布库 
- 创建虚拟环境
    ```Bash
    python -m venv venv
- 激活虚拟环境
    ```Bash
    venv\Scripts\activate
    ```
- 安装依赖项
    ```Bash
      pip install -r requirements.txt
    ```
- 编辑打包
    ```Bash
      python setup.py sdist bdist_wheel
    ```
- 本地安装库
    ```Bash
       pip install dist/mag_tools-0.1-py3-none-any.whl 
    ```
  - 上传包
    ```Bash
      twine upload dist/*
    ```
## 配置 API Token
- 获取API Token
- 配置.pypirc 文件： 在用户主目录下创建 .pypirc 文件，并添加以下内容(请用真实的token替代)
  ```Plaintext
  [distutils]
  index-servers =
      pypi

  [pypi]
  username = __token__
  password = pypi-AgENdGVzdC5weXBpLm9yZwIkZjM2YzQ2Y2QtY2Y2OS00YjY3LWE4YzUtY2Y2OTY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3YjY3Yj
  ```

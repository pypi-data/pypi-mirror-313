# Airosentris

Airosentris is a sentiment analysis platform that includes powerful components for training and running AI models. Designed for ease of use, it enables developers to integrate sentiment analysis capabilities into their applications quickly.

## Features

- **AiroRunner:** Execute trained sentiment analysis models efficiently.
- **AiroTrainer:** Train sentiment analysis models using customizable algorithms.
- **Easy Integration:** Seamlessly integrate with your existing applications.
- **Highly Customizable:** Tailor the AI models to fit specific requirements.

## Installation

You can install Airosentris via pip:

```bash
pip install airosentris
```


# Installing PyTorch with CUDA 12.1 on Windows

## Check CUDA Version

To determine the version of CUDA installed on your system, you can use the following command:

```shell
nvcc --version
```

This command checks the NVIDIA CUDA Compiler Driver version, which is part of the CUDA Toolkit. It will output the CUDA version currently installed.

## Install PyTorch with GPU Support

To install PyTorch with GPU support for CUDA 12.1, follow these steps:

### Step 1: Open Command Prompt

Open Command Prompt or your preferred terminal.

### Step 2: Install PyTorch

Run the following command to install PyTorch with CUDA 12.1 support:

```shell
pip install torch==2.3.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121
```

This command installs the specified version of PyTorch (2.3.1) with CUDA 12.1 support. The `--extra-index-url` flag points to the PyTorch wheel (whl) files for CUDA 12.1.

### Step 3: Verify the Installation

To verify that PyTorch is correctly installed and is using the GPU, run the following Python code:

```python
import torch
print(torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

This code will:
- Print the PyTorch version.
- Check if CUDA is available.
- Print the name of the GPU device if available.

### Example Output

You should see an output similar to this if everything is correctly set up:

```
2.3.1
True
NVIDIA GeForce GTX 1080
```

## Additional Notes

- Ensure that your CUDA drivers are properly installed and match the version you intend to use with PyTorch.
- If you do not have CUDA installed, you can download and install the CUDA Toolkit from the [NVIDIA CUDA website](https://developer.nvidia.com/cuda-toolkit-archive).
- Make sure you have the appropriate version of cuDNN installed, which is typically bundled with the CUDA Toolkit.

By following these steps, you should be able to install and verify PyTorch with GPU support for CUDA 12.1 on your Windows system.

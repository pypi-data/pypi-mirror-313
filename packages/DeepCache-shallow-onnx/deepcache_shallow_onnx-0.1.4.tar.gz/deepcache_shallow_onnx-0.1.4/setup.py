import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DeepCache-shallow-onnx",
    version="v0.1.4",
    author="Xinyin Ma",
    author_email="maxinyin@u.nus.edu",
    description="DeepCache-shallow-onnx: Accelerating Diffusion Models for Free",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/horseee/DeepCache-shallow-onnx",
    packages=setuptools.find_packages(exclude=["DeepCache-shallow-onnx.ddpm"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=['torch', 'diffusers==0.24.0', 'transformers', 'huggingface-hub==0.25.2', 'accelerate==0.23.0'],
    python_requires='>=3.6',
)
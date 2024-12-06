from setuptools import setup, find_packages

setup(
    name="infoapps_mlops_sdk",                           # Package name
    version="0.0.30",                            # Version
    author="Renaldo Williams",
    author_email="renaldo_williams@apple.com",
    description="A custom MLOps SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://prodgit.apple.com/feldspar/mlops-py",  # GitHub URL or any repo link
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
      "turihub==2.18.0",
      "pytorch-lightning==2.1.1",  # PyTorch Lightning with extras
      "torch==2.4.1",               # PyTorch
      # "tensorboard==2.13.*",                # TensorBoard support
      # "mlflow==2.6.0",
      # "wandb==0.18.5",
      # "keras==3.7.0",
      "keras==2.15.0",
      "tensorflow==2.15.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

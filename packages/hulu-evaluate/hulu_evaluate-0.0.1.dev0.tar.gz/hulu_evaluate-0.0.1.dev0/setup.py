from setuptools import find_packages, setup
import subprocess
import platform
import sys

def get_version() -> str:
    rel_path = "src/hulu_evaluate/__init__.py"
    with open(rel_path, "r") as fp:
        for line in fp.read().splitlines():
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

def check_cuda_available() -> bool:
    try:
        result = subprocess.run(
            ["nvcc", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

install_requires = [
    "accelerate==1.0.1",
    "aiohappyeyeballs==2.3.4",
    "aiohttp==3.10.1",
    "aiosignal==1.3.1",
    "annotated-types==0.7.0",
    "attrs==24.2.0",
    "black==24.10.0",
    "certifi==2024.7.4",
    "charset-normalizer==3.3.2",
    "click==8.1.7",
    "datasets==2.20.0",
    "dill==0.3.8",
    "dotwiz==0.4.0",
    "easydict==1.13",
    "evaluate==0.4.2",
    "executing==2.0.1",
    "exrex==0.11.0",
    "filelock==3.15.4",
    "frozendict==2.4.4",
    "frozenlist==1.4.1",
    "fsspec==2024.5.0",
    "funcy==2.0",
    "huggingface-hub==0.24.5",
    "idna==3.7",
    "Jinja2==3.1.4",
    "joblib==1.4.2",
    "json2latex==0.0.2",
    "lazy-load==0.8.3",
    "lazy-object-proxy==1.10.0",
    "littleutils==0.2.4",
    "magicattr==0.1.6",
    "MarkupSafe==2.1.5",
    "mpmath==1.3.0",
    "multidict==6.0.5",
    "multiprocess==0.70.16",
    "mypy-extensions==1.0.0",
    "networkx==3.3",
    "numpy==1.26.4",
    "packaging==24.1",
    "pandas==2.2.2",
    "pathspec==0.12.1",
    "peft==0.13.2",
    "platformdirs==4.3.6",
    "psutil==6.0.0",
    "pyarrow==17.0.0",
    "pyarrow-hotfix==0.6",
    "pydantic==2.8.2",
    "pydantic_core==2.20.1",
    "pyheck==0.1.5",
    "python-dateutil==2.9.0.post0",
    "pytz==2024.1",
    "PyYAML==6.0.2",
    "regex==2024.7.24",
    "requests==2.32.3",
    "roman==4.2",
    "safetensors==0.4.4",
    "scikit-learn==1.5.1",
    "scipy==1.14.0",
    "sentencepiece==0.2.0",
    "seqeval==1.2.2",
    "six==1.16.0",
    "sorcery==0.2.2",
    "sympy==1.13.1",
    "tasknet==1.54.0",
    "tasksource==0.0.45",
    "threadpoolctl==3.5.0",
    "tokenizers==0.19.1",
    "tqdm==4.66.5",
    "transformers==4.44.0",
    "typing_extensions==4.12.2",
    "tzdata==2024.1",
    "urllib3==2.2.2",
    "wrapt==1.16.0",
    "xxhash==3.4.1",
    "yarl==1.9.4",
]


if platform.system() == "Windows" and not check_cuda_available():
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "torch==2.3.1+cpu", "-f", "https://download.pytorch.org/whl/torch_stable.html"]
        )
    except subprocess.CalledProcessError:
        print("Failed to install torch with CPU-only version.")
else:
    install_requires.append("torch==2.4.0")

extras = {
    "cli": [
        "InquirerPy==0.3.4",
    ],
    "inference": [
        "aiohttp",
        "minijinja>=1.0",
    ],
    "torch": [
        "torch",
        "safetensors[torch]",
    ],
    "hf_transfer": [
        "hf_transfer>=0.1.4",
    ],
    "fastai": [
        "toml",
        "fastai>=2.4",
        "fastcore>=1.3.27",
    ],
    "tensorflow": [
        "tensorflow",
        "pydot",
        "graphviz",
    ],
    "tensorflow-testing": [
        "tensorflow",
        "keras<3.0",
    ],
    "typing": [
        "typing-extensions>=4.8.0",
        "types-PyYAML",
        "types-requests",
        "types-simplejson",
        "types-toml",
        "types-tqdm",
        "types-urllib3",
    ],
    "quality": [
        "ruff>=0.5.0",
        "mypy==1.5.1",
        "libcst==1.4.0",
    ],
    "all": [
        "ruff>=0.5.0",
        "mypy==1.5.1",
        "libcst==1.4.0",
        "typing-extensions>=4.8.0",
        "types-PyYAML",
        "types-requests",
        "types-simplejson",
        "types-toml",
        "types-tqdm",
        "types-urllib3",
    ],
    "dev": [
        "ruff>=0.5.0",
        "mypy==1.5.1",
        "libcst==1.4.0",
        "typing-extensions>=4.8.0",
        "types-PyYAML",
        "types-requests",
        "types-simplejson",
        "types-toml",
        "types-tqdm",
        "types-urllib3",
    ],
}

setup(
    name="hulu_evaluate",
    version=get_version(),
    author="HUN-REN Research Center for Linguistics",
    author_email="varga.kristof@nytud.hun-ren.hu",
    description="Client library to train and evaluate models on the HuLu benchmark.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="machine-learning models natural-language-processing deep-learning evaluation benchmark",
    license="Apache",
    url="https://hulu.nytud.hu/",
    package_dir={"": "src"},
    packages=find_packages("src"),
    extras_require=extras,
    entry_points={
        "console_scripts": ["hulu-evaluate=hulu_evaluate.commands.hulu_evaluate_cli:main"],
        "fsspec.specs": "hf=huggingface_hub.HfFileSystem",
    },
    python_requires=">=3.8.0",
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    include_package_data=True,
)

import sys
from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

package_name = "tracebloc_package_dev"
package_url = "https://gitlab.com/tracebloc/tracebloc-py-package/-/tree/dev"
package_author_email = "info@tracebloc.io"

# if "--live" in sys.argv:
# package_name = "tracebloc_package"
# package_url = "https://gitlab.com/tracebloc/tracebloc-py-package"
# package_author_email = "lukas-wutke@tracebloc.io"

setup(
    name=package_name,
    version="0.5.90",
    description="Package required to run Tracebloc jupyter notebook to create experiment",
    url=package_url,
    license="MIT",
    python_requires=">=3",
    packages=find_packages(),
    author="Tracebloc",
    author_email=package_author_email,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "absl-py",
        "dill",
        "protobuf",
        "requests",
        "rich",
        "silence-tensorflow",
        "tensorflow",
        "tensorflow-datasets",
        "termcolor",
        "timm",
        "torch",
        "torchlightning",
        "torchmetrics",
        "torchvision",
        "tqdm",
        "transformers",
        "twine",
    ],
    zip_safe=False,
)

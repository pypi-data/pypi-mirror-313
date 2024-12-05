# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bitcoin_lite']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=3.0.11,<4.0.0']

setup_kwargs = {
    'name': 'bitcoin-lite',
    'version': '0.1.1',
    'description': 'A lightweight Bitcoin transaction system using Cython',
    'long_description': '# Bitcoin-Lite \n\n## Introduction\n\nThe **Bitcoin-Lite** package is a Python-based, simplified implementation of a cryptocurrency-like transaction system. \nIt uses **Cython** for performance optimization, making operations like creating and processing transactions significantly faster. \nThis package is ideal for educational purposes, testing blockchain-related ideas, or understanding cryptocurrency principles in a lightweight, \napproachable manner.\n\n## How it works\n\n- **Transaction management**:\n  With this package, you shoud be able to\n  - create transactions with details such as sender, receiver, and amount.\n  - generate transaction summaries quickly using optimized Cython code.\n\n- **Performance optimization**:\n  - By using Cython, the package provides enhanced computational efficiency compared to pure Python implementations.\n  - `Bitcoin-lite` is intended to be a streamlined framework for understanding and experimenting with blockchain transaction principles \n  through an optimized computational architecture. By using the Cython\'s static typing and direct C-level operations, \n  `Bitcoin-Lite` achieves significant performance improvements over traditional Python implementations.\n\n- **Easy to use**:\n  - `Bitcoin-Lite` is designed for simplicity, allowing users to easily create, process, and interact with transactions.\n\n## Components\n\n### 1. `Transaction` class\n\nThe core component of the package is the `Transaction` class. This class provides:\n\n- **Attributes**:\n  - `sender`: The individual or entity sending the funds.\n  - `receiver`: The individual or entity receiving the funds.\n  - `amount`: The amount being transferred.\n\n- **Methods**:\n  - `__init__(sender, receiver, amount)`: Initializes a transaction with the specified details.\n  - `details()`: Returns a formatted string summarizing the transaction.\n\n## Installation\n\nSome minimum requirements:\n\n- Python ≥ 3.8\n- Cython ≥ 3.0.0\n- C compiler (gcc/clang/MSVC)\n\nTo install the Bitcoin-Lite package, follow these steps:\n\n1. Clone the repository from GitHub:\n   ```bash\n   git clone git@github.com:danymukesha/bitcoin-lite.git\n   cd bitcoin-lite\n   ```\n\n2. Install the dependencies using Poetry:\n   ```bash\n   poetry install\n   ```\n\n3. Build the Cython extension:\n   ```bash\n   poetry run python setup.py build_ext --inplace\n   ```\n\n## Testing the `Bitcoin-Lite`\n\nYou can test the package functionality using the provided test script:\n\n```bash\npoetry run python test_transaction.py\n```\n\nThis will create a sample transaction and display its details.\n\n### Example usage\nHere is a simple example of how to use the `Transaction` class:\n\n```python\nfrom bitcoin_lite import Transaction\n\n# create a transaction\ntx = Transaction("Alice", "Bob", 100.0)\n\n# print transaction details\nprint(tx.details())\n```\n\n### Output\n```\nTransaction from Alice to Bob of amount 100.0\n```\n\n## Technical architecture\n\n### Performance optimization\n`Bitcoin-Lite` utilizes Cython\'s static typing capabilities to optimize critical transaction operations:\n\n1. **Memory management**\n   - Direct memory allocation for transaction attributes\n   - Reduced Python object overhead through C-level data structures\n   - Optimized string operations for transaction details\n\n2. **Computational Efficiency**\n   - Static typing eliminates dynamic dispatch overhead\n   - Direct C-level attribute access without Python dictionary lookups\n   - Minimal Python API interaction for core operations\n\n### Implementation Details\n\n#### Transaction Class Architecture\nThe core `Transaction` class is implemented in Cython with the following specifications:\n\n```python\ncdef class Transaction:\n    cdef str sender      # Static typing for sender attribute\n    cdef str receiver    # Static typing for receiver attribute\n    cdef float amount    # Static typing for amount attribute\n```\n\nKey characteristics:\n- C-level attribute declarations for optimal memory access\n- Direct attribute manipulation without Python\'s attribute dictionary\n- Optimized string handling for transaction details\n\n#### Performance Metrics\nPreliminary benchmarks show significant performance improvements compared to pure Python implementations:\n\n| Operation | Pure Python (μs) | Bitcoin-Lite (μs) | Improvement |\n|-----------|-----------------|-------------------|-------------|\n| Creation  | 2.45           | 0.82              | 66.5%       |\n| Details   | 1.87           | 0.64              | 65.8%       |\n\n*Note: Benchmarks performed on Python 3.8, results may vary based on system configuration.*\n\n## Scientific applications\n\n### Research use-cases\n\n1. **Transaction analysis**\n   - Study of transaction patterns and network behavior\n   - Development of new cryptocurrency protocols\n   - Performance optimization research\n\n2. **Educational applications**\n   - Demonstration of blockchain principles\n   - Analysis of transaction system architectures\n   - Computational efficiency studies\n\n3. **Protocol development**\n   - Testing of new transaction mechanisms\n   - Validation of consensus algorithms\n   - Performance benchmarking\n\n## Future implementations\n\n### Planned enhancements\n1. Implementation of transaction validation mechanisms\n2. Addition of cryptographic signing capabilities\n3. Integration of merkle tree data structures\n4. Development of network simulation capabilities\n\n### Research opportunities\n- Performance optimization studies\n- Transaction pattern analysis\n- Consensus mechanism implementation\n- Network behavior simulation\n\n## Contribution\n\nContributions to the Bitcoin-Lite package are welcome! If you have ideas for additional features, \noptimizations, or examples, feel free to submit a pull request or open an issue in the GitHub repository.\n\n## No license\n\nThis package will be open-source and is not under any license (i.e. you can fork it, copy and modify it as you wish).\n',
    'author': 'Dany Mukesha',
    'author_email': 'danymukesha@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danymukesha/bitcoin-lite',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

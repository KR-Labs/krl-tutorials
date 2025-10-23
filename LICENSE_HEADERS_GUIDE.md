# License Header Guide

This guide explains how to add appropriate license headers to files in the krl-tutorials repository.

## Dual License Structure

This repository uses dual licensing:
- **MIT License** for code (LICENSE-CODE)
- **CC-BY-SA-4.0** for content (LICENSE-CONTENT)

## License Headers by File Type

### Python Files (.py)

```python
# Copyright (c) 2025 KR-Labs. All rights reserved.
# Licensed under the MIT License
# See LICENSE-CODE for details
```

### Jupyter Notebooks (.ipynb)

Add to the first markdown cell:

```markdown
© 2025 KR-Labs. All rights reserved.  
KR-Labs™ is a trademark of Quipu Research Labs, LLC, a subsidiary of Sundiata Giddasira, Inc.

**License:**  
- Code: MIT License ([LICENSE-CODE](../../LICENSE-CODE))  
- Content: CC-BY-SA-4.0 ([LICENSE-CONTENT](../../LICENSE-CONTENT))

SPDX-License-Identifier: MIT AND CC-BY-SA-4.0
```

### Markdown Files (.md)

```markdown
<!--
Copyright (c) 2025 KR-Labs. All rights reserved.
Licensed under CC-BY-SA-4.0
See LICENSE-CONTENT for details
-->
```

### README Files in Notebooks

Add to the bottom:

```markdown
---

**License:**  
- Code examples: MIT License  
- Tutorial content: CC-BY-SA-4.0

See repository [LICENSE](../../LICENSE) for details.

© 2025 KR-Labs. All rights reserved.  
KR-Labs™ is a trademark of Quipu Research Labs, LLC, a subsidiary of Sundiata Giddasira, Inc.
```

## Quick Reference

| File Type | Primary Content | License | Header Template |
|-----------|----------------|---------|-----------------|
| `.py` | Code | MIT | Python header |
| `.ipynb` | Mixed | Dual | Notebook header |
| `.md` | Documentation | CC-BY-SA-4.0 | Markdown header |
| `README.md` | Documentation | CC-BY-SA-4.0 | README footer |

## When in Doubt

- **Executable content** (can be run) → MIT License
- **Educational content** (text, explanations) → CC-BY-SA-4.0
- **Mixed content** (Jupyter notebooks) → Mention both licenses

## Attribution Requirements

### Using Code (MIT License)
```python
# Based on KRL Tutorials (https://github.com/KR-Labs/krl-tutorials)
# Copyright (c) 2025 KR-Labs
# Licensed under MIT License
```

### Using Content (CC-BY-SA-4.0)
```markdown
Adapted from KRL Tutorials by KR-Labs  
https://github.com/KR-Labs/krl-tutorials  
Licensed under CC-BY-SA-4.0
```

## Examples

### Good: Python Script
```python
#!/usr/bin/env python3
# Copyright (c) 2025 KR-Labs. All rights reserved.
# Licensed under the MIT License
# See LICENSE-CODE for details

"""
Data analysis utilities for KRL tutorials.
"""

import pandas as pd

def load_data(file_path):
    """Load data from CSV file."""
    return pd.read_csv(file_path)
```

### Good: Markdown Documentation
```markdown
<!--
Copyright (c) 2025 KR-Labs. All rights reserved.
Licensed under CC-BY-SA-4.0
See LICENSE-CONTENT for details
-->

# Getting Started with KRL Analytics

This tutorial covers the basics of...
```

### Good: Mixed Jupyter Notebook
First cell (markdown):
```markdown
# Income & Poverty Analysis Tutorial

© 2025 KR-Labs. All rights reserved.  
KR-Labs™ is a trademark of Quipu Research Labs, LLC

**License:**  
Code: MIT | Content: CC-BY-SA-4.0  
See [LICENSE](../../LICENSE)
```

## Automated License Checking

To verify license headers:

```bash
# Check Python files
grep -r "Licensed under the MIT License" --include="*.py" .

# Check Jupyter notebooks
grep -r "License:" --include="*.ipynb" .

# Check Markdown files
grep -r "Licensed under CC-BY-SA-4.0" --include="*.md" .
```

## Questions?

For licensing questions, contact: info@krlabs.dev

---

© 2025 KR-Labs. All rights reserved.  
KR-Labs™ is a trademark of Quipu Research Labs, LLC, a subsidiary of Sundiata Giddasira, Inc.

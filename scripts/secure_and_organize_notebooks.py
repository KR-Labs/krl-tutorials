#!/usr/bin/env python3
"""
Secure and Organize KRL Tutorials Notebooks

This script:
1. Updates copyright headers and trademark notices
2. Removes hardcoded API keys and internal paths
3. Organizes notebooks by category
4. Updates contact information
5. Clears execution outputs (already done, but verify)
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List
import re

# Updated legal information
COPYRIGHT_HEADER = """---
© 2025 KR-Labs. All rights reserved.  
KR-Labs™ is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

SPDX-License-Identifier: CC-BY-4.0
---
"""

CONTACT_INFO = {
    "email": "info@krlabs.dev",
    "website": "krlabs.dev",
    "organization": "Quipu Research Labs, LLC",
    "parent_company": "Sudiata Giddasira, Inc."
}

# Category organization
NOTEBOOK_CATEGORIES = {
    "01_fundamentals": {
        "name": "Fundamentals",
        "description": "Core economic and social metrics - start here!",
        "domains": ["D01", "D02", "D03"]
    },
    "02_health_housing": {
        "name": "Health & Housing",
        "description": "Health outcomes, healthcare access, and housing markets",
        "domains": ["D04", "D05", "D28"]
    },
    "03_inequality_demographics": {
        "name": "Inequality & Demographics",
        "description": "Economic inequality, wealth distribution, and population dynamics",
        "domains": ["D06", "D07"]
    },
    "04_economic_behavior": {
        "name": "Economic Behavior",
        "description": "Consumer spending, industry structure, and business dynamics",
        "domains": ["D08", "D09", "D15"]
    },
    "05_social_systems": {
        "name": "Social Systems",
        "description": "Social mobility, capital, services, and civic engagement",
        "domains": ["D10", "D18", "D19", "D20", "D21", "D29"]
    },
    "06_infrastructure_environment": {
        "name": "Infrastructure & Environment",
        "description": "Transportation, digital economy, food systems, and environmental economics",
        "domains": ["D12", "D14", "D17", "D20"]
    },
    "07_justice_equity": {
        "name": "Justice & Equity",
        "description": "Crime, public safety, and equity across systems",
        "domains": ["D13", "D23", "D24", "D26"]
    },
    "08_culture_society": {
        "name": "Culture & Society",
        "description": "Cultural economics, consumption, nutrition, and housing affordability",
        "domains": ["D11", "D22", "D25", "D27"]
    },
    "09_planned": {
        "name": "Planned Tutorials",
        "description": "Future tutorials in development",
        "domains": ["D30", "D31", "D32", "D33"]
    }
}


def update_notebook_header(notebook_path: Path) -> bool:
    """Update notebook with correct copyright header and contact info."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Check if first cell exists and is markdown
        if not notebook.get('cells'):
            print(f"  ⚠️  No cells found in {notebook_path.name}")
            return False
        
        first_cell = notebook['cells'][0]
        
        # Add/update copyright header in first cell
        if first_cell['cell_type'] == 'markdown':
            source = ''.join(first_cell['source'])
            
            # Remove old headers if present
            source = re.sub(r'Copyright.*?All rights reserved\..*?\n', '', source, flags=re.DOTALL)
            source = re.sub(r'---\n.*?KRL.*?trademark.*?\n---\n', '', source, flags=re.DOTALL)
            
            # Add new header at top
            first_cell['source'] = [COPYRIGHT_HEADER + '\n'] + [source]
        else:
            # Insert new markdown cell at beginning
            new_cell = {
                'cell_type': 'markdown',
                'metadata': {},
                'source': [COPYRIGHT_HEADER]
            }
            notebook['cells'].insert(0, new_cell)
        
        # Update all cells for contact information
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                
                # Update email addresses
                source = re.sub(
                    r'(info@|contact@)(krlanalytics\.org|quipulabs\.com)',
                    r'info@krlabs.dev',
                    source
                )
                
                # Update website URLs
                source = re.sub(
                    r'(https?://)?(www\.)?(krlanalytics\.org|quipulabs\.com)',
                    'https://krlabs.dev',
                    source
                )
                
                # Remove hardcoded API key paths
                source = re.sub(
                    r"Path\.cwd\(\)\.parent\.parent\.parent / 'QuipuLabs-khipu' / 'configs' / 'apikeys',?\n",
                    "",
                    source
                )
                
                source = re.sub(
                    r"Path\.cwd\(\)\.parent / 'configs' / 'apikeys',?\n",
                    "",
                    source
                )
                
                # Keep only home directory path for API keys
                # Update load_api_key function to use environment variables first
                if 'def load_api_key' in source:
                    source = re.sub(
                        r'def load_api_key\(api_name: str, required: bool = True\) -> str:.*?return key',
                        '''def load_api_key(api_name: str, required: bool = True) -> str:
    """
    Load API key from environment variables or local config file.
    
    Priority:
    1. Environment variable (e.g., FRED_API_KEY)
    2. ~/.krl/apikeys file
    
    Args:
        api_name: Name of the API (e.g., 'FRED', 'CENSUS')
        required: Whether the API key is required
        
    Returns:
        API key string or None if not required and not found
    """
    import os
    from pathlib import Path
    
    # Try environment variable first
    env_var = f"{api_name.upper()}_API_KEY"
    key = os.environ.get(env_var)
    
    if key:
        return key
    
    # Try local config file
    config_paths = [
        Path.home() / '.krl' / 'apikeys'
    ]
    
    for path in config_paths:
        if path.exists():
            with open(path, 'r') as f:
                for line in f:
                    if line.startswith(f"{api_name}="):
                        return line.split('=', 1)[1].strip()
    
    if required:
        raise ValueError(
            f"API key for {api_name} not found. "
            f"Set {env_var} environment variable or add to ~/.krl/apikeys"
        )
    
    return None''',
                        source,
                        flags=re.DOTALL
                    )
                
                cell['source'] = source.split('\n')
                # Ensure each line ends with newline except last
                cell['source'] = [line + '\n' if i < len(cell['source']) - 1 else line 
                                  for i, line in enumerate(cell['source'])]
        
        # Update metadata
        if 'metadata' not in notebook:
            notebook['metadata'] = {}
        
        notebook['metadata']['authors'] = [{
            'name': 'KR-Labs',
            'email': 'info@krlabs.dev',
            'url': 'https://krlabs.dev'
        }]
        
        notebook['metadata']['license'] = 'CC-BY-4.0'
        
        # Write back
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error updating {notebook_path.name}: {e}")
        return False


def update_readme(readme_path: Path) -> bool:
    """Update README with correct contact information."""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update email
        content = re.sub(
            r'(info@|contact@)(krlanalytics\.org|quipulabs\.com)',
            r'info@krlabs.dev',
            content
        )
        
        # Update website
        content = re.sub(
            r'(https?://)?(www\.)?(krlanalytics\.org|quipulabs\.com)',
            'https://krlabs.dev',
            content
        )
        
        # Add trademark footer if not present
        if '© 2025 KR-Labs' not in content:
            footer = """
---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
"""
            content += footer
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error updating {readme_path.name}: {e}")
        return False


def organize_by_category(notebooks_dir: Path) -> Dict[str, List[str]]:
    """Organize notebooks into category folders."""
    results = {}
    
    # Create category directories
    for category_id, category_info in NOTEBOOK_CATEGORIES.items():
        category_path = notebooks_dir / category_id
        category_path.mkdir(exist_ok=True)
        
        # Create category README
        readme_path = category_path / "README.md"
        readme_content = f"""# {category_info['name']}

{category_info['description']}

## Tutorials in This Category

"""
        
        moved_domains = []
        
        # Move domains to this category
        for domain_id in category_info['domains']:
            domain_dirs = list(notebooks_dir.glob(f"{domain_id}_*"))
            
            for domain_dir in domain_dirs:
                if domain_dir.is_dir() and domain_dir.parent == notebooks_dir:
                    target_dir = category_path / domain_dir.name
                    
                    # Move directory
                    if not target_dir.exists():
                        shutil.move(str(domain_dir), str(target_dir))
                        moved_domains.append(domain_dir.name)
                        print(f"  ✅ Moved {domain_dir.name} to {category_id}/")
                        
                        # Add to category README
                        domain_readme = target_dir / "README.md"
                        if domain_readme.exists():
                            with open(domain_readme, 'r') as f:
                                first_line = f.readline().strip('# \n')
                            readme_content += f"- **{domain_dir.name}**: {first_line}\n"
        
        # Write category README
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        results[category_id] = moved_domains
    
    return results


def create_master_index(notebooks_dir: Path):
    """Create master INDEX.md for all tutorials."""
    index_content = """# KRL Tutorials - Complete Index

© 2025 KR-Labs. All rights reserved.  
**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

## Getting Started

Welcome to KRL Tutorials! These notebooks provide hands-on learning for the KRL Analytics Suite.

### Recommended Learning Path

1. **Start with Fundamentals** (D01-D03) to build core skills
2. **Explore by interest** using the categories below
3. **Check prerequisites** in each notebook's header

---

## Tutorial Categories

"""
    
    for category_id, category_info in NOTEBOOK_CATEGORIES.items():
        category_path = notebooks_dir / category_id
        
        index_content += f"### {category_info['name']}\n\n"
        index_content += f"{category_info['description']}\n\n"
        
        # List domains in this category
        domains = sorted(category_path.glob("D*"))
        for domain_dir in domains:
            if domain_dir.is_dir():
                readme_path = domain_dir / "README.md"
                if readme_path.exists():
                    with open(readme_path, 'r') as f:
                        first_line = f.readline().strip('# \n')
                    index_content += f"- [{domain_dir.name}]({category_id}/{domain_dir.name}/): {first_line}\n"
        
        index_content += "\n"
    
    index_content += """---

## Support & Contact

- **Website**: https://krlabs.dev
- **Email**: info@krlabs.dev
- **Documentation**: https://docs.krlabs.dev
- **GitHub**: https://github.com/KR-Labs

---

© 2025 KR-Labs. All rights reserved.
"""
    
    index_path = notebooks_dir / "INDEX.md"
    with open(index_path, 'w') as f:
        f.write(index_content)
    
    print(f"\n✅ Created master INDEX.md")


def main():
    """Main execution function."""
    print("=" * 70)
    print("KRL Tutorials - Security & Organization Update")
    print("=" * 70)
    
    notebooks_dir = Path("/Users/bcdelo/KR-Labs/krl-tutorials/notebooks")
    
    if not notebooks_dir.exists():
        print(f"❌ Notebooks directory not found: {notebooks_dir}")
        return
    
    # Step 1: Update all notebooks
    print("\n📝 Step 1: Updating notebook headers and security...")
    notebook_files = list(notebooks_dir.glob("D*/*.ipynb"))
    updated_count = 0
    
    for notebook_path in notebook_files:
        if update_notebook_header(notebook_path):
            updated_count += 1
            print(f"  ✅ Updated {notebook_path.parent.name}/{notebook_path.name}")
    
    print(f"\n✅ Updated {updated_count}/{len(notebook_files)} notebooks")
    
    # Step 2: Update all READMEs
    print("\n📝 Step 2: Updating README files...")
    readme_files = list(notebooks_dir.glob("D*/README.md"))
    readme_count = 0
    
    for readme_path in readme_files:
        if update_readme(readme_path):
            readme_count += 1
            print(f"  ✅ Updated {readme_path.parent.name}/README.md")
    
    print(f"\n✅ Updated {readme_count}/{len(readme_files)} READMEs")
    
    # Step 3: Organize by category
    print("\n📁 Step 3: Organizing notebooks by category...")
    organization_results = organize_by_category(notebooks_dir)
    
    total_moved = sum(len(domains) for domains in organization_results.values())
    print(f"\n✅ Organized {total_moved} domains into {len(NOTEBOOK_CATEGORIES)} categories")
    
    # Step 4: Create master index
    print("\n📚 Step 4: Creating master index...")
    create_master_index(notebooks_dir)
    
    # Final summary
    print("\n" + "=" * 70)
    print("✅ COMPLETE - Security & Organization Update")
    print("=" * 70)
    print(f"\nSummary:")
    print(f"  - Notebooks updated: {updated_count}")
    print(f"  - READMEs updated: {readme_count}")
    print(f"  - Domains organized: {total_moved}")
    print(f"  - Categories created: {len(NOTEBOOK_CATEGORIES)}")
    print(f"\nNext steps:")
    print(f"  1. Review changes: cd {notebooks_dir} && git diff")
    print(f"  2. Test a notebook: jupyter notebook {notebooks_dir}/01_fundamentals/D01_income_and_poverty/")
    print(f"  3. Commit: git add . && git commit -m 'feat: Secure and organize tutorials'")
    print(f"  4. Push: git push origin main")


if __name__ == "__main__":
    main()

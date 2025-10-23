# Wiki Content for KRL Tutorials

This directory contains the source content for the [KRL Tutorials Wiki](https://github.com/KR-Labs/krl-tutorials/wiki).

## Publishing to GitHub Wiki

GitHub wikis must be initialized and populated through the web interface or by cloning the wiki repository. To publish these pages:

### Method 1: Web Interface

1. Go to https://github.com/KR-Labs/krl-tutorials/wiki
2. Click "Create the first page"
3. For each markdown file in this directory:
   - Click "New Page"
   - Copy the filename (without .md) as the page title
   - Paste the content
   - Save

### Method 2: Git Clone

```bash
# Clone the wiki repository
git clone https://github.com/KR-Labs/krl-tutorials.wiki.git

# Copy wiki content
cp docs/wiki/*.md krl-tutorials.wiki/

# Commit and push
cd krl-tutorials.wiki
git add *.md
git commit -m "Add comprehensive wiki documentation"
git push origin master
```

## Wiki Pages

### Core Pages
- **Home.md** - Wiki homepage with navigation
- **Installation-and-Setup.md** - Setup guide
- **Quick-Start-Guide.md** - 5-minute getting started
- **FAQ.md** - Frequently asked questions

### Reference Pages
- **Analytical-Tiers-Guide.md** - Understanding the 6-tier framework
- **Data-Sources.md** - API access and data documentation
- **Tutorial-Catalog.md** - Complete listing of all 33 tutorials

### Additional Pages (TODO)
- Learning-Paths.md - Structured curricula
- Code-Examples.md - Common code patterns
- Troubleshooting.md - Common issues and solutions
- Contributing-Guide.md - How to contribute
- Development-Setup.md - Dev environment setup

## Wiki Structure

```
Home
├── Getting Started
│   ├── Installation & Setup
│   ├── Quick Start Guide
│   └── Learning Paths
│
├── Domain References
│   ├── Economic Analytics
│   ├── Social & Policy Analytics
│   └── Advanced Topics
│
├── Technical Documentation
│   ├── Analytical Tiers Guide
│   ├── Data Sources
│   ├── Code Examples
│   └── Troubleshooting
│
└── Contributing
    ├── Contributing Guide
    ├── Code of Conduct
    └── Development Setup
```

## Updating Wiki Content

1. Edit files in `docs/wiki/`
2. Test locally (preview markdown)
3. Commit to main repository
4. Update wiki (use Method 1 or 2 above)

## Naming Conventions

- **Filenames**: `Page-Title-With-Hyphens.md`
- **Links**: Use the filename without `.md` in wiki links
- **Images**: Store in wiki repo or link to main repo

## Cross-Linking

Use wiki syntax for internal links:
```markdown
[Link Text](Page-Name-Without-Extension)
```

For main repo files:
```markdown
[Link Text](https://github.com/KR-Labs/krl-tutorials/blob/main/path/to/file)
```

## Maintenance

- Review wiki quarterly for accuracy
- Update when new tutorials are added
- Keep code examples synchronized with notebooks
- Respond to community feedback

## License

Wiki content follows the same dual licensing as the main repository:
- **Code examples**: MIT License
- **Documentation content**: CC-BY-SA-4.0

---

**Last Updated**: October 2025

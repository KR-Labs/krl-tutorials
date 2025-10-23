# Frequently Asked Questions (FAQ)

Common questions and answers about KRL Tutorials.

## Getting Started

### Q: Do I need to know Python to use these tutorials?

**A:** Basic Python knowledge is helpful but not strictly required. Each tutorial includes:
- Clear explanations of what the code does
- Well-commented code blocks
- Step-by-step progression

**Recommended**: Complete a basic Python tutorial first if you're completely new:
- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [Kaggle Python Course](https://www.kaggle.com/learn/python)

### Q: Do I need to pay for data access?

**A:** No! All data sources used are free:
- **Synthetic data**: Included in notebooks, no setup required
- **Public APIs**: Free registration with Census, FRED, CDC, etc.
- **Open datasets**: No authentication needed

### Q: Which tutorial should I start with?

**A:** Depends on your background:
- **Complete beginner**: D01 (Income & Wealth) - Most accessible
- **Have economics background**: Any domain of interest
- **Data scientist**: Jump to Tier 3+ in any domain
- **Researcher**: Domain-specific based on your field

See **[Learning Paths](Learning-Paths)** for detailed recommendations.

### Q: Can I run these tutorials in Google Colab?

**A:** Yes! Click "Open in Colab" at the top of each notebook, or:
1. Upload the `.ipynb` file to Google Drive
2. Right-click → Open with → Google Colaboratory
3. Install required packages: `!pip install -r config/requirements_opensource.txt`

### Q: How long does each tutorial take?

**A:**
- **Tier 1 only**: 20-30 minutes
- **Tiers 1-2**: 45-60 minutes
- **All tiers**: 2-3 hours (if studying deeply)
- **With modifications/experiments**: 3-5 hours

## Technical Questions

### Q: Why am I getting "ModuleNotFoundError"?

**A:** Missing dependency. Install it:
```bash
pip install [package-name]
```

Or reinstall all requirements:
```bash
pip install -r config/requirements_opensource.txt
```

### Q: My plots aren't showing. How do I fix this?

**A:** Add this to the first code cell:
```python
%matplotlib inline
import matplotlib.pyplot as plt
```

For interactive plots:
```python
import plotly.io as pio
pio.renderers.default = 'notebook'  # or 'colab' for Google Colab
```

### Q: How do I get API keys?

**A:** See **[Installation & Setup - API Keys](Installation-and-Setup#api-keys-setup)**

Quick links:
- **Census**: https://api.census.gov/data/key_signup.html
- **FRED**: https://fred.stlouisfed.org/docs/api/api_key.html
- **BLS**: https://www.bls.gov/developers/home.htm

### Q: Can I use my own data with these notebooks?

**A:** Absolutely! The tutorials are designed to be adaptable:

```python
# Instead of synthetic/API data, load your own
df = pd.read_csv('your_data.csv')

# Then run the analysis code with your data
# Just ensure column names match or update them
```

### Q: Which Python version do I need?

**A:** Python 3.9 or higher is recommended. Check your version:
```bash
python --version
```

## Content Questions

### Q: What's the difference between the tiers?

**A:** See **[Analytical Tiers Guide](Analytical-Tiers-Guide)** for details:
- **Tier 1**: Descriptive ("What happened?")
- **Tier 2**: Predictive ("What will happen?")
- **Tier 3**: Causal ("What caused this?")
- **Tier 4**: Unsupervised ("What patterns exist?")
- **Tier 5**: Advanced ML
- **Tier 6**: Network/Spatial

### Q: Why use synthetic data when real data is available?

**A:** Synthetic data offers several advantages:
- ✅ Works offline (no internet required)
- ✅ No API setup needed
- ✅ Perfectly reproducible
- ✅ Educational focus (cleaner patterns)
- ✅ No rate limits

For real analysis, use the real data sections!

### Q: Are these tutorials peer-reviewed?

**A:** The methodologies are based on peer-reviewed research (see References sections). The tutorials themselves are:
- Community-reviewed through GitHub
- Based on established academic methods
- Regularly updated with feedback

### Q: Can I cite these tutorials in academic work?

**A:** Yes! Each tutorial includes a citation block:

```bibtex
@software{krl_tutorials,
  author = {KR-Labs},
  title = {KRL Analytics Tutorials},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/KR-Labs/krl-tutorials}
}
```

For specific domains, cite relevant academic sources from the References section.

### Q: What's the difference between MIT and CC-BY-SA licenses?

**A:**
- **MIT (Code)**: Use freely, even commercially. Just include license text.
- **CC-BY-SA-4.0 (Content)**: Use freely, give attribution, share improvements under same license.

See **[LICENSE](https://github.com/KR-Labs/krl-tutorials/blob/main/LICENSE)** for full details.

## Usage & Applications

### Q: Can I use these for teaching a class?

**A:** Yes! That's encouraged. The dual licensing allows:
- Using in academic courses
- Modifying for your curriculum
- Creating derivative materials
- Just provide attribution and share improvements

### Q: Can I use these tutorials for commercial training?

**A:** Yes for code (MIT), but content requires sharing under CC-BY-SA-4.0. This means:
- ✅ Use in corporate training
- ✅ Modify for your needs
- ⚠️ Must share modified content under CC-BY-SA
- ✅ Attribute KR-Labs

### Q: Can I include these tutorials in a book?

**A:** Yes, with attribution and sharing under CC-BY-SA. Contact us for specific arrangements.

### Q: How do I contribute improvements?

**A:** See **[Contributing Guide](Contributing-Guide)**. Quick version:
1. Fork the repository
2. Make your improvements
3. Submit a pull request
4. We review and merge

## Domain-Specific Questions

### Q: Which tutorials cover causal inference?

**A:** Causal inference (Tier 3) appears in:
- D01: Income & Wealth (income policies)
- D02: Health Economics (insurance effects)
- D05: Labor Force (employment programs)
- D06: Crime Statistics (policing interventions)
- D10: Intergenerational Mobility (education investments)

### Q: Which tutorials are best for policy analysis?

**A:** All tutorials apply to policy! Particularly relevant:
- **Economic policy**: D01, D02, D03, D04, D05
- **Social policy**: D06, D07, D08, D09, D10
- **Evaluation methods**: Any tutorial with Tier 3 content

### Q: I'm a healthcare analyst. Which tutorials should I focus on?

**A:**
1. **Start**: D02 (Health Economics)
2. **Then**: D04 (Education/Health connections)
3. **Also**: D08 (Demographics/Health)
4. **Advanced**: D30 (Subjective Well-Being)

### Q: Where's the finance/financial markets content?

**A:** Currently limited, but financial data appears in:
- D01: Wealth inequality (asset markets)
- D03: Housing markets
- Future tutorials may expand this

## Troubleshooting

### Q: Kernel keeps crashing. What do I do?

**A:**
1. Restart kernel: `Kernel → Restart`
2. Clear outputs: `Cell → All Output → Clear`
3. Check memory usage (may need to subsample data)
4. Close other notebooks
5. Restart Jupyter entirely

### Q: Code runs but gives wrong results. Help?

**A:** Check:
1. Did you run all cells in order?
2. Did you modify earlier cells and forget to re-run?
3. Are your data types correct? (`df.dtypes`)
4. Any warning messages that were ignored?

### Q: How do I report a bug?

**A:**
1. Check if [issue already exists](https://github.com/KR-Labs/krl-tutorials/issues)
2. If not, [open new issue](https://github.com/KR-Labs/krl-tutorials/issues/new?template=bug_report.yml)
3. Include:
   - Which tutorial/notebook
   - Python version
   - Error message (full traceback)
   - What you were trying to do

## Advanced Topics

### Q: Can I run these on a server/HPC cluster?

**A:** Yes! Use Jupyter server:
```bash
jupyter notebook --no-browser --port=8888
# Then SSH tunnel: ssh -L 8888:localhost:8888 user@server
```

### Q: How do I optimize for large datasets?

**A:**
```python
# Use chunks
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process(chunk)

# Use Dask for parallel processing
import dask.dataframe as dd
df = dd.read_csv('large_file.csv')
```

### Q: Can I deploy these as web apps?

**A:** Yes! Consider:
- **Streamlit**: Quick interactive dashboards
- **Dash**: More customizable
- **Voilà**: Turn notebooks into web apps
- **Jupyter Book**: Static documentation

### Q: How do I automate these analyses?

**A:**
- **Papermill**: Parameterize and execute notebooks
- **Scheduled execution**: Use cron/Task Scheduler
- **APIs**: Use nbconvert to extract code

## Community & Support

### Q: Where can I ask questions?

**A:**
1. **[GitHub Discussions](https://github.com/KR-Labs/krl-tutorials/discussions)** - Best for general questions
2. **[Issues](https://github.com/KR-Labs/krl-tutorials/issues)** - For bugs/errors
3. **[Support](https://github.com/KR-Labs/krl-tutorials/blob/main/.github/SUPPORT.md)** - Full support guide

### Q: Is there a community forum or chat?

**A:** GitHub Discussions serves this purpose. For real-time help, see if a community chat has been established.

### Q: How often are tutorials updated?

**A:** 
- **Bug fixes**: As needed
- **Data updates**: Annually (when new data releases)
- **New tutorials**: Ongoing development
- **Methodology updates**: As field evolves

### Q: Can I request a new tutorial topic?

**A:** Yes! [Open a feature request](https://github.com/KR-Labs/krl-tutorials/issues/new?template=feature_request.yml) with:
- Domain/topic
- Why it's valuable
- Potential data sources
- Use cases

## Legal & Licensing

### Q: Who owns the copyright?

**A:** KR-Labs retains copyright. Content is dual-licensed:
- **Code**: MIT License (permissive)
- **Content**: CC-BY-SA-4.0 (share-alike)

### Q: Can I remove the license headers from notebooks?

**A:** No, license headers must remain. They're part of the license requirements.

### Q: What constitutes "attribution"?

**A:** Include:
- Link to original repository
- "Based on KRL Tutorials by KR-Labs"
- Preserve license notices

### Q: Can I sell these tutorials?

**A:** You can charge for:
- Your teaching/training services
- Custom modifications
- Consulting

But modified content must also be CC-BY-SA (share improvements).

## Still Have Questions?

- **Search the [Wiki](Home)** - May already be documented
- **Check [Issues](https://github.com/KR-Labs/krl-tutorials/issues)** - Someone may have asked
- **Ask in [Discussions](https://github.com/KR-Labs/krl-tutorials/discussions)** - Community help
- **Read [Support Guide](https://github.com/KR-Labs/krl-tutorials/blob/main/.github/SUPPORT.md)** - Comprehensive support info

---

**Last Updated**: October 2025 | **Tutorials**: 33 | **Questions Answered**: 50+

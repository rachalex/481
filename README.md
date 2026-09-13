This GitHub repository contains all code, prompts, and data utilized to generate findings and conclusions presented in the our paper:

** Daniel Janies, Rachel Alexander, Khaled Obeid, and Ward Wheeler (2026) **
* Novel methods for direct characterization of reassortment events and their application in H5 Influenza A outbreaks *

## Abstract
Reassortment resulting from the exchange of genomic segments during co-infection of a host cell with distinct influenza lineage can generate a highly pathogenic, outbreak-driving lineage. These outbreak driving reassortants are capable of destabilizing poultry industries and pose a zoonotic threat to agriculture and public health. The recent invasion of North America and subsequent deaths illustrate that H5N1 reassortment events represent ongoing threats to humans. In this study, we constructed a dataset of 481 genomic sequences of H5NX (X for variable subtypes) of non-reassortant and reassortant viral isolates. We applied a novel graph model (PhyG) to detect reticulation events in phylogenetic networks indicating reassortment. Validated against Gemini model classifications, the graph model demonstrated high recall (87.27%) for reassortant categorization and achieved a Matthews Correlation Coefficient (MCC) of +0.2199 (p < 0.0001), indicating statistically significant predictive utility. Our findings establish the graph model as an efficient, sequence-based screening tool that operates independently of prior knowledge of pathogen lineages. This approach provides a robust framework for identifying dangerous reassortant events to warn of and abate future outbreaks in influenza and other dangerous viruses.

---

## Environmental Setup
git clone (https://github.com/rachalex/481.git)
cd 481

## Create virtual environment
conda create -n myenv python=3.10 -y
conda activate myenv

## Install dependencies
pip install -r requirements.txt

---

## Repository Structure
```text
📁 481/
├── 📁 data/                  # Input datasets & source files
├── 📁 outputs/               # Generated results & output graphs
├── 📁 trees/                 # Graphviz tree output files
├── 📄 481tograph_revised.py  # Graph visualization script
├── 📄 481v2.py               # Main analysis pipeline script
├── 📄 README.md              # Repository overview & instructions
└── 📄 requirements.txt       # Python package dependencies
````

---
## Contact
Dr. Daniel Janies: djanies@charlotte.edu

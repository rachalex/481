This GitHub repository contains all code, prompts, and data utilized to generate findings and conclusions presented in the our paper:

** Daniel Janies, Rachel Alexander, Khaled Obeid, and Ward Wheeler (2026) **
* Novel methods for direct characterization of reassortment events and their application in H5 Influenza A outbreaks *

## Abstract
Reassortment is a biological reality for Influenza A. While the vast majority of these events sustain a low-level baseline of survival in wild bird populations, a rare, volatile segment swap can instantly generate a highly pathogenic, outbreak-driving lineage capable of destabilizing poultry industries and posing a distinct zoonotic threat to public health. H5NX reassortment events represent ongoing threats to global health and economic security. In this study, we constructed a dataset of 481 genomic sequences of reassortant viral isolates and applied a novel phylogenetic graph model (PhyG) to detect reticulation events signifying reassortment. Validated against Gemini model classifications, the graph model demonstrated high recall (87.27%) for reassortant categorization and achieved a Matthews Correlation Coefficient (MCC) of +0.2199 (p < 0.0001), indicating statistically significant predictive utility. Our findings establish the graph model as an efficient, sequence-based screening tool that operates independently of prior knowledge of pathogen lineages. This approach provides a robust framework for identifying dangerous reassortant events to abate potential future outbreaks.

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


## Contact
Dr. Daniel Janies: djanies@charlotte.edu

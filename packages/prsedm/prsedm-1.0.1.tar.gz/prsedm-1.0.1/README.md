# PRSedm

![Graphical Abstract](https://github.com/sethsh7/PRSedm/raw/main/misc/graphical_abstract.png)

## Overview

**PRSedm (Polygenic Risk Score Extension for Diabetes Mellitus)** is a flexible and extendable open-source package for efficient local and remote (All of Us, UK Biobank, etc.) generation of published Polygenic Risk Scores (PRS) for Diabetes Mellitus (DM) and related cardiometabolic phenotypes.  

PRS for Type 1 diabetes (T1D) and Type 2 diabetes (T2D), and more recent partitioned Polygenic Scores (pPS), have numerous applications as research and clinical tools.  

PRSedm aims to introduce a new parallelized "one-liner" method to generate standardized PRS and pPS for DM robust to variables such as genotyping method, quality control, and imputation panel.  

## Installation

### Dependencies

PRSedm requires the following packages:

- Python (>=3.9)
- Joblib (>=1.3.2)
- Pandas (>=2.2.3)
- Pysam (>=0.22.0)
- Numpy\* (2.x/1.x)

\*Build with 1.x when deploying to RAP platforms with 1.x dependencies.

### User Installation

PRSedm is available through a number of channels: \
PIP: ```not yet available``` \
Anaconda: ```not yet available``` \
Build from source: ```not yet available```

## Usage

### Command Line Interface

To call PRSedm from the command line:

```bash
prsedm --bcf <path_to_bcf_file> [options]
```

- `--vcf` *(required)*: Path to an indexed VCF (.gz/.bgz) or BCF file, or a text file mapping one file per contig.
- `--col`: Genotype column to score (default: `GT`, options: `GT` for WGS, `GP` for imputed data).
- `--build`: Genome build to use (default: `hg38`, options: `hg19`, `hg38`).
- `--prsflags` *(required)*: Comma-separated list of PRS to generate, e.g., `PRS1,PRS2`.
- `--impute` *(optional)*: Enable imputation (requires `--refvcf`) (default: `1`).
- `--refvcf` *(optional)*: Reference directory (required if imputation is enabled).
- `--norm` *(optional)*: Perform fixed MinMax normalization (default: `1`).
- `--parallel` *(optional)*: Enable parallel processing (default: `1`).
- `--ntasks` *(optional)*: Number of tasks to use for parallel processing (default: CPU count).
- `--batch-size` *(optional)*: Number of variants per batch (default: `1`).
- `--output`: Path to save the output file (default: `results.csv`).

### Python (recommended)

To call PRSedm from python:

```python
import PRSedm
df = prsedm.gen_dm(vcf, col, build, prsflags, impute, refvcf, norm, parallel, ntasks, batch_size)
```

### Single file per-chromosome loading

For --vcf and --refvcf you can point to a text a single file mapping per contiguous region formatted as such:

```text
file1.chr1.vcf.gz   chr1
file2.chr2.vcf.gz   chr2
...
```

## Research Analysis Platforms (RAP's)

Remote deployment to remote Research Analysis Platforms (RAP's) is possible via notebook wrappers:
- All of Us - [Notebook Here](https://github.com/sethsh7/PRSedm/blob/main/notebooks/PRSedm-AllofUS-notebook.ipynb)
- UK Biobank - Notebook not yet available

## Available PRS

PRS schematics are stored in a SQLlite database (variants.db) and accessed via a JSON metadata (prs_meta.json). These are automatically read and fully extendable if the user wishes to add additional PRS. The following PRS are available by default:  

## Additional Features

### HLA Interaction PRS (+GRS2x Update)

PRSedm features a complete algorithm for GRS which incorporate HLA interaction terms as previously published by us such as T1D-GRS2 (or just GRS2). A number of advancements have been added to improve the generation of HLA interaction, described as GRS2x.

#### HLA Type Estimation and LD Tiebreak

HLA alleles can be estimated by proxy (or tag) single nucleotide polymorphisms alone and predictions are output e.g. (DR3-DQ2.5/DR3-DQ2.5) Due to imperfect proxy SNPs >2 HLA calls can be made in interaction scores such as GRS2, a probablistic tiebreaker algorithm using a HLA reference frequencies (Klitz et al) now resolves impossible numbers of calls without excluding any samples.

### Missing variant mean effect imputation (optional)

PRSedm optionally uses Hardy-Weinberg Equilibrium with a reference VCF/BCF legend (ensure you have variant frequency coded as 'AF', genotypes not required) to impute the mean effect size for missing SNPs, handle missing variants, and enable static normalization.
- dbsnp hg38 - [TOPMED Bravo Freeze 8](https://legacy.bravo.sph.umich.edu/freeze8/hg38/downloads), or [NCBI](https://ftp.ncbi.nih.gov/snp/latest_release/VCF/) ('AF' field added) are recommended.
- dbsnp hg19 - [1000 Genomes](https://mathgen.stats.ox.ac.uk/impute/1000GP_Phase3.html), [Haplotype Reference Consortium](https://www.sanger.ac.uk/collaboration/haplotype-reference-consortium/), [NCBI GRCh37](https://ftp.ncbi.nih.gov/snp/pre_build152/organisms/human_9606_b151_GRCh37p13/VCF/) recommended.

### Minimum and Maximum Normalization (optional)

PRSedm hardcodes static normalization of minimum and maximum potential risk contribution (no risk alleles vs all risk alleles) creating a scale of 0-1. Static normalization with imputation ensures that PRS values translate to a common relative risk scale across datasets. Imputation must be enabled, or all variants must be present.

## Development

Developed and maintained by Seth A. Sharp ([ssharp@stanford.edu](mailto:ssharp@stanford.edu)) at the [Translational Genomics of Diabetes](https://med.stanford.edu/genomics-of-diabetes.html) lab (Dr. Anna Gloyn), Stanford University, with collaboration from colleagues at the [University of Exeter](https://www.diabetesgenes.org) (Amber Luckett, Dr. Michael Weedon, Dr. Richard Oram), and [MGH/Broad Institute](https://www.udlerlab.org) (Dr. Aaron Deutsch, Dr. Miriam Udler).

## License

This project is licensed under the **MIT License (Non-Commercial)**.  
- Academic, research, and personal use are allowed.  
- Commercial use is prohibited without prior permission.  

See the [LICENSE](./LICENSE) file for full details.

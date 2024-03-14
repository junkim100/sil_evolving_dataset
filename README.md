# Self-Improving-Leaderboard (SIL): A Call for Real-World Centric Natural Language Processing Leaderboards
The Self-Improving Leaderboard (SIL) represents a pioneering step in the realm of Natural Language Processing (NLP) leaderboards, focusing on real-world applicability and continuous model improvement. This repository is dedicated to the Evolving Dataset component of SIL, which ensures that the leaderboard is powered by data that reflects the current and dynamic nature of language.

## Requirements
This project is tested and developed with Python 3.10. It is not compatible with Python 2.

Please ensure you are using Python 3.10 to avoid any compatibility issues.

## Installation Instructions

### Step 1: Clone the Repository

Clone the SIL evolving dataset repository to your local machine:

```bash
git clone https://github.com/yourusername/sil_evolving_dataset.git
cd sil_evolving_dataset
```
Replace https://github.com/yourusername/sil_evolving_dataset.git with the actual URL of your repository.

### Step 2: Create and Activate a Conda Environment

Create a new Conda environment and activate it:

```bash
conda create --name sil_env python=3.10
conda activate sil_env
```

### Step 3: Install Dependencies

Since the newscatcher package has specific version requirements for its dependencies, install it first:

```bash
pip install -r requirements.txt
```

Then, upgrade feedparser to the required version:

```bash
pip install --upgrade feedparser==6.0.11
```

This sequence ensures that all dependencies are correctly resolved and installed.

## Usage
Once you have everything installed, you can start generating the evolving dataset using the provided scripts:

```bash
python generate.py
```

Running generate.py initiates the dataset generation process, pulling in fresh data from various sources and processing it to form the dataset that will be used in the SIL evaluations.

## Contributing
We welcome contributions to the SIL Evolving Dataset project. Whether you have suggestions for improving the dataset, code enhancements, or new features, please feel free to fork the repository, make your changes, and submit a pull request.

Thank you for supporting the SIL project and helping advance the field of natural language processing!

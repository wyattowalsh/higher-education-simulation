# Conceptualizing Higher Education Institutions: <br> An Agent-Based Modelling Approach

--- 

Link to cloud hosted simulation experiment data analysis and modelling notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/wyattowalsh/higher-education-simulation/HEAD?filepath=nb.ipynb)

Link to project paper: [Conceptualizing Higher Education Institutions Paper](https://github.com/wyattowalsh/higher-education-simulation/blob/master/Conceptualizing_Higher_Education_Institutions__An_Agent_Based_Modelling_Approach.pdf)

Link to datasets: [Experiment 1](https://www.dropbox.com/s/gq8gqxqvrqlssf3/experiment_1.json?dl=0) and  [All Experiments](https://www.dropbox.com/s/gk31rdjnvzusql6/all_data.csv?dl=0)

---

## Explanation of Repository Contents
. <br>
├── README.md     &emsp;                  *This file* <br>
├── paper.pdf   &emsp;                    *Project Write-Up* <br>
├── environment.yml     &emsp;            *Conda environment configuration file (ssed to load project dependencies)* <br>
├── nb.ipynb                  &emsp;      *Jupyter Notebook used for data analysis and modelling (hosted at the above Binder link)* <br>
├── .gitignore            &emsp;          *Git file used to ignore non-repo local files*  <br>
└── **src**                  &emsp;       *Directory containing custom scripts*     <br>
&emsp;  &emsp;  ├── \_\_init\_\_.py <br>
 &emsp;  &emsp; ├── agent.py        &emsp;            *Agent class definition (agent instantiation and opinion variation)* <br>
 &emsp;  &emsp; ├── data_functions.py     &emsp;      *Helpful functions to manipulate data* <br>
 &emsp;  &emsp; ├── data_operations.py    &emsp;      *Main data file used to prouduce data (utilizes Apache Spark)* <br>
  &emsp; &emsp; ├── data_processing.py    &emsp;      *Short script to fix time data writing issue in simulation* <br>
  &emsp; &emsp; ├── environment.py       &emsp;       *Environment class definiton (establishes agents, holds data, increments time, conducts group negotiations)* <br>
 &emsp;  &emsp; ├── main.py        &emsp;             *Script to run collection of experiments* <br>
  &emsp; &emsp; ├── model.py      &emsp;              *Model class definition (sets enviroment, generates collection of experiment parameters, conducts experiments)* <br>
 &emsp;   &emsp; ├── utilities.py     &emsp;           *Helpful functions used throughout simulation* <br>
   &emsp; &emsp; └── visualization.md     &emsp;      *Mermaid markdown snippet dump for flowcharts* <br>
    
----
## Instructions for Usage

`environment.yml`  can be found in the repository's root directory and used to install necessary project dependencies. If able to successfully configure your computing environment, then launch Jupyter Notebook from your command prompt and navigate to `nb.ipynb`. If unable to successfully configure your computing environment refer to the sections below to install necessary system tools and package dependencies. The following sections may be cross-platform compatibile in several places, however is geared towards macOS<sup>[1](#footnote1)</sup>.

#### Do you have the Conda system installed?

Open a command prompt (i.e. *Terminal*) and run: `conda info`.

This should display related information pertaining to your system's installation of Conda. If this is the case, you should be able to skip to the section regarding virtual environment creation (updating to the latest version of Conda could prove helpful though: `conda update conda`).

If this resulted in an error, then install Conda with the following section. 

#### Install Conda

There are a few options here. To do a general full installation check out the [Anaconda Download Page](https://docs.conda.io/projects/conda/en/latest/user-guide/install/). However, the author strongly recommends the use of Miniconda since it retains necessary functionality while keeping resource use low; [Comparison with Anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html#anaconda-or-miniconda) and [Miniconda Download Page](https://docs.conda.io/en/latest/miniconda.html). 

Windows users: please refer to the above links to install some variation of Conda. Once installed, proceed to the instructions for creating and configuring virtual environments [found here](#Configure-Local-Environment

macOS or Linux users: It is recommended to use the [Homebrew system](https://brew.sh/) to simplify the Miniconda installation process. Usage of Homebrew is explanained next. 

##### Do you have Homebrew Installed?

In your command prompt (i.e. *Terminal*) use a statement such as: `brew help`

If this errored, move on to the next section.

If this returned output (e.g. examples of usage) then you have Homebrew installed and can proceed to install conda [found here](#Install-Miniconda-with-Homebrew).

##### Install Homebrew

In your command prompt, call: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

##### Install Miniconda with Homebrew

In your command prompt, call: `brew install --cask miniconda`

When in doubt, calling in the `brew doctor` might help :pill: 

##### A Few Possibly Useful Conda Commands

All environment related commands can be found here: [Anaconda Environment Commands](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

Here are a few of the most used ones though: 

List all environments (current environment as marked by the \*): `conda env list`

Create a new environment: `conda create --name myenv`

Activate an environment: `conda activate myenv`

Deactivate an environment and go back to system base: `conda deactivate`

List all installed packages for current environment: `conda list`

#### Configure Local Environment

Using the command prompt, navigate to the local project repository directory -- On macOS, I recommend typing `cd ` in Terminal and then dragging the project folder from finder into Terminal. 

In your command prompt, call: `conda env create -f environment.yml`. This will create a new Conda virtual environment with the name: `higher-education-simulation`.

Activate the new environment by using: `conda activate higher-education-simulation`

#### Access Project

After having activated your environment, use `jupyter notebook` to launch a Jupyter session in your browser. 

Within the Jupyter Home page, navigate and click on `nb.ipynb` in the list of files. This will launch a local kernel running the project notebook in a new tab. 

---
<br></br>
<br></br>
<br></br>
<br></br>
<br></br>
<br></br>
<br></br>

<a name="footnote1">1</a>: This project was created on macOS version 11.0.1 (Big Sur) using Conda version 4.9.2, and Python 3.8 (please reach out to me if you need further system specifications). 

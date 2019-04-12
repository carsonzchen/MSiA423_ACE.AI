# Development with Jupyter Notebooks 

## Environment setup for exploratory analysis

`environment.yml` contains the specifications for an environment that will get you started for exploratory data analysis. 
It also contains the packages imported in the template Jupyer notebook, `notebooks/template.ipynb` (see more info below).  

### Create conda environment 
Create conda environment with packages in `environment.yml`: 

`conda env create -f environment.yml`

and activate:

`source activate eda3`

### Complete Jupyter extensions install
After creating and activating your conda environment, run from the commandline:

`jupyter contrib nbextension install --user`

Next, start a Jupyter notebook server by running: 

`jupyter notebook`

You can then go to the extension configurator at [http://localhost:8888/nbextensions/](http://localhost:8888/nbextensions/) and enable your desired extensions. 

#### Collapsible headings extension
I recommend enabling the `Collapsible Headings` extension so that the `Imports and setup` section on the template notebook (see section below), which is quite long, can be minimized, as well as other heading sections when desired. To maintain this collapsibility when exporting to html, run:

`jupyter nbconvert --to html_ch FILE.ipynb`

#### Table of Contents (2)
Enabling the `Table of Contents (2)` extension automatically creates a table of contents based on your notebook headings, which can be placed at the top of the notebook or at the side (which is nice for navigation in a long notebook).

To keep this table of contents when you export to html, add to the command in the prior section and run: 

`jupyter nbconvert --to html_ch FILE.ipynb --template toc2`

#### Other recommended extensions
* `Code prettify`: when enabled, you can press the little hammer icon at the top of the page and it will make "pretty" ([PEP8](https://www.python.org/dev/peps/pep-0008/) compliant) the code in the current cell. This is really nice when you're writing a long command. 
* `Execute time`: when enabled, this adds to the bottom of a code cell the time at which the cell was executed and how long it took. This is nice for traceability purposes and making sure code was run in order when looking at old code. It also helps when code takes a while to run and you leave it and come back and want to know how long it took. 
* `Ruler`: when enabled, this adds a vertical line to code cells to denote the distance of 76 characters, which is the maximum line length suggested by ([PEP8](https://www.python.org/dev/peps/pep-0008/)).

There are a lot more options so take a look through! 

## Template Jupyter Notebook 
`template.ipynb` is a template Jupyter notebook that includes:
 * A set of regularly used package imports 
 * Code that helps reference other parts of the directory structure (e.g. `dataplus()` prepends the data directory for data import)
 * Code that sets up a SQLAlchemy connection to MySQL 
 * Headings for stating notebook objectives, guiding questions, conclusions 
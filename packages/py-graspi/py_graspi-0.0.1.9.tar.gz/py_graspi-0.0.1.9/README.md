# py-graspi

Python-Igraph is a graph-based library contender for the library that works with the GraSPI package. 

This repository contains the implementation to test basic algorithm requirements that need to be met for this package to work similarly to GraSPI.
The basic algorithm requirements include:
  -  Construction of graphs
  -  Graph Filtering
  -  Determine the number of connected components
  -  Determine the shortest path from some meta-vertices to all specified vertices
  -  Provide a list of descriptors
  -  Graph visualization

## Installation
Download the packages found in requirements.txt after you have set up your virtual environment. 
Cone the repo by:
```
git clone https://github.com/owodolab/py-graspi.git
```
**Note: You'd need git installed on your system first**
<br />
<br />
  If you do not have git installed or run into issues with git, please visit: https://github.com/git-guides/install-git
<br />
<br />
Next, you'd need to navigate to the cloned repo using terminal. An example would be:
```
cd /path/py-graspi
```
Next, make sure you're on the correct branch by using:
```
git checkout Card#122-Histogram-Report
```
Once navigated to the branch, access the following directory:
```
cd py_graspi
```
Next, the downloads needed can be found in `requirements.txt` and can be installed by:
```
pip install -r requirements.txt
```
Install the graspi_igraph package by:
```
pip install py-graspi
```
Once installed, to utilize the package remember to import the package:
```
import py_graspi as ig
```

**Note: you must have Python and pip installed onto your system**
<br />
<br />
  If you do not have Python installed, please visit: https://www.python.org/downloads/
<br />
<br />
  If you do not have pip installed or are running into issues with pip, please visit: https://pip.pypa.io/en/stable/installation/
<br />
<br />
  If there are any other issues with installation, please visit: https://python.igraph.org/en/stable/ 

## Running All 33 Morphologies Tests
To run the morphologies tests, return to the previous directory of `/py-graspi` by running:
```
cd ..
```
Next, make sure you're running using bash:
```
bash
```
Next, run the following:
```
chmod +x run.sh
```
Finally, run the following: 
```
./run.sh <file_type>
```
Substitute `<file_type>` with either `txt` or `pdf` for the desired output type.
<br />
<br />
**Note: run txt before pdf to update text files and for an accurate output**
## 33 Morphologies Output
After running the command, the automatic report generation will begin. 
<br />
<br /> 
The following will print when the report generation begins:
```
Generating PDF (If on pdf mode)
Generating Text Files
```
As the script is running, the following will print for which microstructure it is on
```
Executing <test_file>
```
After a few minutes, the following will print once the report has been created
```
Text Files Generated
PDF Generated (If on pdf mode)
```
## Viewing 33 Morphologies Output
For text files, navigate to the results directory by using the following command:
```
cd graspi_igraph/results
```
Use the following command to view the list of text files generated:
```
ls
```
To view the result in each file, run the following command:
```
cat <result_file_name>
```
Replace `<result_file_name>` with any of the files outputted by `ls`
<br />
<br />
If using pdf mode, the pdf should automattically open upon completion.
<br />
<br />
If the pdf does not automatically pop up, use the following commands:
### On Windows
```
start graspi_igraph/test_results.pdf
```
### On MacOS
```
open graspi_igraph/test_results.pdf
```
### On Linux
```
evince graspi_igraph/test_results.pdf
```
If evince is not installed, run this first:
```
sudo apt install evince
```
## To Test Algorithms

To **generate graphs**, call the generateGraph(_file_) function which takes in a input-file name
returns:
  - g: graph object
  - s_2D: bool of whether the graph is 2D
  - black_vertices: list of all black vertices
  - white_vertices: list of all white vertices
  - black_green: number of edges from black to interface (green vertex)
  - black_interface_red: number of black interface vertices that has a path to top (red)
  - white_interface_blue: number of white interface vertices that has a path to bottom (blue)
  - dim: value of vertices in y direction for 2D and z direction for 3D
  - interface_edge_comp_paths: number of interface edges with complementary paths to top (red) and bottom (blue)
  - shortest_path_to_red: shortest paths from all vertices to red 
  - shortest_path_to_blue: shortest paths from all vertices to blue
  - CT_n_D_adj_An: number of black vertices in direct contact with top (red)
  - CT_n_A_adj_Ca: number of white vertices in direct contact with bottom (blue)

```
ig.generateGraph("2D-testFile/testFile-10-2D.txt")   # utilizing the test file found in 2D-testFiles folder as an example
```

To **filter graphs**, call filterGraph(_graph_) function which takes in a graph object 
  -  can pass a graph generated by generateGraph(_file_)
  -  returns a filtered graph
```
g = ig.generateGraph("2D-testFile/testFile-10-2D.txt")[0]     # utilizing the test file found in 2D-testFiles folder as an example
fg = ig.filterGraph(g)
```

### To get dictionary of descriptors

To test if descriptors are computed correctly, you can run the following script in the terminal to check.
  -  make sure you are in the py_graspi directory after git cloning
  -  if not in directory py-graspi/py_graspi, in the terminal, run the command
     ```
     cd py_graspi
     ```

```
python simple-test.py data/data_0.5_2.2_001900.txt
```
This will print out whether the descriptor computation is correct and should take around 10-15 seconds.

The **descriptors stored in a dictionary** can be computed by calling the function descriptors(...)
It take in values returned from generateGraph() and a input filename as the parameters:
  - graph: graph object
  - filename: input filename used to generate graph
  - black_vertices: list of all black vertices
  - white_vertices: list of all white vertices
  - black_green: number of edges from black to interface (green vertex)
  - black_interface_red: number of black interface vertices that has a path to top (red)
  - white_interface_blue: number of white interface vertices that has a path to bottom (blue)
  - dim: value of vertices in y direction for 2D and z direction for 3D
  - interface_edge_comp_paths: number of interface edges with complementary paths to top (red) and bottom (blue)
  - shortest_path_to_red: shortest paths from all vertices to red 
  - shortest_path_to_blue: shortest paths from all vertices to blue
  - CT_n_D_adj_An: number of black vertices in direct contact with top (red)
  - CT_n_A_adj_Ca: number of white vertices in direct contact with bottom (blue)

```

ig.descriptors(graph,filename,black_vertices,white_vertices, black_green, black_interface_red, white_interface_blue, dim,interface_edge_comp_paths, shortest_path_to_red, shortest_path_to_blue, CT_n_D_adj_An, CT_n_A_adj_Ca) 
```
The ** descriptors in a text file** can be computed by calling the function descriptorsToTxt(_dictionary_,_filename_)
  -  _dict_ is a dictionary of descriptors that is returned by calling ig.descriptors(...)
```
ig.descriptorsToTxt(dict,"descriptors_list.txt") 
```


### To visualize graphs

To visualize graphs, call visualize(_graph_, _is_2D_)
  -  _graph_ is a graph object
  -  _is_2D_ is a bool of whether a graph is 2D, also a return value when _generateGraph()_ is called
```
g, is_2D = ig.generateGraph("2D-testFile/testFile-10-2D.txt")[0:1]     # utilizing the test file found in 2D-testFiles folder as an example
ig.visual2D(g, is_2D)
```

## Testing from Command Line


Now that we have cloned the REPO lets talk about testing.

\*\*\*First and foremost make sure you are in the py-graspi directory. If not you may run into some errors\*\*\*

In this GitHub Repo, you can find test files in the data directory or the 2D-testFile and 3D-testFile directories.
Inside these directories, some files hold information about either 2d or 3d graphs based on the directory name. 
When running from command lines you will need to know the complete pathname of the test file you are trying to run.

There are 2 type of input file formats: *.txt & *.graphe
### _*.txt input format:_


The command line input to run a graph creation for *.txt files will have the following format:
```
python graspi_igraph/igraph_testing.py {total pathname of test file}
```
If you have the same test directories as this GitHub Repo you should be able to run the following command line argument to output a 2D 10x10 graph.
```
python graspi_igraph/igraph_testing.py graspi_igraph/2D-testFile/testFile-10-2D.txt 
```
### _*.graphe input format:_
*.graphe input format is not that different, only extra parameter you need to input is a '-g' before the total pathname of the test file.

The command line input to run a graph creation for *.graphe files will have the following format:
````
python graspi_igraph/igraph_testing.py -g {total pathname of test file} 
````
If you have the same test directories as this GitHub Repo you should be able to run the following command line argument to output a 2D 4x3 graph.
```
python graspi_igraph/igraph_testing.py -g graspi_igraph/data_4_3.graphe
```
### _Running with Periodicity:_
We include the option of running any test case with periodicity turned on (only for .txt files). This 
is done with an added '-p' parameter. This parameter is added first before inputting the test case
format.

For example, for *.txt cases with periodicity turned on will look like the following:
```
python graspi_igraph/igraph_testing.py -p {total pathname of test file}
```
To test this out run the example test case above but with the added '-p' parameter
to turn periodicity on.
## Output of Command Line Input
As long as the inputs follow the format above and a file exists the program shall do the following:
1. Pop up window should appear, this will be the initial visualization of the graph along with red, blue, and green meta vertices.
2. Exit out of this pop up window with the top right "X" button.
3. Now a second pop up window should appear, this window will now show a visualization of the filtered version of the graph in step 1.
4. Exit out this window following same steps as step 2.
5. Make sure program exits correctly (code 0).

DISCLAIMER: if any issues occur you may not be in the right directory (py-graspi) or the test file may not exists or be poorly formatted.

## Generate and Run Files for py-graspi API
In order to generate an API using sphinx, you need to follow the installation of py-graspi:

Cloning the repository:
```
git clone https://github.com/owodolab/py-graspi.git
```

**Make sure your current directory is py-graspi**

In order to create an API with sphinx, you need to download sphinx with this command in the command line interface:
```
pip install sphinx
```
Additional dependencies needed for installed Sphinx Extension:
```
pip install sphinxcontrib-details-directive
```
Provides additional details (dropdowns) for each submodle listed.
```
pip install sphinx_rtd_theme
```
Uses the rtf theme for the API
```
pip install --upgrade setuptools
```
Used by python to handle resources and files

In the command line interface, run this command:
```
sphinx-build -b html ./docs/source/ ./docs/ 
```
* **sphinx-build**: This is the main command for building Sphinx documentation. It generates documentation from reStructuredText (.rst) or Markdown (.md) source files.
* **-b html**: This specifies the output format. Here, -b html tells Sphinx to build the documentation in HTML format, which is typically used for web-based documentation.
* **./docs/source/**: This is the path to the source directory where Sphinx looks for the documentation source files. In this example, it’s in the source subdirectory inside docs.
* **./docs/**: This is the output directory where the built HTML files will be saved. In this example, it’s the main docs folder. After running this command, you’ll find the generated HTML files here.

In order to see the py-graspi API, run this command in the command line interface:

**FOR WINDOWS:**
```
start docs/index.html
```

**FOR MACOS:**
```
open docs/index.html
```
This would create a local view. You can see the official API on Github pages at: https://owodolab.github.io/py-graspi/

## 2D & 3D Morphologies Tests
To run the 2d and 3d morphologies you will need to setup notebook and pip install the graspi_igraph package.

First you will need to git clone the current repo, make sure that you are in the ""dev branch"":
```
git clone https://github.com/owodolab/py-graspi.git
```
Then, you will need to install the igraph package:
```
pip install graspi-igraph
```
Install jupyter notebook in order to view the test file:
```
pip install notebook
```

Finally, you will be able to use the command:
```
jupyter notebook
```
This will bring you into the testing filing on jupyter.
Navigate to the directory 3d_2d_tests.
Navigate to the file graspi_igraph_notebook.ipynb.

On this file you will be able to run and view the 2d and 3d morphologies for subtask 4, card 104.

## View Demo Videos for Py-Graspi Installation, Notebook Setup, and Testing via Command Line
Please visit this link: https://drive.google.com/drive/folders/1AECLQXII4kmcBiQuN86RUYXvJG_F9MMq?usp=sharing
### Videos
* **py_graspi_installation**: How to install Py-Graspi and run basic commands.
* **py_graspi_notebook**: How to utilize our prebuilt notebook to run basic commands of Py-Graspi.
* **py_graspi_command_line**: How to print out Py-Graspi's calculations of connected components, descriptors, visualizations of graph, etc of provided input files via command line.

## Translate Image File Into Truncated .txt File
1. make sure you have py-graspi installed: pip install py-graspi
2. Make sure you cd into py_graspi directory first. 
3. The command line format to translate an image file into its truncated .txt file is as follows:
```
python img_to_txt.py {pathname of image file} {Resize calculation amount}
```
4. The "resize calculation amount" is multiplied to the X and Y axis of the original image and this will alter the size of the image's final resized .txt file. 
5. This should place both a truncated image file and truncated .txt file of the original image file into the "resized" directory. 
6. They will be named "resized_" followed by the image file name and correct extension. 
7. An example command line input that should work for this repo is as follows:
```
python img_to_txt.py images/data_0.5_2.2_001900.png 0.25
```

## Mycelium Filtered Vertices Visualization
This section explains how to visualize a mycelium image by both it's white and black vertices filtered versions.
The mycelium image used is included in the "images" directory called "mycelium.png".

The following are steps on how to visualize the graph from this image.
1. Make sure you have py-graspi installed: pip install py-graspi
2. Make sure you cd into py_graspi directory first.
3. The command line format input is as follows
```
python myceliumTest.py {pathname of image file} {Resize calculation amount}
```
4. The input is the same as the translation input from image files to .txt files, it will create a new .img and .txt file for it in the "resized" directory.
5. The image input pathname must be in the "images" directory.
6. If you wish to not resize the original image just input a '1' for the Resize calculation amount, this will keep the original size.
7. Example command line input is as follows:
```
python myceliumTest.py images/mycelium.png 0.25
```
8. This creates a turncated version of the mycelium image (for runtime purposes) and outputs two graphs, first one is a white only vertex graph and the second one is a black only vertex version.

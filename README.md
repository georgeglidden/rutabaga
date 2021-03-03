## rutabaga
Rutabaga is a collection of scripts, tools, and applications created while investigating q polynomials and other objects related to two-bridge links.

So far, our main focus has been on generating and displaying the roots (input `x` values for which a function `f(x) = 0`) to q polynomials. The roots are complex numbers, so each value is a two-dimensional point. 
The `/tileserver` folder contains a server+client web application for viewing the distribution of those root points and, more generally, any set of two-dimensional coordinate data, at arbitrary resolutions and zoom levels. 

If you want more direct access to the data, the Jupyter notebooks in the top-level directory provide tools for generating and analyzing several objects of interest.

### How to Use Rutabaga
- run generate_Qs.py to make csv of the Q polynomials
- run rootfinder.py to make a csv of the roots for each polynomial
- run the server to visualize the pattern of the roots:
  1. Update the repository to the latest version with git pull
  2. On a command line, cd into the tileserver directory (or open up the directory in PyCharm)
  3. Run python dynserve.py. (Or run the "dynserv.py" file from within PyCharm)
  4. Open the file called "demoClient.html" with a web-browser (it's also in the tileserver directory of the repository; just click on it, and the webpage should come up.)
  It really looks marvelous.


### Attributions and Further Reading:
This project is part of ongoing work by students in Dr. Eric Chesebro's Undergraduate Research Group at the University of Montana.
- http://www.umt.edu/people/chesebro
- https://arxiv.org/abs/1902.01968
- https://arxiv.org/abs/2008.13303

Our aesthetic and programmatic inspiration came from the  beautiful images generated and shared by John Baez, Dan Christensen, and Sam Derbyshire.
- https://www.scientificamerican.com/article/math-polynomial-roots/
- http://jdc.math.uwo.ca/roots/
- https://math.ucr.edu/home/baez/roots/

A similar project, rootviz, was created by nessig.github.io
- https://github.com/nessig/rootviz

This project makes use of the following libraries:
- https://mpmath.org/
- https://tqdm.github.io/
- https://jupyter.org/index.html
- https://scikit-image.org/
- https://pandas.pydata.org/
- https://www.scipy.org/
- https://www.sagemath.org/

### To-Do:
* documentation, documentation, documentation
* develop client UX!
- integrate multiple tile sources
- adjustable color maps
- contour detection
- blob detection
* serve multi-channel images 
* serve queries for tile and pyramid metadata
* try webASM implementations of the root-finder

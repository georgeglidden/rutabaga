## rutabaga
_rutabaga_ is a web-based tool for visualizing solutions to polynomials with integer coefficients.

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
* develop client UX!
- integrate multiple tile sources
- adjustable color maps
- contour detection
- blob detection
* serve multi-channel images 
* serve queries for tile and pyramid metadata
* try webASM implementations of the root-finder

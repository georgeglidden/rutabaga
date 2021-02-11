## rutabaga
_rutabaga_ is a web-based tool for visualizing the roots of polynomials with integer coefficients.

### Resources and Reference Material:
- https://planetmath.org/sturmstheorem
- https://jupyter.org/index.html

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
- https://openseadragon.github.io/
- https://mpmath.org/
- https://tqdm.github.io/
- https://scikit-image.org/
- https://pandas.pydata.org/
- https://www.scipy.org/
- https://www.sagemath.org/

### To-Do:
- fix quartering algorithm
- support >4 layers resolution
- dynamic color maps by resolution + sample density
- find all real & complex roots to a  q-polynomial constrained over a rectangular interval
- try webASM implementations of the root-finder

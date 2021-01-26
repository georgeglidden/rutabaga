## rutabaga
_rutabaga_ is a web-based tool for visualizing the roots of polynomials with integer coefficients.

### Resources and Reference Material:
- https://planetmath.org/sturmstheorem

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

### To-Do:
- generate a density map from a set of points
- consistent or at least comprehensible color encoding(s) for density maps at arbitrary intervals
- render the density map + encoding in a browser
- find all real & complex roots to a  q-polynomial constrained over an or
- ... quickly enough to dynamically serve them to an arbitrary number of clients
- ... efficiently enough to run on the browser
- try webASM implementations of the root-finder

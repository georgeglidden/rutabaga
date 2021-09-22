server <- function(input, output) {
  install.packages("reticulate")
  library(reticulate)
  
  # load csv of Q polynomials
  py_run_file("generate_Qs.py")
  
  # load csv of the roots for each polynomial
  py_run_file("rootfinder.py")
  
  # run tileserver
  py_run_file("dynserv.py")
  
  
  
}
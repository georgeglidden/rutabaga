install.packages("shiny")
library("shiny")

source("ui.R")
source("server.R")

# Create Shiny app ----
shinyApp(ui = ui, server = server)
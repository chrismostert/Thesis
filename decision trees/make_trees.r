library(party)
library(stringr)

filelist = list.files(pattern="*.csv")

for (file in filelist) {
  # Load data
  data <- read.csv(file)
  
  # Make tree
  tree <- ctree(label ~ ., data=data, control=ctree_control(maxdepth=5))
  
  # Write tree plot to disk
  png(filename=str_replace(file, '.csv', '.png'), width=6000, height=6000)
  plot(tree)
  dev.off()
  
  # Write textual representation to file
  sink(file=str_replace(file, '.csv', '.txt'))
  print(tree)
  sink()
}



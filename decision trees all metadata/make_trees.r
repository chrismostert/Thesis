library(party)

datafile <- 'relaxed_anomalies'

# First load in the abbreviated data to create a visual plot
data <- read.csv(paste(datafile, ".csv", sep=""))

# Full tree with no height restriction
tree <- ctree(label ~ ., data=data)
png(filename=paste(datafile, "_full.png", sep=""), width=16000, height=8000)
plot(tree)
dev.off()

# Tree limited in size which gives an easier overview
tree <- ctree(label ~ ., data=data, control=ctree_control(maxdepth=5))
png(filename=paste(datafile, "_limited.png", sep=""), width=6000, height=6000)
plot(tree)
dev.off()

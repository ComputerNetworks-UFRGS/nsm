data <- read.table("time_analisys-100-3-9-18.txt", sep=';')
names(data) <- c("Entropy","Direct Comparison")

# Get the mean values of both groups
medias <- c(mean(data[,1]),mean(data[,2]))

# Set desired font family
op <- par(family = "Helvetica")

# Create the plot (without axes, we will add those later)
# Range of y-axis is set to interval (0, 60) to give space 
# to the error bars
# Midpoints of the bars will be saved in variable mp
mp <- barplot(medias, width=1, axes=FALSE, axisnames=FALSE, ylim=c(0,0.5),
              col=c("cornflowerblue"),
              #main="Average Boot Time",
              xlab="Detection approach", ylab="Time [ms]")

# Set grid
grid(NA, ny=NULL, 5, lty=2, lwd=1, col="black")
par(new=TRUE)

# Plot bars again to overcome y lines
mp <- barplot(medias, width=1, axes=FALSE, axisnames=FALSE, ylim=c(0,0.5),
              col=c("cornflowerblue", "lightblue"),
              #main="Average Boot Time",
              xlab="Detection approach", ylab="Time [ms]")

# The x-axis with labels for each group
# The labels are drawn at the bar midpoints
#axis(1, labels=c("Time", at = mp))
# The y-axis with the age going from 0 to 60 
axis(2, at=seq(0 , 0.5, by=0.05))
# Put the plot in a box
box()

##### Add the error bars #####
# Get standard deviation of each group
# The standard deviations are saved in a matrix of same size 
# as the matrix with midpoints, this is useful for plotting 
# the error bars
stDevs <- matrix(c(sd(data[,1]), sd(data[,2])), ncol=2)
# Plot the vertical lines of the error bars
# The vertical bars are plotted at the midpoints
segments(mp, medias - stDevs, mp, medias + stDevs, lwd=3)
# Now plot the horizontal bounds for the error bars
# 1. The lower bar
segments(mp - 0.05, medias - stDevs, mp + 0.05, medias - stDevs, lwd=3)
# 2. The upper bar
segments(mp - 0.05, medias + stDevs, mp + 0.05, medias + stDevs, lwd=3)

# Reset font style:
par(op)

Myerrors <- c(stDevs[1]/sqrt(100), stDevs[2]/sqrt(100))

dados <- data.frame(medias, as.data.frame(Myerrors))

write.table(dados, sep=";", file= "boot_gnuplot.csv", row.names=FALSE, col.names=FALSE)

dados
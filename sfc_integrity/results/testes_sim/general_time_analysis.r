data0 <- read.table("time_test_100-1-3-6.dat", sep=';')
data1 <- read.table("time_test_100-3-6-18.dat", sep=';')
data2 <- read.table("time_test_100-6-18-36.dat", sep=';')
data3 <- read.table("time_test_100-12-36-72.dat", sep=';')
data4 <- read.table("time_test_100-24-72-144.dat", sep=';')
data5 <- read.table("time_test_100-48-144-288.dat", sep=';')
data6 <- read.table("time_test_100-96-288-576.dat", sep=';')
data7 <- read.table("time_test_100-192-576-1152.dat", sep=';')
data8 <- read.table("time_test_100-384-1152-2304.dat", sep=';')

names(data0) <- c("Entropy","Direct Comparison")
names(data1) <- c("Entropy","Direct Comparison")
names(data2) <- c("Entropy","Direct Comparison")
names(data3) <- c("Entropy","Direct Comparison")
names(data4) <- c("Entropy","Direct Comparison")
names(data5) <- c("Entropy","Direct Comparison")
names(data6) <- c("Entropy","Direct Comparison")
names(data7) <- c("Entropy","Direct Comparison")
names(data8) <- c("Entropy","Direct Comparison")

# Get the mean values of both groups
medias0 <- c(mean(data0[,1]),mean(data0[,2]))
medias1 <- c(mean(data1[,1]),mean(data1[,2]))
medias2 <- c(mean(data2[,1]),mean(data2[,2]))
medias3 <- c(mean(data3[,1]),mean(data3[,2]))
medias4 <- c(mean(data4[,1]),mean(data4[,2]))
medias5 <- c(mean(data5[,1]),mean(data5[,2]))
medias6 <- c(mean(data6[,1]),mean(data6[,2]))
medias7 <- c(mean(data7[,1]),mean(data7[,2]))
medias8 <- c(mean(data8[,1]),mean(data8[,2]))

##### Add the error bars #####
# Get standard deviation of each group
# The standard deviations are saved in a matrix of same size 
# as the matrix with midpoints, this is useful for plotting 
# the error bars
stDevs0 <- matrix(c(sd(data0[,1]), sd(data0[,2])), ncol=2)
stDevs1 <- matrix(c(sd(data1[,1]), sd(data1[,2])), ncol=2)
stDevs2 <- matrix(c(sd(data2[,1]), sd(data2[,2])), ncol=2)
stDevs3 <- matrix(c(sd(data3[,1]), sd(data3[,2])), ncol=2)
stDevs4 <- matrix(c(sd(data4[,1]), sd(data4[,2])), ncol=2)
stDevs5 <- matrix(c(sd(data5[,1]), sd(data5[,2])), ncol=2)
stDevs6 <- matrix(c(sd(data6[,1]), sd(data6[,2])), ncol=2)
stDevs7 <- matrix(c(sd(data7[,1]), sd(data7[,2])), ncol=2)
stDevs8 <- matrix(c(sd(data8[,1]), sd(data8[,2])), ncol=2)

Myerrors0 <- c(stDevs0[1]/sqrt(100), stDevs0[2]/sqrt(100))
Myerrors1 <- c(stDevs1[1]/sqrt(100), stDevs1[2]/sqrt(100))
Myerrors2 <- c(stDevs2[1]/sqrt(100), stDevs2[2]/sqrt(100))
Myerrors3 <- c(stDevs3[1]/sqrt(100), stDevs3[2]/sqrt(100))
Myerrors4 <- c(stDevs4[1]/sqrt(100), stDevs4[2]/sqrt(100))
Myerrors5 <- c(stDevs5[1]/sqrt(100), stDevs5[2]/sqrt(100))
Myerrors6 <- c(stDevs6[1]/sqrt(100), stDevs6[2]/sqrt(100))
Myerrors7 <- c(stDevs7[1]/sqrt(100), stDevs7[2]/sqrt(100))
Myerrors8 <- c(stDevs8[1]/sqrt(100), stDevs8[2]/sqrt(100))

dados0 <- data.frame(medias0, as.data.frame(Myerrors0))
dados1 <- data.frame(medias1, as.data.frame(Myerrors1))
dados2 <- data.frame(medias2, as.data.frame(Myerrors2))
dados3 <- data.frame(medias3, as.data.frame(Myerrors3))
dados4 <- data.frame(medias4, as.data.frame(Myerrors4))
dados5 <- data.frame(medias5, as.data.frame(Myerrors5))
dados6 <- data.frame(medias6, as.data.frame(Myerrors6))
dados7 <- data.frame(medias7, as.data.frame(Myerrors7))
dados8 <- data.frame(medias8, as.data.frame(Myerrors8))

# Entropy
#nrow= numeber of observations (experiments)
entropy_results <- matrix(NA, nrow=9, ncol=2)

entropy_results[1,] = c(medias0[1], Myerrors0[1])
entropy_results[2,] = c(medias1[1], Myerrors1[1])
entropy_results[3,] = c(medias2[1], Myerrors2[1])
entropy_results[4,] = c(medias3[1], Myerrors3[1])
entropy_results[5,] = c(medias4[1], Myerrors4[1])
entropy_results[6,] = c(medias5[1], Myerrors5[1])
entropy_results[7,] = c(medias6[1], Myerrors6[1])
entropy_results[8,] = c(medias7[1], Myerrors7[1])
entropy_results[9,] = c(medias8[1], Myerrors8[1])

# Direct Comparison
#nrow= numeber of observations (experiments)
comparison_results = matrix(NA, nrow=9, ncol=2)

comparison_results[1,] = c(medias0[2], Myerrors0[2])
comparison_results[2,] = c(medias1[2], Myerrors1[2])
comparison_results[3,] = c(medias2[2], Myerrors2[2])
comparison_results[4,] = c(medias3[2], Myerrors3[2])
comparison_results[5,] = c(medias4[2], Myerrors4[2])
comparison_results[6,] = c(medias5[2], Myerrors5[2])
comparison_results[7,] = c(medias6[2], Myerrors6[2])
comparison_results[8,] = c(medias7[2], Myerrors7[2])
comparison_results[9,] = c(medias8[2], Myerrors8[2])

write.table(entropy_results, sep=";", file= "entropy_mean_std.csv", row.names=FALSE, col.names=FALSE)
write.table(comparison_results, sep=";", file= "comparison_mean_std.csv", row.names=FALSE, col.names=FALSE)

entropy_results
comparison_results
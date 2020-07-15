install.packages("devtools")
library("devtools")
install_github("galanisl/NetHypGeom")
library("NetHypGeom")

# Generate network dataset and visualize its structure
net <- ps_model(N = 500, avg.k = 10, gma = 2.3, Temp = 0.15)
plot_degree_distr(net$network)
compare_clustering_to_er(net$network, 100, "PS network")
plot_hyperbolic_net(network = net$network, nodes = net$polar, node.colour = net$polar$theta)

# To embed the network using HyperMap, we set LaBNE+HM's window to 2*pi
hm <- labne_hm(net = net$network, gma = 2.3, Temp = 0.15, k.speedup = 10, w = 2*pi)

# To embed with LaBNE+HM, we reduce HyperMap's search space from 2*pi 
# to a small window of 15 degrees around LaBNE's angles
lh <- labne_hm(net = net$network, gma = 2.3, Temp = 0.15, k.speedup = 10, w = pi/12)

# Comparison between real and HyperMap-inferred angles and real and LaBNE+HM-inferred angles
plot(net$polar$theta, hm$polar$theta, pch = 16, 
     xlab = "Real angles", ylab = "Inferred angles", main = "HyperMap")
plot(net$polar$theta, lh$polar$theta, pch = 16, 
     xlab = "Real angles", ylab = "Inferred angles", main = "LaBNE+HM")
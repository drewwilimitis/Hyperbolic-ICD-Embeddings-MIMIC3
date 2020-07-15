library("devtools")
devtools::install_github("galanisl/NetHypGeom")
library("NetHypGeom")
library("igraph")

# example with randomly generated graph network
net <- ps_model(N = 500, avg.k = 10, gma = 2.3, Temp = 0.15)
plot_degree_distr(net$network)
plot_hyperbolic_net(network = net$network, nodes = net$polar, node.colour = net$polar$theta)

# we want to load our ICD network as edges stored within a two-column dataframe
icd_df = read.csv('icd_full_relations.csv')

# to embed the network using HyperMap, we set LaBNE+HM's window to 2*pi
hm_coords <- labne_hm(net = icd_df, gma = 2.3, Temp = 0.15, k.speedup = 10, w = 2*pi)

# plot resulting network embedded in hyperbolic space
icd_net <- graph_from_data_frame(icd_df[, 1:2], directed = F)
plot_hyperbolic_net(network = icd_net, nodes = hm_coords$polar, node.colour = hm_coords$polar$theta)

# to embed with LaBNE+HM, we reduce HyperMap's search space from 2*pi 
# to a small window of 15 degrees around LaBNE's angles
lh_coords <- labne_hm(net = icd_df, gma = 2.3, Temp = 0.15, k.speedup = 10, w = pi/12)

# plot resulting network embedded in hyperbolic space
plot_hyperbolic_net(network = icd_net, nodes = lh_coords$polar, node.colour = lh_coords$polar$theta)

# write outputs of embedding methods to csv
write.csv(data.frame(hm_coords$polar), 'hypermap_embedding.csv')
write.csv(data.frame(lh_coords$polar), 'laplacian_embedding.csv')
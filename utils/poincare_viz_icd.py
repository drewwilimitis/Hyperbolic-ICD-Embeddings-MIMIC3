import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def dist_squared(x, y, axis=None):
    return np.sum((x - y)**2, axis=axis)

def plot_poincare_icd(emb, labels, edge_list, legend_headers=None, title=None, height=8, width=8,
                  add_labels=False, label_dict=None, plot_frac=1, edge_frac=1, label_frac=0.001):
    # Note: parameter 'emb' expects data frame with node ids and coords
    emb.columns = ['node', 'x', 'y']
    n_classes = len(np.unique(labels))
    plt.figure(figsize=(width, height))
    plt.xlim([-1.0, 1.0])
    plt.ylim([-1.0,1.0])
    ax = plt.gca()
    circ = plt.Circle((0, 0), radius=1, edgecolor='black', facecolor='None', linewidth=3, alpha=0.8)
    ax.add_patch(circ)
    
    # set colormap,
    if n_classes <= 12:
        colors = ['b', 'r', 'g', 'y', 'm', 'c', 'k', 'silver', 'lime', 'skyblue', 'maroon', 'darkorange']
    elif 12 < n_classes <= 20:
        colors = [i for i in plt.cm.get_cmap('tab20').colors]
    else:
        cmap = plt.cm.get_cmap(name='viridis')
        colors = cmap(np.linspace(0, 1, n_classes))

    # plot embedding coordinates
    emb_data = np.array(emb.iloc[:, 1:3])
    for i in range(n_classes):
        plt.scatter(emb_data[(labels == i), 0], emb_data[(labels == i), 1],
                             color = colors[i], alpha=0.8, edgecolors='black', linewidth=1, s=35)
    # plot edges,
    for i in range(int(len(edge_list) * edge_frac)):
        x1 = emb.loc[(emb.iloc[:, 0] == edge_list[i][0]), ['x', 'y']].values[0]
        x2 = emb.loc[(emb.node == edge_list[i][1]), ['x', 'y']].values[0]
        _ = plt.plot([x1[0], x2[0]], [x1[1], x2[1]], '--', c='black', linewidth=1, alpha=0.35)
    
    # add labels to embeddings,
    if add_labels and label_dict != None:
        plt.grid('off')
        plt.axis('off')
        embed_vals = np.array(list(label_dict.values()))
        keys = list(label_dict.keys())
        # set threshhold to limit plotting labels too close together
        min_dist_2 = label_frac * max(embed_vals.max(axis=0) - embed_vals.min(axis=0)) ** 2
        labeled_vals = np.array([2*embed_vals.max(axis=0)])
        n = int(plot_frac*len(embed_vals))
        for i in np.random.permutation(len(embed_vals))[:n]:
            if np.min(dist_squared(embed_vals[i], labeled_vals, axis=1)) < min_dist_2:
                continue
            else:
                props = dict(boxstyle='round', lw=2, edgecolor='black', alpha=0.35)
                _ = ax.text(embed_vals[i][0], embed_vals[i][1]+0.02, s=keys[i].split('.')[0],
                            size=10, fontsize=12, verticalalignment='top', bbox=props)
                labeled_vals = np.vstack((labeled_vals, embed_vals[i]))
    if title != None:
        plt.suptitle('ICD-9: Poicare Embedding' + title, size=16);
    if legend_headers != None:
        plt.legend(loc='best')
    plt.show();
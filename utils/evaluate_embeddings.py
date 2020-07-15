# import libraries
import pandas as pd
import numpy as np
import sys

# import modules within repository
my_path = 'C:\\Users\\dreww\\Desktop\\hyperbolic-learning\\utils' # path to utils folder
sys.path.append(my_path)
from utils import *

# NOTE: two globally defined variables are assumed (subchapter_range_name and chapter_range_name)

def get_chapter_nodes(chapter, edge_list):
    """ Return the set of nodes within a given chapter
    Parameters
    ----------
    chapter : must be given in range notation, e.g. '001_139'
    edge_list: list of [u, v] edge pairs
    """
    child_nodes = [e[0] for e in edge_list if e[1] == chapter]
    return child_nodes

def within_chapter_distances(chapter_nodes, embedding_dict):
    # compute all pairwise hyperbolic distances
    D = poincare_distances(np.array([embedding_dict[x] for x in chapter_nodes]))
    mean_dist = D[D>0].mean()
    std_dev = D[D>0].std()
    return [mean_dist, std_dev]

def get_subchapter_nodes(subchapter, edge_list):
    """ Return the set of nodes within a given subchapter
    Parameters
    ----------
    subchapter : must be given in range notation, e.g. '001_007'
    edge_list: list of [u, v] edge pairs
    """
    child_nodes = [e[0] for e in edge_list if e[1] == subchapter]
    return child_nodes

def within_subchapter_distances(subchapter_nodes, embedding_dict):
    # compute all pairwise hyperbolic distances
    if len(subchapter_nodes) <= 1:
        return
    else:
        D = poincare_distances(np.array([embedding_dict[x] for x in subchapter_nodes]))
        mean_dist = D[D>0].mean()
        std_dev = D[D>0].std()
    return [mean_dist, std_dev]

def between_chapter_distances(chapter_nodes, embedding, dist_matrix):
    # compute all pairwise hyperbolic distances
    embedding = embedding[embedding.node != 'ICD-9_Diagnoses'].reset_index(drop=True)
    in_group_indices = embedding[embedding.node.apply(lambda x: x in chapter_nodes)].index
    rows = np.arange(0, dist_matrix.shape[0])
    out_group_indices = list(set(rows).difference(in_group_indices))
    between_dists = [dist_matrix[ix, out_group_indices] for ix in in_group_indices]
    mean_dist = np.mean(between_dists)
    std_dev = np.std(between_dists)
    return [mean_dist, std_dev]

def between_subchapter_distances(subchapter_nodes, embedding, dist_matrix):
    # compute all pairwise hyperbolic distances
    embedding = embedding[embedding.node != 'ICD-9_Diagnoses'].reset_index(drop=True)
    in_group_indices = embedding[embedding.node.apply(lambda x: x in subchapter_nodes)].index
    rows = np.arange(0, dist_matrix.shape[0])
    out_group_indices = list(set(rows).difference(in_group_indices))
    between_dists = [dist_matrix[ix, out_group_indices] for ix in in_group_indices]
    mean_dist = np.mean(between_dists)
    std_dev = np.std(between_dists)
    return [mean_dist, std_dev]

def chapter_metrics(embedding_dict, edge_list, dist_matrix, chapter_range_name):
    # calculate within chapter metrics
    if chapter_range_name is None:
        return
    within_chapter_metrics = {'mean_dists': [], 'std_dev': []}
    for chapter in chapter_range_name.keys():
        chapter_nodes = get_chapter_nodes(chapter, edge_list)
        mean, std = within_chapter_distances(chapter_nodes, embedding_dict)
        within_chapter_metrics['mean_dists'].append(mean)
        within_chapter_metrics['std_dev'].append(std)
    mean_dist_within = np.mean(within_chapter_metrics['mean_dists'])
    std_dev_within = np.mean(within_chapter_metrics['std_dev'])
    
    # calculate between chapter metrics
    emb = pd.DataFrame([[k, v[0], v[1]] for k,v in embedding_dict.items()], columns=['node', 'x', 'y'])
    between_chapter_metrics = {'mean_dists': [], 'std_dev': []}
    for chapter in chapter_range_name.keys():
        chapter_nodes = get_chapter_nodes(chapter, edge_list)
        mean, std = between_chapter_distances(chapter_nodes, emb, dist_matrix)
        between_chapter_metrics['mean_dists'].append(mean)
        between_chapter_metrics['std_dev'].append(std)
    mean_dist_between = np.mean(between_chapter_metrics['mean_dists'])
    std_dev_between = np.mean(between_chapter_metrics['std_dev'])
    return [np.round(x, 3) for x in [mean_dist_within, std_dev_within, mean_dist_between, std_dev_between]]

def subchapter_metrics(embedding_dict, edge_list, dist_matrix, subchapter_range_name):
    if chapter_range_name is None:
        return
    # calculate within group metrics
    within_subchapter_metrics = {'mean_dists': [], 'std_dev': []}
    for subchapter in subchapter_range_name.keys():
        subchapter_nodes = get_subchapter_nodes(subchapter, edge_list)
        if len(subchapter_nodes) <= 1:
            continue
        else:
            mean, std = within_subchapter_distances(subchapter_nodes, embedding_dict)
            within_subchapter_metrics['mean_dists'].append(mean)
            within_subchapter_metrics['std_dev'].append(std)
    mean_dist_within = np.mean(within_subchapter_metrics['mean_dists'])
    std_dev_within = np.mean(within_subchapter_metrics['std_dev'])
    
    # calculate between group metrics
    emb = pd.DataFrame([[k, v[0], v[1]] for k,v in embedding_dict.items()], columns=['node', 'x', 'y'])
    between_subchapter_metrics = {'mean_dists': [], 'std_dev': []}
    for subchapter in subchapter_range_name.keys():
        subchapter_nodes = get_subchapter_nodes(subchapter, edge_list)
        if len(subchapter_nodes) <= 1:
            continue
        else:
            mean, std = between_subchapter_distances(subchapter_nodes, emb, dist_matrix)
            between_subchapter_metrics['mean_dists'].append(mean)
            between_subchapter_metrics['std_dev'].append(std)
    mean_dist_between = np.mean(between_subchapter_metrics['mean_dists'])
    std_dev_between = np.mean(between_subchapter_metrics['std_dev'])
    return [np.round(x, 3) for x in [mean_dist_within, std_dev_within, mean_dist_between, std_dev_between]]

def evaluate_embedding(embedding_dict, edge_list):
    # need to define pairwise distances for each embedding
    emb_data = np.array(list(embedding_dict.values()))
    D = poincare_distances(emb_data)
    D_symm = D.T + D
    
    # store all chapter and subchapter metrics
    eval_metrics = {}
    eval_metrics['chapter'] = chapter_metrics(embedding_dict, edge_list, D_symm)
    eval_metrics['subchapter'] = subchapter_metrics(embedding_dict, edge_list, D_symm)
    return eval_metrics

#embedding_dicts = [emb_dict, hyper_emb_dict, laplacian_emb_dict]
#embeddings = ['Poincare', 'HyperMap', 'LaBNE']
#overall_metrics = {}
#for i in range(len(embeddings)):
#    overall_metrics[embeddings[i]] = evaluate_embedding(embedding_dicts[i], edge_list)
#overall_metrics
#
#from prettytable import PrettyTable
#x = PrettyTable()
#x.field_names = ["Embedding", "Category", "Within Category", "Outside Category"]
#val_lists = [[overall_metrics[k]['chapter'], overall_metrics[k]['subchapter']] for k in overall_metrics.keys()]
#for i, l in enumerate(val_lists):
#    v1 = str(l[0][0]) + ' (' + str(l[0][1]) + ')'
#    v2 = str(l[0][2]) + ' (' + str(l[0][3]) + ')'
#    v3 = str(l[1][0]) + ' (' + str(l[1][1]) + ')'
#    v4 = str(l[1][2]) + ' (' + str(l[1][3]) + ')'
#    x.add_row([embeddings[i], 'Chapter', v1, v2])
#    x.add_row([embeddings[i], 'Subchapter', v3, v4])
#print(x)

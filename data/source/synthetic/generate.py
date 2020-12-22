import networkx as nx
import json


def write_json_graph(G, filename):
    with open(filename, 'w') as outfile:
        json.dump(nx.node_link_data(G), outfile)


write_json_graph(nx.connected_caveman_graph(3, 5), 'connected_caveman_graph(3,5).json')
write_json_graph(nx.connected_caveman_graph(4, 2), 'connected_caveman_graph(4,2).json')
write_json_graph(nx.connected_caveman_graph(4, 3), 'connected_caveman_graph(4,3).json')
write_json_graph(nx.connected_caveman_graph(4, 4), 'connected_caveman_graph(4,4).json')
write_json_graph(nx.connected_caveman_graph(4, 5), 'connected_caveman_graph(4,5).json')
write_json_graph(nx.connected_caveman_graph(5, 4), 'connected_caveman_graph(5,4).json')
write_json_graph(nx.connected_caveman_graph(7, 4), 'connected_caveman_graph(7,4).json')
write_json_graph(nx.connected_caveman_graph(10, 10), 'connected_caveman_graph(10,10).json')
write_json_graph(nx.connected_caveman_graph(10, 20), 'connected_caveman_graph(10,20).json')
write_json_graph(nx.connected_caveman_graph(15, 30), 'connected_caveman_graph(15,30).json')

write_json_graph(nx.balanced_tree(5, 4), 'balanced_tree(5,4).json')
write_json_graph(nx.balanced_tree(3, 3), 'balanced_tree(3,3).json')
write_json_graph(nx.balanced_tree(3, 4), 'balanced_tree(3,4).json')
write_json_graph(nx.balanced_tree(3, 5), 'balanced_tree(3,5).json')
write_json_graph(nx.balanced_tree(3, 6), 'balanced_tree(3,6).json')
write_json_graph(nx.balanced_tree(3, 7), 'balanced_tree(3,7).json')
write_json_graph(nx.balanced_tree(3, 10), 'balanced_tree(3,10).json')
write_json_graph(nx.balanced_tree(4, 4), 'balanced_tree(4,4).json')
write_json_graph(nx.balanced_tree(4, 7), 'balanced_tree(4,7).json')
write_json_graph(nx.balanced_tree(5, 2), 'balanced_tree(5,2).json')

write_json_graph(nx.barabasi_albert_graph(10, 5), 'barabasi_albert_graph(10,5).json')
write_json_graph(nx.barabasi_albert_graph(20, 3), 'barabasi_albert_graph(20,3).json')
write_json_graph(nx.barabasi_albert_graph(20, 10), 'barabasi_albert_graph(20,10).json')
write_json_graph(nx.barabasi_albert_graph(50, 40), 'barabasi_albert_graph(50,40).json')

write_json_graph(nx.random_lobster(5, 0.6, 0.4, seed=0), 'random_lobster(5,0_6,0_4).json')
write_json_graph(nx.random_lobster(5, 0.4, 0.6, seed=0), 'random_lobster(5,0_4,0_6).json')
write_json_graph(nx.random_lobster(10, 0.6, 0.4, seed=0), 'random_lobster(10,0_6,0_4).json')
write_json_graph(nx.random_lobster(10, 0.4, 0.6, seed=0), 'random_lobster(10,0_4,0_6).json')
write_json_graph(nx.random_lobster(20, 0.6, 0.4, seed=0), 'random_lobster(20,0_6,0_4).json')
write_json_graph(nx.random_lobster(20, 0.4, 0.6, seed=0), 'random_lobster(20,0_4,0_6).json')
write_json_graph(nx.random_lobster(50, 0.6, 0.4, seed=0), 'random_lobster(50,0_6,0_4).json')
write_json_graph(nx.random_lobster(50, 0.4, 0.6, seed=0), 'random_lobster(50,0_4,0_6).json')
write_json_graph(nx.random_lobster(100, 0.6, 0.4, seed=0), 'random_lobster(100,0_6,0_4).json')
write_json_graph(nx.random_lobster(100, 0.4, 0.6, seed=0), 'random_lobster(100,0_4,0_6).json')

write_json_graph(nx.lollipop_graph(5, 4), 'lollipop_graph(5,4).json')
write_json_graph(nx.lollipop_graph(10, 5), 'lollipop_graph(10,5).json')
write_json_graph(nx.lollipop_graph(10, 50), 'lollipop_graph(10,50).json')

write_json_graph(nx.petersen_graph(), 'petersen_graph().json')
write_json_graph(nx.octahedral_graph(), 'octahedral_graph().json')
write_json_graph(nx.pappus_graph(), 'pappus_graph().json')
write_json_graph(nx.dodecahedral_graph(), 'dodecahedral_graph().json')
write_json_graph(nx.frucht_graph(), 'frucht_graph().json')



write_json_graph(nx.star_graph(10), 'star_graph(50).json')
write_json_graph(nx.star_graph(50), 'star_graph(50).json')
write_json_graph(nx.star_graph(100), 'star_graph(50).json')

write_json_graph(nx.ring_of_cliques(5, 80), 'ring_of_cliques(5,80).json')
write_json_graph(nx.ring_of_cliques(6, 70), 'ring_of_cliques(6,70).json')

write_json_graph(nx.barbell_graph(3, 4), 'barbell_graph(3,4).json')
write_json_graph(nx.barbell_graph(3, 8), 'barbell_graph(3,8).json')
write_json_graph(nx.barbell_graph(5, 2), 'barbell_graph(5,2).json')
write_json_graph(nx.barbell_graph(5, 0), 'barbell_graph(5,0).json')
write_json_graph(nx.barbell_graph(50, 20), 'barbell_graph(50,20).json')
write_json_graph(nx.barbell_graph(50, 50), 'barbell_graph(50,50).json')

write_json_graph(nx.dorogovtsev_goltsev_mendes_graph(2), 'dorogovtsev_goltsev_mendes_graph(2).json')
write_json_graph(nx.dorogovtsev_goltsev_mendes_graph(3), 'dorogovtsev_goltsev_mendes_graph(3).json')
write_json_graph(nx.dorogovtsev_goltsev_mendes_graph(4), 'dorogovtsev_goltsev_mendes_graph(4).json')
write_json_graph(nx.dorogovtsev_goltsev_mendes_graph(5), 'dorogovtsev_goltsev_mendes_graph(5).json')

write_json_graph(nx.navigable_small_world_graph(8), 'navigable_small_world_graph(8).json')
write_json_graph(nx.navigable_small_world_graph(20), 'navigable_small_world_graph(20).json')

write_json_graph(nx.circular_ladder_graph(5), 'circular_ladder_graph(5).json')
write_json_graph(nx.circular_ladder_graph(100), 'circular_ladder_graph(100).json')


write_json_graph(nx.duplication_divergence_graph(50,0.5,seed=0), 'duplication_divergence_graph(50,0_5).json')

write_json_graph(nx.balanced_tree(3,4), 'balanced_tree(3,4).json')
write_json_graph(nx.balanced_tree(3,5), 'balanced_tree(3,5).json')
write_json_graph(nx.balanced_tree(3,8), 'balanced_tree(3,8).json')
write_json_graph(nx.balanced_tree(4,5), 'balanced_tree(4,5).json')
write_json_graph(nx.balanced_tree(4,6), 'balanced_tree(4,6).json')
write_json_graph(nx.balanced_tree(4,7), 'balanced_tree(4,7).json')


write_json_graph(nx.watts_strogatz_graph(100,3,0.05), 'watts_strogatz_graph(100,3,0.05).json')
write_json_graph(nx.watts_strogatz_graph(100,3,0.25), 'watts_strogatz_graph(100,3,0.25).json')
write_json_graph(nx.watts_strogatz_graph(100,3,0.5), 'watts_strogatz_graph(100,3,0.5).json')
write_json_graph(nx.watts_strogatz_graph(100,4,0.05), 'watts_strogatz_graph(100,4,0.05).json')
write_json_graph(nx.watts_strogatz_graph(100,4,0.25), 'watts_strogatz_graph(100,4,0.25).json')
write_json_graph(nx.watts_strogatz_graph(100,4,0.5), 'watts_strogatz_graph(100,4,0.5).json')
write_json_graph(nx.watts_strogatz_graph(100,5,0.05), 'watts_strogatz_graph(100,5,0.05).json')
write_json_graph(nx.watts_strogatz_graph(100,5,0.25), 'watts_strogatz_graph(100,5,0.25).json')
write_json_graph(nx.watts_strogatz_graph(100,5,0.5), 'watts_strogatz_graph(100,5,0.5).json')

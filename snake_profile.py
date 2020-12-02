from snake_evo import Population #pylint: disable=import-error
from line_profiler import LineProfiler

P = Population(n_pop=100, blocks_width=15, blocks_height=10, hidden_sizes=[10,10])

ag = P.pop[0]

lp = LineProfiler()

lp.add_function(ag.predict)
lp_wrapper = lp(ag.play)
lp_wrapper(blocks_height = 10, blocks_width = 15, threshold = 10)
lp.print_stats()
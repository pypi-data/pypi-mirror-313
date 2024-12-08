import cProfile
import pstats
from test_bok_improved_method import main

# Profile the entire script with command-line arguments
cProfile.run('main("new_100k_6_cat.csv","logisticRegression")', 'profile_stats')

# Analyze the profile data
p = pstats.Stats('profile_stats')
p.sort_stats('cumulative').print_stats()
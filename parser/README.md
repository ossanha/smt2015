# How to run a test

Once ran, the generated benchmarks will be saved as Python pickles
(i.e. serialized data) for further use as in any of the two sections below.

# How to generate the test configurations

1. In `benches.conf`, put the pairs title / directory that you
   want to test.
2. In `.benchmarks.ini`, prepare the list of tools you want to test, as well as
   their command and names (used for later pickle generation)
3. Run `make test_conf`. This should generate one `.smtbench_<title>.ini` file
for each directory you want to test.

If you wish, you can directly put all directories to be test as title /
directory pair under the `bench_directories` section of `.benchmarks.ini`. In
the current state of the benchmarks script, this is however less modular.

Running `make all_tests` will run `benchmarks.py` for all the `.*.ini` files of
the directories.


# How to compute a ranking for the test

Say you want to see the rankings for the auflira category. Typing

~~~~{.sh}
# ./benchmark.py -ld -pd auflira
~~~~

will load and display the rankings for the category, displaying for each match:
* the number of wins, draws and losses for the match,
* the timing of the average win and of the average loss,
* the best win, with the name of the file
* the worst loss, with the name of the file

## How ranking works

Ranking is done according to sum of the points the tools get in direct
confrontations

If a tool fails for a given benchmark and not the other, the latter is declared
the winner. If both have a return code different than 0, it is a draw. Otherwise
we have 2 tools with the same return code of 0. In this case, we
consider that a tool beat another on a benchmark whenever the timed difference
is at least 20% of the higher time and also higher than 0.01 second.

A match (i.e. a series of benchmark) is declared a draw if benchmark draws
represent at least half the scores and no tool has more
than twice the number of wins of the other. Otherwise, the number of wins
decides the winner. The winner of a confrontation scores 2 points, the loser 0;
if it is draw, both score 1 point.


# See the raw data

Raw data for the generated tests are available as Python pickles, that can be
used by `benchmark.py` or other Python scripts.

A textual version can also be generated

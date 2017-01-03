Title: randchop.py
Author: Judah High

Description: Takes two arguments (1) an .xyz formatted trajectory file from
a molecular dynamics simulation and (2) the number of frames out of that
trajectory file should be extracted at random.

The script will use a randomly seeded number generator to chop frames out
of the trajectory into separate .xyz files stored in a newly created
directory within the current working directory called chopped_frames.

Use: user provides two arguments as specified in the description.

>> python randchop.py trajectories.xyz 100

from   matplotlib import pyplot
import re, argparse
import numpy as np
import plistlib
import sys


# +-----------------------------------------+
# | FIND COMMON TRACKS AMONG MULTIPLE FILES |
# +-----------------------------------------+

def findCommonTracks(fileNames):

    # A list of sets of track names
    trackNameSets = []

    # +------------------------+
    # | LOOP THROUGH FILENAMES |
    # +------------------------+
    
    for fileName in fileNames:

        # Create a new set
        trackNames = set()

        # Read in playlist
        plist = plistlib.readPlist(fileName)

        # Get the tracks
        tracks = plist['Tracks']

        # Iterate through the tracks
        for trackId, track in tracks.items():
            try:
                # Add the track name to a set
                trackNames.add(track['Name'])
            except:
                # Ignore
                pass
        # Add to list
        trackNameSets.append(trackNames)

    # Get the set of common Tracks
    commonTracks =  set.intersection(*trackNameSets)

    # Write to a file
    if len(commonTracks) > 0:
        f= open("common.txt", "w")
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s)
        f.close()
        print("%d common tracks found. "
              "Track names written to common.txt." % len(commonTracks))
    else:
        print("No common tracks!")


# +--------------------------+
# | COLLECT STATICS OF SONGS |
# +--------------------------+

def plotStats(fileName):

    # Read in a playlist
    plist = plistlib.readPlist(fileName)

    # Get tracks from playlist
    tracks = plist['Tracks']

    # Create list of song ratings and track durations
    durations = []
    ratings   = []

    # Iterate through the tracks
    for trackId, track in tracks.items():
        try:
            durations.append(track['Total Time'])
            ratings.append(track['Album Rating'])
        except:
            # Ignore
            pass

    # Ensure that valid data was collected
    if ratings == [] or durations == []:
        print("No valid Album Rating/Total Time data in %s." % fileName)
        return
    
    # +--------------------------+
    # | PLOT DATA (SCATTER PLOT) |
    # +--------------------------+

    # Create numpy arrays for duration(x) and ratings(y)
    x = np.array(durations, np.int32)
    y = np.array(ratings, np.int32)
    
    # Convert duration to minutes
    x = x/60000.0

    # +------------+
    # | MATPLOTLIB |
    # +------------+

    # Construct graph
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track Duration')
    pyplot.ylabel('Track Rating')

    # Plot histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track Duration')
    pyplot.ylabel('Count')

    #Show Plot
    pyplot.show()

    
# +-------------------------------------+
# | FIND DUPLICATES IN A GIVEN PLAYLIST |
# +-------------------------------------+

def findDuplicates(fileName):
    print("finding duplicate tracks in %s..." % fileName)

    # +--------+
    # | TRACKS |
    # +--------+
    
    # Read in playlist file
    plist = plistlib.readPlist(fileName)
    # Get tracks from tracks dictionary
    tracks = plist['Tracks']
    # Create a track name dictionary
    trackNames = {}

    # +-------------+
    # | TRACKS LOOP |
    # +-------------+

    # Iterate through the tracks
    for trackId, track in tracks.items():
        try:
            name     = track['Name']
            duration = track['Total Time']

            #Look for existing entries
            if name in trackNames:

                # If a name and duration match, increament the count
                # round the track length to the nearest second
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name] = (duration, count+1)
                else:
                    # Add dictionary entry as tuple (duration, count)
                    trackNames[name] = (duration, 1)
        except:
            # Ignore
            pass
        
    # +--------------+
    # | EXTRACT DUPS |
    # +--------------+

    # Store duplicates as (name, count) tuples
    dups = []

    # Iterate through the track names
    for k, v in trackNames:
        if v[1] > 1:
            dups.append((v[1], k))

    # Save duplicates to a file
    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
    else:
        print("No duplicate tracks found!")
        
    f = open("dups.txt", "w")
    for val in dups:
        f.write("[%d] %s\n" % (val[0], val[1]))
    f.close()
    
# +-------------+
# | MAIN METHOD |
# +-------------+

def main():

    # Create parser
    descStr = """
    This program analyzes playlist files (.xml) exported from iTunes.
    """

    parser = argparse.ArgumentParser(description=descStr)
    # Add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # Add expected arguments
    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dups', dest='plFileD', required=False)

    # Parse args
    args = parser.parse_args()

    if args.plFiles:
        # Find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # Plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # Find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")

if __name__ == '__main__':
    main()

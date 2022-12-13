# you will need to install following instructions at:
# https://bgpstream.caida.org/docs/install
# https://bgpstream.caida.org/docs/api/pybgpstream
import pybgpstream
from collections import OrderedDict
 
# this is the beview file you have downloaded
BVIEWFILE="/Users/mjreed/nobackup/libbgpstreamer/example-data/bview.20220707.0800"
 
# you can also use the bgpreader tool to show the contents of the file
# bgpreader -d singlefile -c rrc00 -o rib-file= -m /Users/mjreed/nobackup/libbgpstreamer/example-data/bview.20220707.0800 
 
 
# the file is read as a stream (so you have to access each entry, or element
# one at a time)
# you first have to open the stream with certain search parameters
stream = pybgpstream.BGPStream(
    # note using add_interval_filter to get all entries in file
    # this gets all entries in any time (ie from zero unix time to max unix time)
    from_time="0",            until_time="4294967295",
    
    # we do not need this to be set for bview file, it is dependent on the file
    #collectors=["rrc01"],
    # this tells it to read routing information
    record_type="ribs",
    # it is possible to filter, but the syntax is difficult to work out
    #filter="peer 11666 and prefix more 210.180.0.0/16"
    #filter="peer "+source
)
 
# tel the stream to read from a singlefile, else it gets from the internet which is very slow
stream.set_data_interface("singlefile")
## this is a bview from RCC01
stream.set_data_interface_option("singlefile","rib-file",BVIEWFILE)
 
# will use this as a simple counter
i=0
# I am setting this so that it only shows a small amount of data to save time
maxcount=500
# if you want them all you could use
#maxcount=float('inf')
 
uniquePaths = dict()
uniquePeers = dict()
uniqueASNs = dict()
pathPairs = dict()
 
# this reads each routing entry in the stream. Syntax for this is
# available from https://bgpstream.caida.org/docs/api/pybgpstream
for elem in stream:
   # record fields can be accessed directly from elem
   # e.g. elem.time
   # or via elem.record
   # e.g. elem.record.time
    i=i+1
    # stop if we reach maxcount
    if i > maxcount:
        break
        #None
    print(elem)
    # add the peer to the unique Peer dict and count how many times we have seen this peer
    if elem.peer_asn in uniquePeers:
        uniquePeers[elem.peer_asn] = uniquePeers[elem.peer_asn] + 1
    else:
        uniquePeers[elem.peer_asn] = 1
    # this can split the path into a array if you want it to analyse it
    path = elem._maybe_field("as-path").split()
 
    # this gets the list of unique paths (ignores ones that are repeated)
    uniquePath = list(OrderedDict.fromkeys(path))
    uniquePathStr = ' '.join(uniquePath)
    
    if len(path) > 0:
        destASN = path[-1]
        if destASN in uniqueASNs:
            uniqueASNs[destASN] = uniqueASNs[destASN] + 1
        else:
            #print("New ASN " + destASN)
            uniqueASNs[destASN] = 1
        if uniquePathStr in uniquePaths:
            uniquePaths[uniquePathStr] = uniquePaths[uniquePathStr] + 1
        else:
            uniquePaths[uniquePathStr] = 1
 
        
#print(uniquePaths)
#print(uniquePeers)
#print(uniqueASNs)
print("Num paths = "+str(len(uniquePaths)))
print("Num peers = "+str(len(uniquePeers)))
print("Num ASNs = "+str(len(uniqueASNs)))


pip install \
    --global-option build_ext \
    --global-option '--include-dir=/Users/swaroop/src/libbgpstream-2.2.0/include' \
    --global-option '--library-dir=/Users/swaroop/src/libbgpstream-2.2.0/lib' \
    pybgpstream
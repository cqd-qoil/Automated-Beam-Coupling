import sys
import time
import clr

# Paths for ttInterface.dll - Update these accordingly
sys.path.append("C:\\...\\Release")
clr.AddReference("C:\\...\\Release\\ttInterface.dll")

from System import Array, Byte, Int64
from TimeTag import TTInterface

# Initialize the time tagger
MyTagger = TTInterface()
MyTagger.Open()  # Assuming it's okay to let it automatically select the device

# Configure the channel for measurement
test_channel = 2
MyTagger.SetInputThreshold(test_channel, 0.5)

# Start time tagging mode
MyTagger.StartTimetags()

# Preallocate buffers
chans = Array.CreateInstance(Byte, 10000000)
times = Array.CreateInstance(Int64, 10000000)

# Capture readings for 1 second
time.sleep(1)
(num_tags, chans, times) = MyTagger.ReadTags(chans, times)

# Stop time tagging mode
MyTagger.StopTimetags()

# The arrays 'chans' and 'times' now hold the readings for 1 second.
# Additional analysis can be done on these data as required.

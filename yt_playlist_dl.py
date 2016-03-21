# Python script to download all videos from a YouTube playlist as .m4a audio
# files and save them in a folder. "pafy" library is a dependency (can be
# installed using pip)
import pafy     # Has to be installed
import ftfy     # Has to be installed
import re
import os

# Enter playlist's URL
url = raw_input("Please enter a valid YouTube playlist URL: ")
playlist = pafy.get_playlist2(url)

print("\n"+playlist.title+" successfully opened")
# Create a folder for saving all the songs there
if not os.path.exists(playlist.title):
    os.makedirs(playlist.title)
# Cycle over all videos in the playlist, skip any that has problems
counter = 0
errors = 0
for video in playlist:
    counter += 1
    print("- Retrieving audio "+str(counter)+" of "+str(len(playlist))+"...")
    if not re.findall("Deleted video", video.title):
        audiostreams = video.audiostreams
        audio_options = []
        # Cycle over all the audio streams available in the video
        for audio in audiostreams:
            # Get only m4a format streams
            if re.findall('m4a',audio.extension):
                audio_options.append(audio)
        # Get the highest quality m4a audio (typically, the latest in the list)
        # if there was a m4a option anyway...
        try:
            if audio_options:
                audio_options[-1].download(filepath="./"+playlist.title+"/"+ftfy.fix_text(video.title)+"."+audio_options[-1].extension)
                print("\nAudio "+str(counter)+" retrieved correctly")
            else:
                print("XXX Audio "+str(counter)+" couldn't be retrieved (no m4a stream available)")
                errors += 1
        except:
            print("XXX Audio "+str(counter)+" couldn't be retrieved")
            errors += 1
            pass

if (errors != 0):
    print("\nDownload completed with "+str(errors)+" errors")
else:
    print("\nAll songs downloaded!")

# Once finished, open the folder in the file explorer
if (os.name is 'nt'):
    os.startfile(playlist.title)
elif (os.name is 'os2'):
    os.system('open "%s"' % playlist.title)
elif (os.name is 'posix'):
    os.system('xdg-open "%s"' % playlist.title)
else:
    pass

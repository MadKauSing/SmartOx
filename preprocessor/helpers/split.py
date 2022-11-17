from pydub import AudioSegment


#helps to divide songs into time segments
#input pydub:AudioSegement
#output list of pydub:AudioSegments


def divide_3_secs(mp3_file:AudioSegment,no_of_segments:int):
    song_parts=[]
    try:
        for i in range(no_of_segments):
            start=3000*i
            end=3000*(i+1)
            try:
                #takes care if the song runs out
                part=mp3_file[start:end]
                if part!=AudioSegment.empty():
                    song_parts.append(part)
            except:
                continue
    except:
        print("I think song too small")
    return song_parts

def divide_6_secs(mp3_file:AudioSegment,no_of_segments:int):
    song_parts=[]
    try:
        for i in range(no_of_segments):
            start=6000*i
            end=6000*(i+1)
            try:
                #takes care if the song runs out
                part=mp3_file[start:end]
                if part!=AudioSegment.empty():
                    song_parts.append(part)
            except:
                continue
    except:
        print("I think song too small")
    return song_parts

def divide_10_secs(mp3_file:AudioSegment,no_of_segments:int):
    song_parts=[]
    try:
        for i in range(no_of_segments):
            start=10000*i
            end=10000*(i+1)
            #takes care if the song runs out
            try:
                part=mp3_file[start:end]
                if part!=AudioSegment.empty():
                    song_parts.append(part)
            except:
                continue
    except:
        print("I think song too small")
    return song_parts


def main():

    filename='Marika Takeuchi - Melding.mp3'
    mp3_file=AudioSegment.from_file(file=filename,format="mp3")

    song_parts=divide_6_secs(mp3_file,100)
    for index,part in enumerate(song_parts):
        outname=filename+"_"+str(index)
        part.export(out_f=f"{outname}.mp3",format="mp3")

if __name__=='__main__':
    main()

#--------------------------------------------------
# print(type(mp3_file))
# print(mp3_file.frame_rate,"FRAME RATE")
# print(mp3_file.channels,"NO OF CHANNELS")
# print(mp3_file.max,"MAX AMPLITUDE")
# print(len(mp3_file))


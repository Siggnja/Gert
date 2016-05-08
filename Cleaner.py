import os
import re
import PTN
import logging
#####Setting Logger#####
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename ='logger.log', mode='w',encoding='utf-8')
logger.addHandler(handler)

videoTypes = ['.avi', '.mkv', '.wmv', '.mp4','.flv'] #List of videotypes
music = ['.mp3'] #List of music types


#SHOWS = "C:\\Users\\Sverrir\\OneDrive\\HR\\1 ár - Vorönn\\Python\\Verkefni\\Verkefni 4\\TV\\Shows\\"
#MOVIES = "C:\\Users\\Sverrir\\OneDrive\\HR\\1 ár - Vorönn\\Python\\Verkefni\\Verkefni 4\\TV\\Movies\\"
#TEST = "C:\\Users\\Sverrir\\OneDrive\\HR\\1 ár - Vorönn\\Python\\Verkefni\\Verkefni 4\\Tester"
######
#SHOWSS = "C:\\Users\Sigurdur\\Documents\\HR - 1 ár\\Python\\Verkefni 4\\TV\\Shows\\"
#MOVIESS = "C:\\Users\\Sigurdur\\Documents\\HR - 1 ár\\Python\\Verkefni 4\\TV\Movies\\"
#MUSIC = "C:\\Users\\Sigurdur\\Documents\\HR - 1 ár\\Python\\Verkefni 4\\TV\Music\\"
#TESTS = "C:\\Users\\Sigurdur\\Documents\\HR - 1 ár\\Python\\Verkefni 4\\downloads"
BASE  = "C:\\Users\\Sigurdur\\Documents\\HR - 1 ár\\Python\\Verkefni 4\\TV"

def movefile(s):

    filename = os.path.basename(s)

    result = checkFileRace(filename)
    if result == 0: #Deletable file
        try:
            os.remove(s)
        except FileNotFoundError:
            logging.warning('I was not able to find %s' %(s))
        except PermissionError:
            print(s)
            print("I was not allowed to delete %s"%(s))
        
    elif result == 1: #show
        name = getName(filename)

        path = makeShowdir(name)

        try:
            if name == "Unsorted TV Shows":
                path = makeShowdir(name) + "\\" + filename
            else:     
                season = getSeason(filename)
                path = makeseason(name, season) + "\\" + filename
                
            mover(s, path)
        except TypeError:
            logger.warning("%s is an incorrect name" %s)

    
    elif result == 2: #Movie
        name = getName(filename)
        if name == "Unsorted Movies":
            path = MOVIESS + "\\" + filename
        else:
            path = makeMoviedir(name) + "\\" + filename
        mover(s, path)
    elif result == 3: #Music file - mp3
        mover(s,MUSIC+filename)
    
def makeMoviedir(movie): #Creates a directory for the given movie
    path = MOVIESS + movie
    if not os.path.exists(path):
        os.makedirs(path)
    return path
    
    
def makeShowdir(show): #Creates a directory for the given show
    path = SHOWSS + show
    if not os.path.exists(path):
        os.makedirs(path)
    return path
        
def makeseason(show, season): #Creates a directory for the given season of a show
    try:
        path = SHOWSS + show + "\\" + "Season " + str(season)
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    except FileNotFoundError:
        logger.warning( "%s could not be moved!"%(os.path.basename(path)))
    

def mover(old, new): #Deletes the old file and moves it to the new location
    try:
        os.rename(old, new)
    except FileExistsError:
            os.remove(old)
            logging.warning("%s File exists in: %s, deleting file" %(os.path.basename(old),os.path.dirname(new)))
    except FileNotFoundError:
            logger.warning( "%s Not found in: %s"%s (os.path.basename(old),os.path.dirname(old)))
    

def findpaths(folder):
    
    for root, dirs, files in os.walk(folder):
        for f in files:
            fullpath = os.path.join(root, f)
            movefile(fullpath)

    for root, dirs, files in os.walk(folder):
        for f in dirs:
            if os.path.isdir(f):
                pass
            else:
                fullpath = os.path.join(root, f)
    del_dirs(folder)



def getName(name): #Returns the title of a Show or Movie

   try:
        return PTN.parse(name)['title']
       
   except KeyError:
        return "Unsorted"




def getSeason(filename): #Return the season of a Show
    try:
        return PTN.parse(filename)['season']
    except KeyError:
        return None

def checkFileRace(filename): 
    for i in videoTypes:
        if filename.endswith(i):
            if 'sample' in filename.lower():
                return 0
            if getSeason(filename)!=None:
                return 1
            else:
                return 2
    for i in music:
        if filename.endswith(i):
            return 3
    return 0
#This function checks what kind of file the given filename is, return the following values
# 0 = Files to remove
# 1 = Tv Shows
# 2 = Movies
# 3 = Music


def del_dirs(src_dir):
    for dirpath, _, _ in os.walk(src_dir, topdown=False):  # Listing the files
        if dirpath == src_dir:
            break
        try:
            os.rmdir(dirpath)
        except OSError as ex:
            pass

print("Please input the full path of your download folder: ")
temp = input()
SHOWSS = temp + "\\Shows"
MOVIESS = temp + "\\Movies"
MUSIC = temp + "\\Music"
#Creating the directories Shows,Movies,Music in the downloads folder
if not os.path.exists(SHOWSS):
    os.makedirs(SHOWSS)
if not os.path.exists(MOVIESS):
    os.makedirs(MOVIESS)
if not os.path.exists(MUSIC):
    os.makedirs(MUSIC)
    
SHOWSS += "\\"
MOVIESS += "\\"
MUSIC += "\\"
findpaths(temp)

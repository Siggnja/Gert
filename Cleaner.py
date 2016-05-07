import os
import re

videoTypes = ['.avi', '.mkv', '.wmv', '.mp4']

SHOWS = "C:\\Users\\Sverrir\\OneDrive\\HR\\1 ár - Vorönn\\Python\\Verkefni\\Verkefni 4\\TV\\Shows\\"
MOVIES = "C:\\Users\\Sverrir\\OneDrive\\HR\\1 ár - Vorönn\\Python\\Verkefni\\Verkefni 4\\TV\\Movies\\"
TEST = "C:\\Users\\Sverrir\\OneDrive\\HR\\1 ár - Vorönn\\Python\\Verkefni\\Verkefni 4\\Tester"

def movefile(s):


    filename = os.path.basename(s)

    #Fall sem tekur file'inn og tjékkar hvort hann sé þáttur


    result = checkMovieOrShow(filename)
    if result == 0:
        try:
            os.remove(s)
        except FileNotFoundError:
            print(s)
            print("Could not delete file!")
        except PermissionError:
            print(s)
            print("I was not allowed to delete this file!")
        
    elif result == 1:
        name = getShowName(filename)

        path = makeShowdir(name)

        try:
            if name == "Unsorted TV Shows":
                path = makeShowdir(name) + "\\" + filename
            else:     
                season = getSeason(filename)
                path = makeseason(name, season) + "\\" + filename
                
            
            mover(s, path)
        except TypeError:
            print("Name was invalid")


        
    
    elif result == 2:
        name = getMovieName(filename)
        try:
            if name == "Unsorted Movies":
                path = MOVIES + "\\" + filename
            else:
                path = makeMoviedir(name) + "\\" + filename

            mover(s, path)
        except TypeError:
            print("MOVIE ERROR MOVIE ERROR")

    else:
        print("SIDDL EDDEH HVENN EDDEH EG A EKKI AD PRENTAST VENNUR")
    
def makeMoviedir(movie):
    path = MOVIES + movie
    if not os.path.exists(path):
        os.makedirs(path)
    return path
    
    
    
    
def makeShowdir(show):
    path = SHOWS + show
    if not os.path.exists(path):
        os.makedirs(path)
    return path
        
def makeseason(show, season):
    try:
        path = SHOWS + show + "\\" + "Season " + str(season)
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    except FileNotFoundError:
        print(os.path.basename(path), " could not be moved!")
    

def mover(old, new):
    try:
        os.rename(old, new)
    except FileExistsError:
        print(os.path.basename(old), "File exists in: ", os.path.dirname(new))
    except FileNotFoundError:
        print(os.path.basename(old), "Not found in: ", os.path.dirname(old))
    

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
                movefile(fullpath)

    del_dirs(folder)



def getShowName(name):

    #t = re.compile('^((?P<ShowNameA>.*[^ (_.])[ (_.]+( (?P<ShowYearA>\d{4})([(_.]+S(?P<SeasonA>\d{1,2})E(?P<EpisodeA>\d{1,2}))?|(?<!\d{4}[(_.])S(?P<SeasonB>\d{1,2})E(?P<EpisodeB>\d{1,2})|(?P<EpisodeC>\d{3}))|(?P<ShowNameB>.+))')

    #t = re.compile('^( (?P<ShowNameA>.*[^ (.]) [ (.]+ ( (?P<ShowYearA>\d{4}) ([ (.]+S(?P<SeasonA>\d{1,2})E(?P<EpisodeA>\d{1,2}))? | (?<!\d{4}[ (.]) S(?P<SeasonB>\d{1,2})E(?P<EpisodeB>\d{1,2}) | (?P<EpisodeC>\d{3}[^720p|480p]) ) | (?P<ShowNameB>.+) )')

    regtv = re.compile('(.+?)[ .]S(\d\d?)E(\d\d?).*?(?:[ .](\d{3}\d?p)|\Z)?')
    
    tv = regtv.match(name)

    if tv is None:
        x = re.search(".*[sS][0-9]+", name)
        if re.search(".*[sS][0-9]+", name):
            x = x.group()
            x = x[0:-4].strip()
            x = x.replace('.', ' ')
        else:
            x = "Unsorted TV Shows"
        return x.title()
    else:
        return tv.group(1).replace(".", " ")


def getMovieName(name):
    regmovie = re.compile('(.*?[ .]\d{4}).*?(?:[ .](\d{3}\d?p)|\Z)?')

    tv = regmovie.match(name)

    if tv is None:
        return "Unsorted Movies"
    else:
        return tv.group(1).replace(".", " ")
    



def getSeason(filename):
    patterns =      [
                '.*S(\d+)E(\d+).*',
                '(\d+)x(\d+).*'
            ]
    
    for pattern in patterns:
        p = re.compile(pattern, re.I)
        g = p.findall(filename)
        if len(g) > 0:
            season = int(g[0][0])
            return season

    return None

def checkMovieOrShow(filename):
    for i in videoTypes:
        if filename.endswith(i):
            if getSeason(filename)!=None:
                return 1
            else:
                return 2
    return 0

# 0 = other files to remove
# 1 = show
# 2 = movie


def adoptionCandidates(basedir, file):
    dirs = filter(lambda x : os.path.isdir(os.path.join(basedir, x)), os.listdir(basedir))
    if os.path.isdir(file):
        #print '%s is a directory. Aborting' % file
        return []

    (filepath, filename) = os.path.split(file)

    ignoredPhrases = ['-','_']

    candidates = []
    for dir in dirs:
        dirParts = dir.split()
        score = 0
        requiredScore = 0

        for part in dirParts:
            if ignoredPhrases.count(part) > 0:
                continue

            requiredScore = requiredScore + 1

            if filename.find(part) >= 0:
                score = score + 1

        if score == requiredScore:
            candidates.append( (os.path.join(basedir, dir), score) )

        #print '%s scored %i (req: %i)' % (dir, score, requiredScore)

    #for (dir, score) in candidates:
    #       print '%s with score %i' % (dir, score)

    return candidates




def del_dirs(src_dir):
    for dirpath, _, _ in os.walk(src_dir, topdown=False):  # Listing the files
        if dirpath == src_dir:
            break
        try:
            os.rmdir(dirpath)
        except OSError as ex:
            pass


def get_files(src_dir):
# traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(src_dir):
        path = root.split('/')
        for file in files:
            process(os.path.join(root, file))
            os.remove(os.path.join(root, file))

                    

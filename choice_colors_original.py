import os, random, math, string
from random import randint
from math import radians, sin, cos
from psychopy import core, visual, event, gui, misc, data 

def enterSubInfo(expName):
    """Brings up a GUI in which to enter all the subject info."""
    try:
        expInfo = misc.fromFile(expName+'_lastParams.pickle')
    except:
        expInfo = {'ExpTitle':expName,'Subject':'s99', 'Subject Initials':'asb','Start at trial':0,'Experimenter Initials':'asb'}
    expInfo['dateStr']= data.getDateStr() 
    dlg = gui.DlgFromDict(expInfo, title=expName+' Exp', fixed=['dateStr'])
    if dlg.OK:
        misc.toFile(expName+'_lastParams.pickle', expInfo)
    else:
        core.quit()
    return expInfo
    
def showInstructions(instructText1,instructText2,pos=[0,.3],waitKeys=True):
    """ Displays the experiment specific instructional/descriptive text. 
    The position/wrapWidth may need to be changed depending
    on the length of the text."""
    
    instructs1 = visual.TextStim(win, color='#fdfdfd',pos=pos,wrapWidth=1.2, height=.06,text= instructText1)
    instructs2 = visual.TextStim(win, color='#fdfdfd',pos=[coord*-.8 for coord in pos],wrapWidth=1.2, height=.06,text= instructText2)
    instructs1.draw()
    instructs2.draw()
    win.flip()
    
    if waitKeys:
        event.waitKeys()
    else:
        pass
    
def makeDataFile(subject,expName):
    """Make a text file to save data, will not overwrite existing data"""
    fileName = subject+'_'+expName 
    ext =''
    i = 1
    while os.path.exists(fileName+ext+'.txt'): #changes the extenstion on the filename so no file is ever overwritten.
        ext = '-'+str(i)
        i +=1
    dataFile = open(fileName+ext+'.txt', 'w')
    return dataFile

def writeToFile(fileHandle,trial,sync=True):
    """Writes a trial (a dictionary) to a fileHandle, in a specific order, given 
    by overall order (general variables that are always used) and experiment 
    specific variables (variables that vary based on what you're measuring)."""

    overallOrder = ['subject','subInitials','date','experimenter','totalTime','trialNum']
    overallOrder.extend(expVarOrder)
    
    line = ''
    
    #place var names on first line before training
    if trialNum==0:
        for item in overallOrder:
            line += item
            line += '\t'
        line += '\n'
    
    for item in overallOrder:
        line += str(trial[item])
        line += '\t'
    line += '\n' #add a newline
    print(line)
    fileHandle.write(line)
    if sync:
        fileHandle.flush()
        os.fsync(fileHandle)

def generateTraining():
    """Generates initial trial list for training phase, before latencies are added."""
    
    trials = []
    
    for trial in range(numTraining):
        trials.append({'latency':'NA','avgChoiceTime':'NA'})
        
    return trials
    
def generateExperimental(throwOut=15):
    """Generates experimental trials."""
    
    # time before the red target appears
    choiceLatencies = [3,5,7,9,15,30,60]
    #choiceLatencies = [9]
    askConf = [0,1]
    
    # generate experimental trials
    # reps are number of times all latency types loop (i.e.,numTrials/numLatencies)
    trials = []
    
    for rep in range(reps):
        for latency in choiceLatencies:
            for asked in askConf:
                trials.append({'latency':int(latency),'avgChoiceTime':'NA','askConf':asked})
            
    # randomly shuffle only experimental trials
    random.shuffle(trials)
            
    return trials
    
def addTrialVariables():
    """Adds extra trial details to each line written to the datafile."""
    trial['subject'] = expInfo['Subject']
    trial['subInitials'] = expInfo['Subject Initials']
    trial['experimenter'] = expInfo['Experimenter Initials']
    trial['date'] = expInfo['dateStr']
    trial['totalTime'] = expClock.getTime()
    trial['trialNum'] = trialNum + 1 #add 1 because index starts at 0
    trial['circlePositions'] = circlePositions
    trial['response'] = response
    trial['responseTime'] = responseTime
    trial['choiceTime'] = choiceTime
    trial['confAnswer'] = confAnswer
    trial['colorOptions'] = colorOptions

def readySequence():
    """Prompts subject with "Ready" screen and counts down to stimulus presentation."""
    
    ready.draw()
    trialDisplay = visual.TextStim(win,text=trialNum+1,height=.08,pos=(0,-.8),color=[1,1,1]) #displays trial num.
    trialDisplay.draw()
    win.flip()
    
    # check for 'q' press to quit experiment prematurely
    if ['q']==event.waitKeys(keyList=['space','q']):
        quit.draw()
        win.flip()
        if ['y']==event.waitKeys(keyList=['y','n']):
            dataFile.close()
            win.close()
            core.quit()
        else:
            ready.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
    
    fixation.draw()
    win.flip()
    core.wait(.5)

def presentStimuli(numCircles,askConf,latency='NA',training=False):
    """Draws non-overlapping letters in window for specified time."""

    #letterOptions = random.sample(string.ascii_uppercase,numCircles)
    colorOptions = ['Red','Gold','Lime','Fuchsia','Aqua','Coral']
    random.shuffle(colorOptions)
    fixedCirclesLatency = 9

    # create letter/masking circle stimuli
    circles = []
    letters = []
    
    for circleNum in range(numCircles):
        circles.append(visual.Circle(win,size=70,units='pix',fillColor=colorOptions[circleNum],lineColor=colorOptions[circleNum]))
        
    # distance that the 5 letters are from center
    centerDist = 150

    for circleNum,circle in enumerate(circles):
        tryAgain = True
        while tryAgain:
            circleAng = radians(randint(0,360))
            circle.pos = (centerDist*sin(circleAng),centerDist*cos(circleAng))
            tryAgain = False      
            for i in range(circleNum): 
                if circle.overlaps(circles[i]):
                    tryAgain = True
                    break
                    
    if training==True: ##Training Trials
        response = 'NA'
        responseTime = 'NA'
                
        # draw all non-overlapping circles
        for circle in circles:
            circle.draw(win)
        win.flip()

        choiceClock.reset()

        event.waitKeys(keyList=['space'])
        choiceTime = choiceClock.getTime()
    
    else: ##Experimental Trials
        choiceTime = 'NA'
        centerCircle = visual.Circle(win,size=70,units='pix',pos=[0,0],fillColor=colorOptions[1],lineColor=colorOptions[1])
        
        if fixedCirclesLatency > latency:
            print("Main circle draws first")
            for n in range(fixedCirclesLatency):
                for circle in circles:
                    circle.draw(win)
                if n >= latency:
                    centerCircle.draw(win)
                win.flip()
            centerCircle.draw(win)
            win.flip()

        elif fixedCirclesLatency < latency:
            print("Main circle draws second")
            for n in range(latency):
                if n <= fixedCirclesLatency:
                    for circle in circles:
                        circle.draw(win)
                win.flip()
            centerCircle.draw(win)
            win.flip()
                
        else:
            print("Every circle draws at the same time")
            for n in range(latency):
                centerCircle.draw(win)
                for circle in circles:
                    circle.draw(win)
                win.flip()
            centerCircle.draw(win)
            win.flip()
            
        # draw all non-overlapping circles for specified latency time
        #for n in range(latency):
        #    for circle in circles:
        #        circle.draw(win)
        #    win.flip()
        
        #centerCircle = visual.Circle(win,size=70,units='pix',pos=[0,0],fillColor=colorOptions[1],lineColor=colorOptions[1])

        #for circle in circles:
            #circle.fillColor='White'
        #    circle.draw(win)
        #centerCircle.draw(win)
        #win.flip()
    
        responseClock.reset()
    
        # store whether subject guessed target circle (y/n) and when
        response = event.waitKeys(keyList=['y','n','d'])
        responseTime = responseClock.getTime()
        
        # ask the confidence question if one of the designated trials
        if askConf and response!=['d']:
            confQuestionVisual.draw(win)
            win.flip()
            confAnswer = event.waitKeys(keyList=['1','2','3','4','5'])
        else: 
            confAnswer = 'NA'
    
    # store final positions of all circles
    circlePositions = [str(letter.pos) for letter in letters]
    colorOptions=colorOptions[:2]
    
    return circlePositions,response,responseTime,choiceTime,confAnswer,colorOptions

## Define Experimental Variables ##
expVarOrder = ['latency','avgChoiceTime','circlePositions','response','responseTime','choiceTime','confAnswer','colorOptions']
expInfo = enterSubInfo('Color Choice')
dataFile = makeDataFile(expInfo['Subject'],expInfo['ExpTitle'])

win = visual.Window([1200,1200],color=[-1,-1,-1],fullscr=True,monitor='testMonitor')
ready = visual.TextStim(win,text='Ready?',height=.3,color=[1,1,1])
fixation = visual.TextStim(win,text='+',height=.07,color=[1,1,1])
quit = visual.TextStim(win,text='Quit experiment now (y/n)?',height=.1,color=[1,1,1])
confQuestionText = 'On a scale from 1 to 5, how confident are you in your response (1=not at all confident, 5=extremely confident)?'
confQuestionVisual = visual.TextStim(win,color='#fdfdfd',wrapWidth=1.2, height=.06,text=confQuestionText)

mouse = event.Mouse(visible=False,win=win)

expClock = core.Clock()
responseClock = core.Clock()
choiceClock = core.Clock()

## Practice Instructions ##
text1 = 'Welcome to the experiment. The instructions are going to follow. \
Since we are also running this experiment with children, the instructions \
are written in rather simple language.'

text2 = 'This experiment is going to look at how people choose objects on a screen. \
Here is what is going to happen. First, a plus sign (+) is going to flash in the middle \
of the screen. And then 2 different colored circles will suddenly show up on the screen. You will not \
know where these circles are going to show up. As quickly as you can, you will have to \
choose one of these circles in your head and remember the circle you chose. You can \
choose a circle in whatever way you want; there is no right choice. (Press any key to continue.)'

showInstructions(text1,text2)

text1 = 'At some point after the 2 circles show up on the screen, a new circle, which matches the color of one of the 2 circles you saw, \
will appear in the middle of the screen. If this new circle has the same color as the circle \
you remember choosing, indicate yes by pressing Y \
on your keyboard. If it does not have the same color as the circle you remember choosing, press N, indicating no.'

text2 = 'This process will sometimes occur very quickly, so it is important that you try to \
choose a circle in your head as fast as you can. But, if you tried your hardest and you \
still could not choose a circle before the new circle appeared in the middle, indicate that you did not \
have time to choose a circle, by pressing the D key on your keyboard. (Press any key to continue.)'

showInstructions(text1,text2)

text = 'On some trials, you will be asked how confident you were (on a 1-5 scale) in your judgment about whether or not \
you chose the circle with the same color as the center circle. You may find that you feel very confident on all or most trials, in which \
case it is perfectly acceptable to always answer 5. You may also find that you almost never feel confident about your choice, \
in which case it is perfectly acceptable to always answer 1 or 2. We simply want your honest judgments. (Press any key to continue.)'

instruct = visual.TextStim(win, color='#fdfdfd',pos=[0,0],wrapWidth=1.2, height=.06,text=text)
instruct.draw()
win.flip()
event.waitKeys()

text1 = 'Before the beginning of each activity, the word Ready? will be on the screen. \
To get started, press spacebar at any time. Feel free to take breaks if you need to, \
and ask me if you have any questions or concerns.'

text2 = 'We will first practice this activity a few times. Whenever you are ready, \
press any key to continue.'

showInstructions(text1,text2)


## Practice Trials ##
reps = 1 #go through each kind of experimental trial once for practice
practiceTrials = generateExperimental()

for trialNum,trial in enumerate(practiceTrials):
    readySequence()
    presentStimuli(2,trial['askConf'],trial['latency'])
    
## Final Instructions ##
text = 'Now the real experiment will start. Remember that you can take as many breaks \
as you want and that you should ask me if you have any questions. When you are ready, \
press any key to continue.'

instruct = visual.TextStim(win,color='#fdfdfd',pos=[0,0],wrapWidth=1.2,height=.06,text=text)
instruct.draw()
win.flip()
event.waitKeys()
    
## Experimental Trials ##
reps = 14 #number of experimental trials is reps*number of latencies
experimentalTrials = generateExperimental()

for trialNum,trial in enumerate(experimentalTrials):
    readySequence()
    circlePositions,response,responseTime,choiceTime,confAnswer,colorOptions = presentStimuli(2,trial['askConf'],trial['latency'])
    addTrialVariables()
    writeToFile(dataFile,trial)

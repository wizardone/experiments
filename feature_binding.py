#-*- coding: utf-8 -*-

import os, random, math, string, time
from threading import Timer
from random import randint
from math import radians, sin, cos
from psychopy import core, clock, visual, event, gui, misc, data
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

def enterSubInfo(expName):
    """Brings up a GUI in which to enter all the subject info."""
    try:
        expInfo = misc.fromFile(expName+'_lastParams.pickle')
    except:
        expInfo = {'ExpTitle':expName,'Subject':'s01', 'Subject Initials':'abc','Start at trial':0,'Experimenter Initials':'KV'}
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
    while os.path.exists(fileName+ext+'.xls'): #changes the extenstion on the filename so no file is ever overwritten.
        ext = '-'+str(i)
        i +=1
    dataFile = open(fileName+ext+'.xls', 'w')
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
    
def generateExperimental():
    """Generates experimental trials."""
    
    # time before the red target appears
    choiceLatencies = [3,5,10,15,20,30,60]
    latenciesMilliseconds = [0.05, 0.083, 0.166, 0.25, 0.33, 0.5, 1]
    askConf = [0,1]
    
    # generate experimental trials
    # reps are number of times all latency types loop (i.e.,numTrials/numLatencies)
    trials = []
    
    for rep in range(reps):
        # choiceLatencies was used here
        for latency in latenciesMilliseconds:
            for asked in askConf:
                trials.append({'latency':latency,'avgChoiceTime':'NA','askConf':asked})
            
    # randomly shuffle only experimental trials
    random.shuffle(trials)
            
    return trials
    
def addTrialVariables():
    """Adds extra trial details to each line written to the datafile."""

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

def presentStimuli():
    colorOptions = ['Red','Gold','Lime','Fuchsia','Aqua','Coral']
    mouse = event.Mouse()
    
    circle = visual.Circle(win, size=0.1, fillColor=random.choice(colorOptions),lineColor=random.choice(colorOptions),interpolate=False)
    rect = visual.Rect(win,width=0.1,height=0.1,fillColor=random.choice(colorOptions),lineColor=random.choice(colorOptions))
    triangle = visual.ShapeStim(win=win, name='polygon',
        vertices=[[-(0.1, 0.1)[0]/2.0,-(0.1, 0.1)[1]/2.0], [+(0.1, 0.1)[0]/2.0,-(0.1, 0.1)[1]/2.0], [0,(0.1, 0.1)[1]/2.0]],
        ori=0,lineWidth=1, fillColor=random.choice(colorOptions),lineColor=random.choice(colorOptions))
    cross = visual.ShapeStim(win=win, name='polygon_2', vertices='cross', size=(0.1, 0.1), ori=0,
        lineWidth=1, fillColor=random.choice(colorOptions),lineColor=random.choice(colorOptions))
    star = visual.ShapeStim(win=win, name='polygon_3', vertices='star7',size=(0.1, 0.1),ori=0, 
        lineWidth=1, fillColor=random.choice(colorOptions),lineColor=random.choice(colorOptions))
        
    # Create a list to hold all shapes
    shapeOptions = [circle, rect, triangle, cross, star]
    # Shuffle shape options
    random.shuffle(shapeOptions)
    # Iterate over shapes and draw
    i = 0
    xPos = -0.3
    while i < 4:
        shapeOptions[i].pos = (xPos, 0)
        shapeOptions[i].draw(win)
        xPos += 0.2
        i += 1

    win.flip()
    
    waitClick = True
    while waitClick:
        if sum(mouse.getPressed()) > 0:
            waitClick = False
            break
    
    if mouse.isPressedIn(circle):
        chosenShape = circle
        chosenColor = circle.fillColor
    if mouse.isPressedIn(rect):
        chosenShape = rect
        chosenColor = rect.fillColor
    if mouse.isPressedIn(star):
        chosenShape = star
        chosenColor = star.fillColor
    if mouse.isPressedIn(triangle):
        chosenShape = triangle
        chosenColor = triangle.fillColor
    if mouse.isPressedIn(cross):
        chosenShape = cross
        chosenColor = cross.fillColor
        
    win.flip()

    scenario = random.choice([1,2,3])
    if scenario == 1:
        # Scenario 1: change the color of the shape
        colorOptions.remove(chosenShape.fillColor)
        chosenShape.fillColor = random.choice(colorOptions)
        chosenShape.pos = [0, 0]
        chosenShape.draw(win)
    elif scenario == 2:
        # Scenario 2: change the shape and maintain the color
        newShape = random.choice(shapeOptions)
        newShape.fillColor = chosenColor
        newShape.pos = [0, 0]
        newShape.draw(win)
    else:
        chosenShape.pos = [0, 0]
        chosenShape.draw(win)
        
    win.flip()
    event.waitKeys(keyList=['t'])
    #response = event.waitKeys(keyList=['t','f','c'])



## Define Experimental Variables ##
expVarOrder = ['latency','avgChoiceTime','circlePositions','response','responseTime','choiceTime','confAnswer','colorOptions', 'centerCircleColor']
expInfo = enterSubInfo('Choice Experiment')
dataFile = makeDataFile(expInfo['Subject'],expInfo['ExpTitle'])

win = visual.Window([1920,1080],color=[-1,-1,-1],fullscr=False,monitor='testMonitor')
ready = visual.TextStim(win,text=u'Ready?',height=.3,color=[1,1,1])
fixation = visual.TextStim(win,text='+',height=.07,color=[1,1,1])
quit = visual.TextStim(win,text='Quit experiment now (y/n)?',height=.1,color=[1,1,1])

confQuestionText = u'On a scale from 1 to 5, how confident you are that this is your choice? (1= Not confident at all; 5= Extremely confident) '
confQuestionVisual = visual.TextStim(win,color='#fdfdfd',wrapWidth=1.2, height=.06,text=confQuestionText)

mouse = event.Mouse(visible=False,win=win)

expClock = core.Clock()
responseClock = core.Clock()
choiceClock = core.Clock()

## Practice Instructions ##
text1 = 'Welcome! The aim of the current experiment is to look at how people choose between simple visual objects, \
not to test specific skills or intellectual abilities.'

text2 = 'First, a plus sign (+) is going to flash in the middle of the screen. \
Then 2 different colored circles will suddenly show up on random spots on the screen. \
As quickly as you can, you will have to choose one of these circles "in your head"  and remember which one you chose. \
There is no right or wrong choice: answer based on your personal preferences (Press any key to continue.)'

showInstructions(text1,text2)

text1 = 'After the circles show up on the screen, a third circle, which matches the color of one of the first two \
will appear in the middle. If this new circle has the same color as the circle \
you chose: press T (TRUE) on your keyboard. \
If it does not have the same color: press F (False).'

text2 = 'Sometimes the third circle will appear extremely quickly, so it is important that you try to \
choose a circle in your head as fast as you can. If the third circle appears so quickly that you did not manage to choose a circle before that, \
press C (Could not Choose). \
(Press any key to continue.)'

showInstructions(text1,text2)

text = 'On some trials, you will be asked How confident are you that this was the circle you chose\
on a scale from 1 to 5 (1=Not confident at all; 5=Extremely confident). \
You may find that you feel very confident on all or most trials, in which case it is perfectly \
acceptable to always answer 5 and vice versa\
Just answer based onyour honest judgment. (Press any key to continue.)'

instruct = visual.TextStim(win, color='#fdfdfd',pos=[0,0],wrapWidth=1.2, height=.06,text=text)
instruct.draw()
win.flip()
event.waitKeys()

text1 = 'Before the beginning of each activity, the word Ready?(press SPACE) will be on the screen. \
Feel free to take breaks if you need to, and wait for the Ready? screen if you want to pause and\
ask questions to the Experimenter.'

text2 = 'You will have the chance to practice the task before the real experiment starts. Whenever you are ready, \
press any key to continue.'


showInstructions(text1,text2)


## Practice Trials ##
reps = 1 #go through each kind of experimental trial once for practice
practiceTrials = generateExperimental()

for trialNum,trial in enumerate(practiceTrials):
    readySequence()
    presentStimuli()
    
## Final Instructions ##
text = 'Now the real experiment will begin. Remember that you can take as many breaks \
as you want and that you should ask the Experimenter if you have any questions. When you are ready, \
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
    #circlePositions,response,responseTime,choiceTime,confAnswer,colorOptions, centerCircleColor = presentStimuli(2,trial['askConf'],trial['latency'])
    addTrialVariables()
    writeToFile(dataFile,trial)

# pyMetronomeGUI
# Original source: https://github.com/unixhead/pyMetronomeGUI

# Beerware license

# Created for messing around with drumming

#sudo apt-get install -y python3-dev libasound2-dev
#pip install dearpygui simpleaudio

import simpleaudio, time


metronomeRunning = False
scheduleMetronomeRunning = False
currentSchedule = 0

metronomeCount = 0
metronomeTimeSig = 4
timerStart = 0
scheduleRows = 0
last = 0

strongBeat = simpleaudio.WaveObject.from_wave_file('strong_beat.wav')
weakBeat = simpleaudio.WaveObject.from_wave_file('weak_beat.wav')


#print any debug info text into console
def debugLog(text):
    print(text)
    

def get_time_ms():
    return int(time.time()*1000)


def startBPM(sender, app_data):
    #debugLog("startBPM:" + str(dpg.get_value("bpmValue")))
    if scheduleMetronomeRunning == True:
        return False
    global metronomeRunning, metronomeCount, metronomeTimeSig, timerStart
    metronomeCount = 0
    metronomeRunning = True
    try:
        metronomeTimeSig = int(dpg.get_value("timeSigValue"))
    except:
        metronomeTimeSig = 4
        dpg.configure_item("timeSigValue", default_value="4")
    # set sig to r/o
    dpg.configure_item("timeSigValue", readonly=True)
    timerStart = get_time_ms()


def stopBPM(sender, app_data):
    #debugLog("stopBPM:" + str(dpg.get_value("bpmValue")))
    global metronomeRunning
    metronomeRunning = False
    dpg.set_value("timerValue", "0") 
    dpg.configure_item("timeSigValue", readonly=False)


def renderCallback():
    return True

def startSchedule():
    #debugLog("StartSchedule")
    if metronomeRunning == True:
        return False
    global scheduleMetronomeRunning, currentSchedule, timerStart, currentTimerStart, metronomeCount
    metronomeCount = 0
    scheduleMetronomeRunning = True
    currentSchedule = 0
    timerStart = get_time_ms()
    currentTimerStart = get_time_ms()


def stopSchedule():
    #debugLog("StopSchedule")
    global scheduleMetronomeRunning, currentSchedule
    scheduleMetronomeRunning = False
    i = 0
    try:
        #blank all "Active" fields and set plain colour
        
        while (i <= scheduleRows):
            dpg.set_value("tableActive"+str(i),"")
            dpg.highlight_table_cell(metro_table_id, i, 3, [0, 0, 0, 0])
            i=i+1
    except:
        #do nowt
        time.sleep(0.001)
        debugLog("failed at " + str(i))
    currentSchedule = 0

def addScheduleRow():
    global scheduleRows
    #debugLog("adding row: " + str(scheduleRows+1))
    scheduleRows = scheduleRows + 1
    rowNum = scheduleRows
    with dpg.table_row(parent="scheduleTable",  tag="tableRow"+str(rowNum)):
        dpg.add_input_text(tag="tableBPM"+str(rowNum), decimal=True, width=40)
        dpg.add_input_text(tag="tableLength"+str(rowNum), decimal=True, width=40)
        dpg.add_input_text(tag="tableSig"+str(rowNum), decimal=True, width=40, default_value=4)
        dpg.add_text("",tag="tableActive"+str(rowNum))
        
    


def delScheduleRow():
    global scheduleRows
    #debugLog("delete rows: " + str(scheduleRows))
    if scheduleRows == 0:
        #debugLog("freturning false")
        return False
    
    dpg.delete_item("tableRow"+str(scheduleRows))
    scheduleRows = scheduleRows - 1
    

last = get_time_ms()

import dearpygui.dearpygui as dpg

dpg.create_context()

# Uses open Sans font from https://github.com/adobe-fonts/source-sans
# License for this font: https://github.com/adobe-fonts/source-sans/blob/release/LICENSE.md
with dpg.font_registry():
    default_font = dpg.add_font("SourceSans3-Regular.otf", 20)


with dpg.theme() as green_bg_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (0, 153, 0), category=dpg.mvThemeCat_Core)

with dpg.window(tag="Primary Window"):
    dpg.bind_font(default_font)


    dpg.add_tab_bar()
    with dpg.collapsing_header(label="Basic Metronome Timer", default_open=True):

        ## metronome
        #  input box to set bpm
        dpg.add_text("BPM:", tag="bpmText")
        dpg.add_input_text( default_value="100",  tag="bpmValue", width=100, indent=50)
        bpmGroup = dpg.add_group(horizontal=True)
        dpg.move_item("bpmText", parent=bpmGroup)
        dpg.move_item("bpmValue", parent=bpmGroup)

        # time signature
        dpg.add_text("Sig:", tag="sigText")
        dpg.add_input_text( default_value="4",  tag="timeSigValue", width=100, indent=50)
        sigGroup = dpg.add_group(horizontal=True)
        dpg.move_item("sigText", parent=sigGroup)
        dpg.move_item("timeSigValue", parent=sigGroup)



        # timer
        dpg.add_text("Timer:", tag="timerText")
        dpg.add_input_text( default_value="0",  tag="timerValue", width=100, indent=50)
        timerGroup = dpg.add_group(horizontal=True)
        dpg.move_item("timerText", parent=timerGroup)
        dpg.move_item("timerValue", parent=timerGroup)


        # start / stop buttons
        dpg.add_button(label="Start", callback=startBPM, tag="startButton")
        dpg.add_button(label="Stop", callback=stopBPM, tag="stopButton")   
        buttonGroup = dpg.add_group(horizontal=True)
        dpg.move_item("startButton", parent=buttonGroup)
        dpg.move_item("stopButton", parent=buttonGroup)


    dpg.add_tab_bar()
    with dpg.collapsing_header(label="Schedule Metronome"):
        with dpg.table(tag="scheduleTable",header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, width=300) as metro_table_id:
            dpg.add_table_column(label="BPM", width=20,  width_fixed=True)
            dpg.add_table_column(label="Length(s)", width=40,  width_fixed=True)
            dpg.add_table_column(label="Signature", width=40,  width_fixed=True)
            dpg.add_table_column(label="Active", width=40,  width_fixed=True)
            
            rowNum = 0
            with dpg.table_row(): 
                dpg.add_input_text(tag="tableBPM"+str(rowNum), decimal=True, width=40)
                dpg.add_input_text(tag="tableLength"+str(rowNum), decimal=True, width=40)
                dpg.add_input_text(tag="tableSig"+str(rowNum), decimal=True, width=40, default_value=4)
                dpg.add_text("",tag="tableActive"+str(rowNum))
                     
        dpg.add_button(label="add row", callback=addScheduleRow,tag="addRowButton")
        dpg.add_button(label="del row", callback=delScheduleRow,tag="delRowButton")
        schedButtonGroup = dpg.add_group(horizontal=True)
        dpg.move_item("addRowButton", parent=schedButtonGroup)
        dpg.move_item("delRowButton", parent=schedButtonGroup)

        # BPM
        dpg.add_text("BPM:", tag="scheduleCurrentBPMText")
        dpg.add_input_text( default_value="0",  tag="scheduleCurrentBPMValue", width=100, indent=50, readonly=True)
        scheduleCurrentBPMGroup = dpg.add_group(horizontal=True)
        dpg.move_item("scheduleCurrentBPMText", parent=scheduleCurrentBPMGroup)
        dpg.move_item("scheduleCurrentBPMValue", parent=scheduleCurrentBPMGroup)


        # timer
        dpg.add_text("Timer:", tag="scheduletimerText")
        dpg.add_input_text( default_value="0",  tag="scheduleTimerValue", width=100, indent=50, readonly=True)
        scheduleTimerGroup = dpg.add_group(horizontal=True)
        dpg.move_item("scheduletimerText", parent=scheduleTimerGroup)
        dpg.move_item("scheduleTimerValue", parent=scheduleTimerGroup)




        # start / stop buttons
        dpg.add_button(label="Start", callback=startSchedule, tag="startScheduleButton")
        dpg.add_button(label="Stop", callback=stopSchedule, tag="stopScheduleButton")   
        buttonScheduleGroup = dpg.add_group(horizontal=True)
        dpg.move_item("startScheduleButton", parent=buttonScheduleGroup)
        dpg.move_item("stopScheduleButton", parent=buttonScheduleGroup)

dpg.create_viewport(title='pyMetronome', height=600, width=300)
 
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)



#
# Main loop
#
while dpg.is_dearpygui_running():

    #simple metronome 
    if metronomeRunning == True:
        try: # try this because if the user is changing the field then it might be empty
            metronomeBPM = int(dpg.get_value("bpmValue"))
            metronomeInterval = int((60/metronomeBPM)*1000)
        except:            
            next

        #debugLog("Metronome running")
        # check if interval has passed
        now = get_time_ms()

        # update timerValue with gap * 1000
        currentTimerValue = int((now - timerStart) / 1000)
        dpg.set_value("timerValue", currentTimerValue)

        gap = now - last
        #debugLog("now:" + str(now))
        if gap > metronomeInterval: # BEEP !
            
            if metronomeCount % metronomeTimeSig == 0:
                #debugLog("Strong beep")
                strongBeat.play()
            else:
                #debugLog("weak beep")
                weakBeat.play()
            #debugLog("beep:" + str(now))
            last = get_time_ms()
            
            metronomeCount = metronomeCount + 1



    #Schedule metronome
    
    if scheduleMetronomeRunning == True:
        #debugLog("current row: " + str(currentSchedule))
        finished = False

        #sort timer
        now = get_time_ms()
      

        #currentSchedule, timerStart
        bpmVal = dpg.get_value("tableBPM"+str(currentSchedule))
        timeVal = dpg.get_value("tableLength"+str(currentSchedule))
        sigVal = dpg.get_value("tableSig"+str(currentSchedule))
        

        # set overall timer
        currentTimerValue = int((now - timerStart) / 1000)

        # set time current schedule is running:
        currentRunTime = int((now - currentTimerStart) / 1000)+1
        dpg.set_value("scheduleTimerValue", str(currentTimerValue))

        try:
            dpg.set_value("tableActive"+str(currentSchedule),str(currentRunTime))
        except:
            stopSchedule()

        if bpmVal == "":
            #print("empty bpm, stopping")
            stopSchedule()
            finished = True

        try:
            scheduleMetronomeInterval = int((60/int(bpmVal))*1000)
            dpg.set_value("scheduleCurrentBPMValue", bpmVal)
            
        except:
            #debugLog("Ran out of lines, ending")
            stopSchedule()
           

        if timeVal == "":
            #debugLog("empty time, stopping")
            stopSchedule()
            

        if sigVal == "": # set sig to default
            sigVal = 4

        gap = now - last
        #debugLog("now:" + str(now))
        if gap > scheduleMetronomeInterval: # BEEP !
            #strongBeat.play()
            try:
                #set active column green
                dpg.highlight_table_cell(metro_table_id, currentSchedule, 3, [0, 150, 0, 100])
                #unset prevoius active column
                if currentSchedule > 0:
                    dpg.highlight_table_cell(metro_table_id, currentSchedule-1, 3, [0, 0, 0, 0])
                    dpg.set_value("tableActive"+str(currentSchedule-1),"")

                if metronomeCount % int(sigVal) == 0:
                    strongBeat.play()
                else:
                    #debugLog("weak beep")
                    weakBeat.play()
                #debugLog("beep:" + str(now))
                last = get_time_ms()
                
                metronomeCount = metronomeCount + 1
            except:
                stopSchedule()
        try:
            if now - currentTimerStart > int(timeVal)*1000:
                currentSchedule = currentSchedule + 1
                currentTimerStart = get_time_ms()
        except:
            stopSchedule()


    dpg.render_dearpygui_frame()

dpg.destroy_context()

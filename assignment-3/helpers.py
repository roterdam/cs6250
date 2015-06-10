#!/usr/bin/python

"Helpers for Assignment 3."
logfile = None

def open_log(filename):
    global logfile
    logfile = open(filename, "w")
    

def write_entry(logstring):
    global logfile
    # Prints out an entry to the log file
   
    logfile.write(logstring + "\n")
    print logstring

def next_entry():
    global logfile
    logfile.write("-----\n")
    print "-----"

def finish_log():
    global logfile
    logfile.close()



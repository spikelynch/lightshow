# Lightshow

A quick frequency-spectrum analyser for Holiday programmable LED lights, or the command line, or anything else you care to add.

Uses the PyAudio package to read data from an audio input, and runs numpy's
FFT to generate frequency spectrum data, which it then sends to an object
implementing a method render().

This package includes two renderers:

* AsciiSpectrum writes an ascii-art spectrum to the command line as a debugging aid
* HolidaySpectrum sends colours to a set of Holiday lights over your wifi

## How to run it

./lightshow.py -i INPUT -l LIGHTS -m MODE -g GRADIENTS -d DECAY -s SCALE -a

INPUT is the index number of the input channel. I use a USB audio
adaptor on my Pi which shows up as index # 2, but it may not be the
same on whatever device you use. I've included a script called
devices.py which scans all the audio devices with PyAudio and dumps
them out with their index numbers to help find it

LIGHTS is the  IP address of your Holiday lights

MODE is the visualisation mode, either 'levels', 'spectrum' or 'wave'.

In the first two modes, each light represents a frequency level. 
In 'spectrum' mode a light's colour depends on its frequency
and the brightness varies with the level of that frequency. In
'levels' mode, both the brightness and the colour of each light vary
with its level. Both of these modes map the left channel on one side of
the lights and the right channel on the other, mirrored down the middle.

In 'wave' mode, there's no frequency analysis, the audio signal is used
as the basis for a chaser display.

GRADIENTS is an optional flag which lets you set a JSON file
controlling the colour gradients. There's a default provided,
gradients.json, which you can have a look at if you want to customise it.

DECAY lets you smooth out the visualisation by making lights decay
exponentially from a peak value, instead of just going dark. It's a
value between 0 and 1: the larger, the slower and smoother. Values
from 0.2 to 0.5 look good to me. If you leave it off, it's equivalent
to DECAY = 0 (ie a light goes dark as soon as its level drops)

SCALE is a scaling factor, because the code isn't smart enough yet to
adjust itself to the input levels. Higher values of SCALE will tell it
to expect louder input: set it to lower levels if you're playing some
quiet stuff and can't see anything.

The -a flag sends an ASCII-art visualisation of the spectrum to the
command line: it's useful for debugging if you haven't got the lights
working yet.  It looks like this:


                  .  ..++=..  .                   
                    ::-:......                    
                   ...:-@%:...                    
                      =:=::-                      
                    ..=-+@:-                      
                      :: .::                      
                      ..@@-:                      
                      :.#-:-                      
                     .::@#.:.                     
                    ...-@....                     
                       .=@:                       
            .....   . . #%.      .. ..            
            ..  .      :-+:. :. .  ..             
                   ...   =  .. .                  
                     ..-*::...  .                 
                  .  ..==#:...                    
                    .. ::=.:                      
                 . ..:+-   :.                     
                     .  -+. :                     
                     :..+  :: .                   
                     .:-@+.:.                     
                     .---=.:                      
                    .:..@# ..                     
                ..    ::= :-... .                 
                      :.#+..                      
                      ..#@.                       
                     ..::: .                      
             ..: .. . ..=@:.....  ...             
               .    . ::==.. :..                  
                . .:..-::::= ..                   
              ..     -. ..:::....  .   .          
                  . . :=:-.:.                     
                       .@@:                       
      .               ..*# .               .      
                       .+.-.  .   .               
               .   :.  :@*. .:-.                  
                .  . ..:+#: .....                 
                . :  -. .=.. . :: .               
                  .  . .--::  .   .               
                   ...:-:@:-.. . .                
                      ::-*-=                 


## Installation

The dependencies are:

* PyAudio
* NumPy

I run the code on my Raspberry Pi and installed the dependencies using
the Raspbian packages python-pyaudio and python-numpy. I've put a
setup.py in this repo with the dependencies, but haven't tested it
yet.

# To Do

Better error handling: sometimes it freezes because the visualiser
can't keep up with the audio input

Automatic scaling to the input signals

Detect pauses between songs - could switch between gradients here


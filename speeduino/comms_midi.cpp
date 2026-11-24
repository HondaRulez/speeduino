/*
 Converts bettween the MIDI packet and serial stream.
 MIDI packets are 4 bytres and the data bytes are 7bit only.

 so we need additional framiong to send/receive 8bit stream.

 Author:
    Ferenc Mikula, fmiku@hondarulez.com, Aka HondaRulez

*/

#include "globals.h"
#include "comms_midi.h"

#if CFG_TUD_MIDI > 0
Adafruit_USBD_MIDI usb_midi;
#endif





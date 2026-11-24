List of changes by me.

Signature changed to 'speeduino 202504-vetuner'

Branch: feat/Embended.INI

 Allow to read the .INI file directly from the device.
 The .INI file stored in the FLASH as compressed .zst file (included by ASM .incbin from references/speeduino.ini.z
st)
 (compressed by 'zstd -19 speeduini.ini' command automatically by the build environment)

 Currently enabled fo STM32 F4xxxE devices, but probably OK for all where the FLASH size allowed.
 see platformio.ini to enable for more devices by add ${env:embended_ini.build_flags} to the 'build_flags' section.

 Changed functions:
    sendBufferAndCrcNonBlocking(const byte *buffer, size_t start, size_t length):
        This modified to calculate the CRC in small chunks (as the serial port drains the data).
        This is needed to prevent a huge stall in the main loop when sending huge amount of data.

    static void sendSerialPayloadNonBlocking(size_t payloadLength, bool flash=false);
        got an optional parameter to tell the sender() func the data is in the FLASH.
        In this case the start address of the data placed into the serialPayload[0] buffer.
        (No any copy made), so before call this function place the address there.
        i.e:
            writeU32(serialPayload, 0, static_cast<uint32_t>(reinterpret_cast<uintptr_t>(_ini_bin_start)));
            sendSerialPayloadNonBlocking(_ini_bin_end - _ini_bin_start, true);

     Host side command to read:  '@', (implemented as leagcy command, like as 'F' always available)
     Reply: <size of the payload (.INI content) in 32 bit BIGENDIAN> <payload> <32 bit CRC>


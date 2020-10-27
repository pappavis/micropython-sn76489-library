import machine
import utime
import ustruct


# 0.01 20201027  nog niet werkend versie. This code doesnt work, not yet.

# ref https:#github.com/maxint-rd/mxUnifiedSN76489
class mxUnifiedSN76489:
    def __init__(sel, pUniOut=8, NotWE=7, useMCUpin=False):
        self._pUniOut = pUniOut
        self._nPin_NotWE = NotWE
        self._fUseMCUpin = useMCUpin
        self._OUTPUT = 1
        self._CLK = 4000000/32
        self._FREQ_TABLE = {
            0,
          #1         2         3         4         5         6         7         8         9         10        11        12
          #C         C#        D         D#        E         F         F#        G         G#        A         A#        B
            16.35,   17.32,   18.35,   19.45,   20.60,   21.83,   23.12,   24.50,   25.96,   27.50,   29.14,   30.87,   # Octave 0
            32.70,   34.65,   36.71,   38.89,   41.20,   43.65,   46.25,   49.00,   51.91,   55.00,   58.27,   61.74,   # Octave 1
            65.41,   69.30,   73.42,   77.78,   82.41,   87.31,   92.50,   98.00,   103.83,  110.00,  116.54,  123.47,  # Octave 2
            130.81,  138.59,  146.83,  155.56,  164.81,  174.62,  185.00,  196.00,  207.65,  220.00,  233.08,  246.94,  # Octave 3
            261.63,  277.18,  293.67,  311.13,  329.63,  349.23,  370.00,  392.00,  415.31,  440.00,  466.17,  493.89,  # Octave 4
            523.25,  554.37,  587.33,  622.26,  659.26,  698.46,  739.99,  783.99,  830.61,  880.00,  932.33,  987.77,  # Octave 5
            1046.51, 1108.74, 1174.67, 1244.51, 1318.52, 1396.92, 1479.99, 1567.99, 1661.23, 1760.01, 1864.66, 1975.54, # Octave 6
            2093.02, 2217.47, 2349.33, 2489.03, 2637.03, 2793.84, 2959.97, 3135.98, 3322.45, 3520.02, 3729.33, 3951.09, # Octave 7
        }
        self._begin()


    def _begin(self):
        self.pnMode(self._nPin_NotWE, self._OUTPUT, self._fUseMCUpin)
        self._silenceAllChannels()

    def _putByte(sel, b):   # put byte on expanded pins 0-7
        pass

    def _sendByte(sel, b):
        pass
    
    def _silenceAllChannels(self):
        pass

    def _tone(sel, nFreqVal, nVolume=0, nChannel=0):        # nFreqVal= clock / 32 / freq
        ''' start to play a tone as specified. Use nVolume=15 to stop playing the tone'''
        # nChannel=0-3, 3=noise
        # nVolume=0-15, 0=highest, 15=silence
        self._sendByte(self.SN76489_NIBBLE_TONE(nChannel) | (nFreqVal & 0b1111)) # lowest nibble
        if (nFreqVal > 0b1111):                    # more than one byte needed?
            self._sendByte((nFreqVal >>4))
            nVol = min(nVolume, 15)
            self._sendByte(SN76489_NIBBLE_VOL(nChannel) | nVol)      # vol 15-nVol


    def _digitWrite(sel, nPin, nValue, fUseMCUpin=True):
        pass


    def _pnMode(sel, t1, t2, fUseMCUpin=True):
        pass


    def tone(sel, ftFrequency, nVolume=0, nChannel=0):        # A4=440Hz, standard tuning, volume 0-15, 15 for silence
        freqval=SN76489_CLKDIV32/ftFrequency;
        self._tone(freqval, nVolume, nChannel);
    
    
    def volume(sel, nVolume, nChannel=0):   # set the volume on the specified channel. Use nVolume=15 to stop playing the tone
        nVol = min(nVolume, 15)
        self._sendByte(SN76489_NIBBLE_VOL(nChannel) | nVol)      # vol 15-nVol
    
    
    def noTone(sel, nChannel=0):  # kill sound on specified channel
        self._volume(0x, nChannel)
    

    def beep(sel, nDuration=100):                                  # simple beep sound
        pass
    
    def note(sel, nNote, nDecay):
        ftFreq = pgm_read_float(FREQ_TABLE[nNote+10])
        self._tone(ftFreq)
        if(nDecay > 0):
            for nVol in range(0,  nVol<=15):
                self.volume(nVol)
                self._dela(nDecay)
    
    
    def stop(self):                                            # stop sound on all channels
        pass
    


class SNdefs(mxUnifiedSN76489):
    SN76489_CMD  = 0x8
    SN76489_VOL  = 0x1
    SN76489_TONE = 0x0
    SN76489_CHN0 = 0x0
    SN76489_CHN1 = 0x1
    SN76489_CHN2 = 0x2
    SN76489_CHN3 = 0x3

    SN76489_NIBBLE_VOL = [0,0,0]
    SN76489_NIBBLE_TONE = [0,0,0]

    SN76489_PULSE_WE = 50     # Duration of /WE pulse in micro-seconds. (1ms in example seems way too long)
    SN76489_CLKDIV32 = 125000.0   # clock divided by 32, required to calculate prescaler value for tone

    OPT_SN7648_NOTE  = 0          # Set to 1 to include a note method that uses note-numbers and a frequency table
    
    G_notes = {
      #DEC     HEX     #   NOTE  MIDI  Comments
      4545,  # 0x11C1  0   A0    21    Lowest piano key. (MIDI note 21)
      4290,  # 0x10C2  1   A0#   22
      4050,  # 0xFD2   2   B0    23

      3822,  # 0xEEE   3   C1    24
      3608,  # 0xE18   4   C1#   25
      3405,  # 0xD4D   5   D1    26
      3214,  # 0xC8E   6   D1#   27
      3034,  # 0xBDA   7   E1    28
      2863,  # 0xB2F   8   F1    29
      2703,  # 0xA8F   9   F1#   30
      2551,  # 0x9F7   10  G1    31
      2408,  # 0x968   11  G1#   32
      2273,  # 0x8E1   12  A1    33
      2145,  # 0x861   13  A1#   34
      2025,  # 0x7E9   14  B1    35
     
      1911,  # 0x777   15  C2    36
      1804,  # 0x70C   16  C2#   37
      1703,  # 0x6A7   17  D2    38
      1607,  # 0x647   18  D2#   39
      1517,  # 0x5ED   19  E2    40
      1432,  # 0x598   20  F2    41
      1351,  # 0x547   21  F2#   42
      1276,  # 0x4FC   22  G2    43
      1204,  # 0x4B4   23  G2#   44
      1136,  # 0x470   24  A2    45
      1073,  # 0x431   25  A2#   46
      1012,  # 0x3F4   26  B2    47    LOWEST NOTE AT 4Mhz (?)

      956,   # 0x3BC   27  C3    48
      902,   # 0x386   28  C3#   49
      851,   # 0x353   29  D3    50
      804,   # 0x324   20  D3#   51
      758,   # 0x2F6   31  E3    52
      716,   # 0x2CC   32  F3    53
      676,   # 0x2A4   33  F3#   54
      638,   # 0x27E   34  G3    55
      602,   # 0x25A   35  G3#   56
      568,   # 0x238   36  A3    57
      536,   # 0x218   37  A3#   58
      506,   # 0x1FA   38  B3    59

      478,   # 0x1DE   39  C4    60    MIDDLE C
      451,   # 0x1C3   40  C4#   61
      426,   # 0x1AA   41  D4    62
      402,   # 0x192   42  D4#   63
      379,   # 0x17B   43  E4    64
      358,   # 0x166   44  F4    65
      338,   # 0x152   45  F4#   66
      319,   # 0x13F   46  G4    67
      301,   # 0x12D   47  G4#   68
      284,   # 0x11C   48  A4    69    440hz (standard tuning)
      268,   # 0x10C   49  A4#   70
      253,   # 0xFD    50  B4    71

      239,   # 0xEF    51  C5    72
      225,   # 0xE1    52  C5#   73
      213,   # 0xD5    53  D5    74
      201,   # 0xC9    54  D5#   75
      190,   # 0xBE    55  E5    76
      179,   # 0xB3    56  F5    77
      169,   # 0xA9    57  F5#   78
      159,   # 0x9F    58  G5    79
      150,   # 0x96    59  G5#   80
      142,   # 0x8E    60  A5    81
      134,   # 0x86    61  A5#   82
      127,   # 0x7F    62  B5    83

      119,   # 0x77    63  C6    84
      113,   # 0x71    64  C6#   85
      106,   # 0x6A    65  D6    86
      100,   # 0x64    66  D6#   87
      95,    # 0x5F    67  E6    88
      89,    # 0x59    68  F6    89
      84,    # 0x54    69  F6#   90
      80,    # 0x50    70  G6    91
      75,    # 0x4B    71  G6#   92
      71,    # 0x47    72  A6    93
      67,    # 0x43    73  A6#   94
      63,    # 0x3F    74  B6    95

      60,    # 0x3C    75  C7    96
      56,    # 0x38    76  C7#   97
      53,    # 0x35    77  D7    98 
      50,    # 0x32    78  D7#   99
      47,    # 0x2F    79  E7    100
      45,    # 0x2D    80  F7    101
      42,    # 0x2A    81  F7#   102
      40,    # 0x28    82  G7    103
      38,    # 0x26    83  G7#   104
      36,    # 0x24    84  A7    105
      34,    # 0x22    85  A7#   106
      32,    # 0x20    86  B7    107

      30,    # 0x1E    87  C8    108   Highest piano key.
      28,    # 0x1C    88  C8#   109 
      27,    # 0x1B    89  D8    110
      25,    # 0x19    90  D8#   111
      24,    # 0x18    91  E8    112
      22,    # 0x16    92  F8    113
      21,    # 0x15    93  G8    114
      20,    # 0x14    94  G8#   115
      19,    # 0x13    95  A8    116
      18,    # 0x12    96  A8#   117
      17,    # 0x11    97  B8    118
     
      16,    # 0x10    98  C9    119   HIGHEST NOTE at 4MHz (?)
      15,    # 0xF     99  C8#   120
      14,    # 0xE     100 D8    121
      13,    # 0xD     101 D8#   122
      13,    # 0xD     102 E8    123
      12,    # 0xC     103 F8    124
      11,    # 0xB     104 F8#   125
      11,    # 0xB     105 G8    126
      10,    # 0xA     106 G8#   127   HIGHEST MIDI NOTE
    }

    def __init__(self):        
        self._setNibble()
        

    def _setNibble(self):
        for chan in range(1,3):
            self.SN76489_NIBBLE_VOL[chan] =  ((self.SN76489_CMD | ((chan&0b11)<<1) |self.SN76489_VOL) << 4)
            self.SN76489_NIBBLE_TONE[chan] =  ((self.SN76489_CMD | ((chan&0b11)<<1) |self.SN76489_TONE) << 4)


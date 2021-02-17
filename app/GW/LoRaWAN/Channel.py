
class Channel:
    EU433 = {0:433.175,
             1:433.375,
             2:433.575,
             3:433.775,
             4:433.975,
             5:434.175,
             6:434.375,
             7:434.575,
             8:434.665} # 8:RX2
    EU868 = {0:868.1,
             1:868.3,
             2:868.5,
             3:867.1,
             4:867.3,
             5:867.5,
             6:867.7,
             7:867.9,
             8:869.525} # 8:RX2
    US915 = {0:[902.3, 902.5, 902.7, 902.9, 903.1, 903.3, 903.5, 903.7],
             1:[],
             2:[],
             3:[]}


    def get_freq(region, ch_num, subband=0):
        if region == 'EU433':
            return Channel.EU433[ch_num]
        elif region == 'EU868':
            return Channel.EU868[ch_num]
        elif region == 'US915':
            return Channel.US915[subband][ch_num]


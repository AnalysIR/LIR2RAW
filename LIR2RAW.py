
lirSignal = "LiR: 26 2328 1194 0232 0232 0232 0696 0232 9C28 2328 08CA 0F 18 F2 81 21 1F 25 12 2F 14 34 1F"
# Raw(71): 9000, 4500, 563, 563, 563, 563, 563, 563, 563, 563, 563, 563, 563, 563, 563, 563, 563, 563, 563, 1687, 563, 1687, 563, 1687, 563, 1687, 563, 1687, 563, 1687, 563, 1687, 563, 1687, 563, 563, 563, 1687, 563, 563, 563, 563, 563, 1687, 563, 1687, 563, 1687, 563, 1687, 563, 1687, 563, 563, 563, 1687, 563, 1687, 563, 563, 563, 563, 563, 563, 563, 563, 563, 39976, 9000, 2250, 563


def LIR2RAW(sig):
    sig = sig.upper().replace("LIR:", "").strip()
    # signal now in desired format
    parts = sig.split()  # list now contains all of the elements of the signal

    carrierHz = int(parts[0], 16)
    print(str(carrierHz) + "kHz")
    rawSig = "RAW(): "

    t = 1  # pointer into parts

    marks = [0]*15  # init to all 0s
    spaces = [0]*15  # init to all 0s

    # first build up arrays for mark and space timings
    #
    while (len(parts[t]) == 4):
        idx = int(t/2)
        print("xxx", idx, t)
        marks[idx] = int(parts[t], 16)

        spaces[idx] = int(parts[t+1], 16)
        t = t+2
        # now check if long sigs if value is odd = > add 0x10000. Longer signal lengths are stored in 16 bit value by making them odd - see syntax docs
        if marks[idx] & 1:  # if odd then add longer value
            marks[idx] += 65536
        if spaces[idx] & 1:
            spaces[idx] += 65536

    # now process individual pulses
    pulseTrain = "".join(parts[t:])

    i = 0
    while i < len(pulseTrain):
        if pulseTrain[i] == "F":  # compress pulses
            if i == len(pulseTrain)-1:
                break  # special case for F in last position - ignore as it is a terminator
            i += 1
            p = int(pulseTrain[i], 16)  # pulse to repeat
            i += 1
            cnt = int(pulseTrain[i], 16)  # number of times to repeat pulse

            for j in range(0, cnt):
                rawSig += str(marks[p]) + ", "
                rawSig += str(spaces[p]) + ", "

        else:
            p = int(pulseTrain[i], 16)  # pulse to repeat
            rawSig += str(marks[p]) + ", "
            rawSig += str(spaces[p]) + ", "
            #print(marks[int(pulseTrain[i], 16)], spaces[int(pulseTrain[i], 16)])
        i += 1

    print(marks)
    print(spaces)
    print(pulseTrain)

    return rawSig


result = LIR2RAW(lirSignal)
print(result)

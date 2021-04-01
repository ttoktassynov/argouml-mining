#!python3

# File for the transaction database
sets = open("sets_sim75.txt", "w")

# Analyse the git log file.
with open("all_sim75.log", "r") as logFile:
    idCounter = 0
    idMap = dict()
    nameMap = dict()
    items = list()

    line = logFile.readline()
    while line:
        entries = line.split("\t")
        if entries[0]:
            if entries[0] == "A":
                # Added file, is not allowed to exist already
                id = entries[1].strip()
                assert id not in idMap
                idCounter += 1
                nameMap[idCounter] = [id]
                idMap[id] = idCounter
                idNum = idCounter
                items.append(idNum)
            elif entries[0] == "D":
                # Deleted file, must exist already
                id = entries[1].strip()
                assert id in idMap
                idCounter += 1
                idNum = idMap[id]
                del idMap[id]
                items.append(idNum)
            elif entries[0] == "M":
                # Changed file, must exist already
                id = entries[1].strip()
                assert id in idMap
                idCounter += 1
                idNum = idMap[id]
                items.append(idNum)
            elif entries[0][0] == "R":
                # Renamed file, old must exist already and new is not allowed to exist already.
                oldId = entries[1].strip()
                newId = entries[2].strip()
                assert oldId in idMap
                assert newId not in idMap
                idNum = idMap[oldId]
                del idMap[oldId]
                nameMap[idNum].append(newId)
                idMap[newId] = idNum
                items.append(idNum)
            else:
                # Something else, should be the commit id and message.
                # Write current set and start new set
                sets.write(" ".join(map(str, sorted(items))) + "\n")
                items.clear()
        line = logFile.readline()

    sets.write(" ".join(map(str, sorted(items))) + "\n")
    items.clear()

    # Write the map of numbers to files.
    with open("map.txt", "w") as mapFile:
        for key, value in nameMap.items():
            mapFile.write(f"{key}: {value}\n")

# All done.
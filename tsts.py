state = (("dfghjkl", True, True, True, True ))

for corner in state[1:]:
    if corner is False:
        print(str( False))
print(str(True))

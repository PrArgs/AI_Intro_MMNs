#make sure we don't explore states that will lead to the state we are currently at.
        # chekMuteMove = temp.getSuccessors()
        # if len(chekMuteMove) == 1 and self.__eq__(chekMuteMove[0]):
        #     successors.remove(temp)
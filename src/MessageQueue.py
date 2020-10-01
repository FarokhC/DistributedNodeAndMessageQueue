# A FIFO Message Queue
class MessageQueue:
    queueContents = []
    def printQueueContents(self):
        print("Queue Contents:" + str(self.queueContents))

    def addMessageToEndOfQueue(self, msg):
        self.queueContents.append(msg)

    def popFirstMessageFromQueue(self):
        if(len(self.queueContents) > 0):
            return self.queueContents.pop(0)
        else:
            raise Exception("MessageQueue is empty")

    def getQueueSize(self):
        return len(self.queueContents)
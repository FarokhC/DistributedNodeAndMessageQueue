

class MessageQueue:
    queueContents = []
    def printQueueContents(self):
        print("Queue Contents:" + str(self.queueContents))

    def addMessageToEndOfQueue(self, msg):
        self.queueContents.append(msg)

    def popFirstMessageFromQueue(self):
        return self.queueContents.pop(0)
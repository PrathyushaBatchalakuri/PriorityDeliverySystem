class treeNode:
    def __init__(self, orderId, currentSystemTime, orderValue, deliveryTime, ETA, priority):
        self.id = orderId
        self.createTime = currentSystemTime
        self.value = orderValue
        self.deliveryTime = deliveryTime
        self.eta = ETA
        self.priority = priority

        # Tree structure properties
        self.leftChild = None
        self.rightChild = None
        self.parent = None
        self.height = 1

    def updateHeight(self):
        leftHeight = 0 if not self.leftChild else self.leftChild.height
        rightHeight = 0 if not self.rightChild else self.rightChild.height
        self.height = max(leftHeight, rightHeight) + 1


class avlTree:
    def __init__(self):
        self.root = None

    def insert(self, curr, node):
        if not curr:  # Base case: If current node is None, insert here
            return node

        if node.priority > curr.priority:
            curr.rightChild = self.insert(curr.rightChild, node)
            curr.rightChild.parent = curr  # Ensure parent is set correctly
        else:
            curr.leftChild = self.insert(curr.leftChild, node)
            curr.leftChild.parent = curr  # Ensure parent is set correctly

        curr.updateHeight()
        return self.balanceTree(curr)


    def delete(self, curr, key, id):
        if not curr:
            return None
        if curr.id == id:
            if not curr.leftChild or not curr.rightChild:
                return curr.leftChild or curr.rightChild
            successor = self.getMin(curr.rightChild)
            curr.id, curr.priority = successor.id, successor.priority
            curr.rightChild = self.delete(curr.rightChild, successor.priority, successor.id)
        elif key > curr.priority:
            curr.rightChild = self.delete(curr.rightChild, key, id)
        else:
            curr.leftChild = self.delete(curr.leftChild, key, id)
        curr.updateHeight()
        return self.balanceTree(curr)

    def _deleteNode(self, node):
        parent = node.parent
        if not node.leftChild:
            self._replaceNodeInParent(node, node.rightChild)
        elif not node.rightChild:
            self._replaceNodeInParent(node, node.leftChild)
        else:
            successor = self.getMin(node.rightChild)
            node.id, node.priority = successor.id, successor.priority
            self.delete(successor, successor.priority, successor.id)

    def _replaceNodeInParent(self, node, newNode):
        if node.parent:
            if node == node.parent.leftChild:
                node.parent.leftChild = newNode
            else:
                node.parent.rightChild = newNode
        else:
            self.root = newNode
        if newNode:
            newNode.parent = node.parent

    def balanceTree(self, node):
        bf = self.getBf(node)

        if bf > 1:  # Left heavy
            if self.getBf(node.leftChild) < 0:
                node.leftChild = self.lRotate(node.leftChild)
            return self.rRotate(node)

        if bf < -1:  # Right heavy
            if self.getBf(node.rightChild) > 0:
                node.rightChild = self.rRotate(node.rightChild)
            return self.lRotate(node)

        return node  # No imbalance, return node as is


    def lRotate(self, A):
        B = A.rightChild
        A.rightChild = B.leftChild
        if B.leftChild:
            B.leftChild.parent = A
        B.leftChild = A
        A.updateHeight()
        B.updateHeight()
        return B

    def rRotate(self, A):
        B = A.leftChild
        A.leftChild = B.rightChild
        if B.rightChild:
            B.rightChild.parent = A
        B.rightChild = A
        A.updateHeight()
        B.updateHeight()
        return B

    def rlRotate(self, A):
        self.lRotate(A.rightChild)
        self.rRotate(A)

    def lrRotate(self, A):
        self.rRotate(A.leftChild)
        self.lRotate(A)

    def _rotate(self, A, B):
        parent = A.parent
        A.parent, B.parent = B, parent
        if parent:
            if parent.leftChild == A:
                parent.leftChild = B
            else:
                parent.rightChild = B
        if B.leftChild:
            B.leftChild.parent = A
        A.rightChild = B.leftChild
        B.leftChild = A
        A.updateHeight()
        B.updateHeight()
        if parent is None:
            self.root = B

    @staticmethod
    def getBf(node):
        leftHeight = 0 if not node.leftChild else node.leftChild.height
        rightHeight = 0 if not node.rightChild else node.rightChild.height
        return leftHeight - rightHeight

    @staticmethod
    def getMin(node):
        while node.leftChild:
            node = node.leftChild
        return node


myTree = avlTree()
nodes = {}  # {orderId: node}
orders = {
    "eta": [],
    "priority": [],
    "ID": [],
    "deliveryTime": [],
    "deliveryStatus": [],
}
lastReturnTime = 0
currentOrderSize = 0

def getPriority(orderValue, createTime, valueWeight=0.3, timeWeight=0.7):
    return valueWeight * orderValue / 50 - timeWeight * createTime


def createOrder(orderId, currentSystemTime, orderValue, deliveryTime):
    global orders, nodes, currentOrderSize, lastReturnTime

    timestamp = max(currentSystemTime, lastReturnTime)
    priority = getPriority(orderValue, currentSystemTime)

    insertRank = currentOrderSize
    for i in range(currentOrderSize):
        if priority > orders["priority"][i]:
            insertRank = i
            break

    if insertRank == 0:
        orderETA = timestamp + deliveryTime
    else:
        prevEndTime = orders["eta"][insertRank - 1] + orders["deliveryTime"][insertRank - 1]
        orderETA = max(timestamp, prevEndTime) + deliveryTime

    orders["ID"].insert(insertRank, orderId)
    orders["eta"].insert(insertRank, orderETA)
    orders["priority"].insert(insertRank, priority)
    orders["deliveryTime"].insert(insertRank, deliveryTime)
    orders["deliveryStatus"].insert(insertRank, 0)

    newOrderNode = treeNode(orderId, currentSystemTime, orderValue, deliveryTime, orderETA, priority)
    myTree.insert(myTree.root, newOrderNode)
    nodes[orderId] = newOrderNode

    currentOrderSize += 1
    return f"Order {orderId} created with ETA {orderETA}\n"


def cancelOrder(orderId, currentSystemTime):
    if orderId not in nodes:
        return f"Order {orderId} not found.\n"

    orderIdx = orders["ID"].index(orderId)
    for key in orders.keys():
        orders[key].pop(orderIdx)

    myTree.delete(myTree.root, nodes[orderId].priority, orderId)
    del nodes[orderId]

    global currentOrderSize
    currentOrderSize -= 1
    return f"Order {orderId} canceled.\n"


def printByOrder(orderId):
    if orderId not in nodes:
        return f"Order {orderId} not found.\n"
    node = nodes[orderId]
    return f"[{node.id}, {node.createTime}, {node.value}, {node.deliveryTime}, {node.eta}]\n"

def printByTime(time1, time2):
    result = []
    for i in range(currentOrderSize):
        if time1 <= orders["eta"][i] <= time2:
            result.append(str(orders["ID"][i]))

    if result:
        return "[" + ", ".join(result) + "]\n"
    else:
        return "There are no orders in that time period.\n"
    
def getRankOfOrder(orderId):
    if orderId not in orders["ID"]:
        return f"Order {orderId} not found.\n"
    
    rank = orders["ID"].index(orderId)
    return f"Order {orderId} will be delivered after {rank} orders.\n"

def updateTime(orderId, currentSystemTime, newDeliveryTime):
    if orderId not in nodes:
        return f"Order {orderId} not found.\n"

    orderIdx = orders["ID"].index(orderId)
    oldDeliveryTime = orders["deliveryTime"][orderIdx]
    offset = newDeliveryTime - oldDeliveryTime

    # Update delivery time and ETA in both lists and the tree node
    orders["deliveryTime"][orderIdx] = newDeliveryTime
    orders["eta"][orderIdx] += offset

    nodes[orderId].deliveryTime = newDeliveryTime
    nodes[orderId].eta += offset

    # Adjust ETAs of subsequent orders if needed
    prevEndTime = orders["eta"][orderIdx] + newDeliveryTime
    updatedOrders = {}
    for i in range(orderIdx + 1, currentOrderSize):
        currStartTime = orders["eta"][i] - orders["deliveryTime"][i]
        if currStartTime < prevEndTime:
            adjustment = prevEndTime - currStartTime
            orders["eta"][i] += adjustment
            nodes[orders["ID"][i]].eta += adjustment
            updatedOrders[orders["ID"][i]] = orders["eta"][i]
        prevEndTime = orders["eta"][i] + orders["deliveryTime"][i]

    # Output updated orders and their ETAs
    if updatedOrders:
        updatedStr = ", ".join(f"{id}: {eta}" for id, eta in updatedOrders.items())
        return f"Updated ETAs: [{updatedStr}]\n"
    
    return f"Order {orderId} has been updated with new delivery time {newDeliveryTime}.\n"

def printByTime(time1, time2):
    result = [str(orders["ID"][i]) for i in range(currentOrderSize) if time1 <= orders["eta"][i] <= time2]
    if result:
        return "[" + ", ".join(result) + "]\n"
    else:
        return "There are no orders in that time period.\n"


def processCommand(cmd):
    cmd = cmd.strip().split('(')
    cmdType = cmd[0]
    argStr = cmd[1][:-1]
    args = [arg.strip() for arg in argStr.split(',')]

    if cmdType == "createOrder":
        return createOrder(*map(int, args))
    elif cmdType == "cancelOrder":
        return cancelOrder(int(args[0]), int(args[1]))
    elif cmdType == "print" and len(args) == 2:
        return printByTime(int(args[0]), int(args[1]))
    elif cmdType == "print" and len(args) == 1:
        return printByOrder(int(args[0]))
    elif cmdType == "getRankOfOrder":
        return getRankOfOrder(int(args[0]))
    else:
        return "Invalid command.\n"




if __name__ == "__main__":
    import sys

    inputFile = sys.argv[1]
    fileName = inputFile[:-4]
    outputStr = ""

    with open(inputFile, 'r') as f:
        cmd = f.readline()
        while not cmd.startswith("Quit()"):
            outputStr += processCommand(cmd.strip())
            cmd = f.readline()

    with open(f"{fileName}_output_file.txt", 'w') as f:
        f.writelines(outputStr)
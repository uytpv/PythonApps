def main():
    global Filename
    print("Program starting.")
    print("This program can analyse list of names.")
    Filename = input("Insert filename: ")
    print("Reading and analysing file '"+Filename+"'.")
    read()
    analysis()


def read():
    global amount
    global shortestName
    global longestName
    global totalLengh
    fileHandle = open(Filename, 'r', encoding="UTF-8")

    # get Amount
    content = fileHandle.readlines()
    amount = len(content)

    # get Max Min
    shortestName = float('inf')
    longestName = 0
    totalLengh = 0
    for line in content:
        if (len(line) > longestName):
            longestName = len(line)-1  # newline character
        if (len(line) < shortestName):
            shortestName = len(line)-1  # newline character
        
        # get average: thay vì tính trung bình thì lấy số tổng thôi rồi hiển thị kết quả lúc in
        totalLengh += len(line)
    


def analysis():
    print("Analysis complete.")
    print("#### REPORT BEGIN ####")
    print("Amount of names: ", amount)
    print("longestName: ", longestName)
    print("shortestName: ", shortestName)
    print("average: ", totalLengh/amount)


main()

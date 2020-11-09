######################################################################
########################## STEGOSAURUS ###############################
######################################################################
# A steganography program written by James Welsh and Donagh Marnane. #
######################################################################


"""
Lets the user choose between decoding or encoding of an image.
Takes no arguemnts and calls the appropriate function or breaks 
the running loop depending on the answer.
"""
def run():
    answer = input(
        "~~~~~~~~~~~~~~~~~~~~~~\n" +
        "Welcome to STEGOSAURUS\n" +
        "~~~~~~~~~~~~~~~~~~~~~~\n" +
        "To encode a message, type 'e'.\n" +
        "To decode an image, type 'd'.\n" +
        "To quit at any time, type 'q'.\n\n" +
        "Please remember to hit the Enter key after your input.\n"
    )

    activeSession = True

    while activeSession:
        userChoice = sanitiseInput(answer)
        
        if userChoice == "q":
            quit()
        
        elif userChoice == "d":
            decode()
            activeSession = False
        
        elif userChoice == "e":
            encode()
            activeSession = False
        
        else:
            answer = input("Please enter only 'e', 'd' or 'q':\n")


"""
Lets the user select a name for the output image and writes all the new data to
that image.
Takes no arguments and returns nothing.
"""
def encode():
    while True:
        imageByteArray = getImageBinary()
        
        outputName = input(
            "Please name your output image.\n" +
            "This should be different from the original.\n")
        
        outputNameCheck = sanitiseInput(outputName)
        
        if outputNameCheck == 'q':
            quit()
        
        if outputNameCheck[-4:] != ".bmp":
            outputName += ".bmp"

        if outputName == inputImageName:
            print("Please do not use the name of the original image.")
            continue
                
        messageString = getMessageString()

        if not enoughStorage(imageByteArray, messageString):
            print("Image too small or message too long. Please try again.\n")
            continue
        
        break

    messageBits = messageAsBits(messageString)
    length = lengthOfPayload(messageBits)

    headerPart = getHeader(imageByteArray)
    bitsToRead = addMessageLengthToImage(imageByteArray, length)
    payload = addMessageToImage(imageByteArray, messageBits)
    rest = addRestOfImage(imageByteArray, messageBits)

    output = headerPart + bitsToRead + payload + rest

    with open(outputName, "wb") as outputImage:
        outputImage.write(output)
    
    print("Your image has been saved in the same directory as this program.\n")


"""
Retrives text hidden in a .bmp image by this program. 
"""
def decode():
    imageByteArray = getImageBinary()
    messageLength = getSecretMessageLength(imageByteArray)
    messageString = getSecretMessage(imageByteArray, messageLength)

    while True:
        ans = input(
            "Your decoded message is ready. Would you like\n" +
            "to view it now, or save it to a .txt file?\n" +
            "Please type 'v' to view, or 't' for a .txt file.\n"
        )
        
        ans = sanitiseInput(ans)

        if ans == "q":
            quit()
        
        elif ans == "v":
            print("Decoded message:\n\n" + messageString + "\n\n")
            break
        
        elif ans == "t":
            with open("decodedMessage.txt", "w") as decodedTextFile:
                decodedTextFile.write(messageString)
            print("Your message has been saved in the same directory as this program.\n\n")
            break
        
        else:
            print("Invalid entry. Please try again.\n")


"""
Allows the user to choose a .bmp file to hide their secret message in.
Take no arguments and returns the image as a bytearray object.
"""
def getImageBinary():
    global inputImageName   
    filePath = input("Please enter the full path to your .bmp file:\n")
    inputImageName = filePath

    # Default value for valid path is false
    validPath = False 

    if sanitiseInput(filePath) == 'q':
        quit()

    while True:
        try:
            with open(filePath, "rb") as imageFile:
                # The image has to be read as a byte array to allow modification
                imageByteArray = bytearray(imageFile.read()) 
                # As this is a valid path set validPath to true
                validPath = True 
                filePath = sanitiseInput(filePath)
                
                # Check file has .bmp extension
                if validPath and (filePath[-4:]) == ".bmp": 
                    print("image found :)\n")
                    return imageByteArray
                
                # If path was valid but file does not have the bmp extension
                elif validPath: 
                    filePath = input(
                        "Path entered does not lead to a bitmap file.\n" +
                        "Please provide a path to a bitmap:\n"
                        )
        
        except FileNotFoundError:
            filePath = input(
                    "No file found. Please enter the correct path with the extension:\n"
                )


"""
Retreives the hidden message from the imageByteArray.
Takes the imageByteArray as an argument, and the number of bytes to read and
returns the hidden message as a string.
"""
def getSecretMessage(imageByteArray, length):
    secretSlice = imageByteArray[86:(86 + length)] #Slice containing the string
    arrayOfChars = []
    noOfChars = int(length / 8)
    count = 0

    for i in range(noOfChars):
        newChar = ""

        for j in range(8):
            #Append the LSB for each byte read to the string representing the
            #eight bit extended ASCII value.
            newChar += (bin(secretSlice[count+j]))[-1]
        
        #Convert the string representing the 8bit binary value to decimal
        arrayOfChars += [int(newChar, 2)]
        count += 8 #Move to next byte

    secretMessage = ""

    for char in arrayOfChars:
        #Append the character represented by the ASCII value to the string
        secretMessage += chr(char)

    return secretMessage


"""
Retrieves the secret message from the user, typed into the terminal.
Takes no arguments and returns a string.
"""
def getStringFromTerminal():
        
    while True:
        answer =  input("Please type your message, followed by Enter:\n")

        if len(answer) == 0:
            check = input(
                "You have not entered any text.\n" +
                "Type 'c' to continue or 't' to type a new message:\n"
            )
            
            check = sanitiseInput(check)
            
            if check == 'q':
                quit()
            
            elif check == 'c':
                return answer
            
            elif check == 't':
                continue
            
            else:
                print("Invalid answer. Please try again.")
        else:
            return answer


"""
Retrieves the string from the user that they wish to hide within the image.
Either by importing a .txt file or by typing a string in the command line.
Takes no arguments and returns a string.
"""
def getMessageString():
    
    # Check if the user would like to type a string or use a text file.
    while True:
        fileOrType = input(
                "\nWould you like to encode a text file or type the message to be encoded?\n" +
                "Please type 'f' for a .txt file, or 't' to type your own, follwed by Enter.\n"
            )
        fileOrType = sanitiseInput(fileOrType)

        if fileOrType == "q":
            quit()
        
        elif fileOrType == "t":
            # Return whatever the user types
            return getStringFromTerminal()
        
        elif fileOrType == "f":
            # Open the referenced text file and return the contents
            while True:
                messageFile = input("Please enter the full path to your text file, followed by Enter:\n")
                if sanitiseInput(messageFile)[-4:] != ".txt":
                    print(
                        "File referenced is not a .txt file, or the extension is missing.\n" +
                        "Please try again.\n"
                    )
                else:
                    break
                    
            with open(messageFile, 'r') as message:
                messageString = message.read()
                return messageString
        
        else:
            print(
                "Invalid entry.\n" + 
                "~~~~~~~~~~~~~~~~~~~~~~~~"
            )
            continue


"""
Takes a string as an argument and returns that a string of bits in ASCII.
"""
def messageAsBits(messageString):
    # Initalises the string
    bits = "" 

    for char in messageString:
        #Adds the character as a string of 8bits to the 'bits' string
        bits += numToBinary(ord(char), 8)

    return bits


"""
Checks that there is enough space in the image to hide the message, taking into
account the header, space to store the length of the payload and the payload itself.
Takes the image object and the message as aruments and returns a boolean.
"""
def enoughStorage(imageByteArray, messageString):
    # The header is 54 bytes and the length will be stored in the next 32 bytes.
    return (len(imageByteArray) - (54 + 32)) >= (len(messageString) * 8)


"""
Takes the image as an argument and returns its header.
"""
def getHeader(imageByteArray):
    #Return the original Bitmap header
    return imageByteArray[:54]


"""
Returns the number of bits in the payload as a string representation of a 32 bit
integer.
"""
def lengthOfPayload(messageBits):
    messageLength = len(messageBits)
    lengthAsBits = numToBinary(messageLength, 32)

    return lengthAsBits


"""
Adds the secret message length to the image so that when decoding the program
knows how many bytes to read.
Takes the image and the number of bits in the message as arguments and returns
the image slice that will contain the length of the message.
"""
def addMessageLengthToImage(imageByteArray, lengthAsBits):
    prePayloadSlice = imageByteArray[54:86]
    count = 0

    for byte in prePayloadSlice:
        byteAsBinary = numToBinary(byte, 8)
        bitToAdd = lengthAsBits[count]

        #Sets the new byte as the first 7 bits of the old byte plus the bit to hide
        newByte = byteAsBinary[:-1] + bitToAdd

        byteAsInt = int(newByte, 2)

        prePayloadSlice[count] = byteAsInt 
        count += 1

    return prePayloadSlice


"""
Adds the secret message to the image.
Takes the image and the message in binary and returns the slice of
the image containing that data.
"""
def addMessageToImage(imageByteArray, messageAsBits):
    #Slice of the image bytes that will be used to store the string
    payloadSlice = imageByteArray[86:(86 + len(messageAsBits))]
    count = 0
    
    for byte in payloadSlice:
        byteAsBinary = numToBinary(byte, 8)
        bitToAdd = messageAsBits[count]
         
        #Sets the new byte as the first 7 bits of the old byte plus the bit to hide
        newByte = byteAsBinary[:-1] + bitToAdd

        byteAsInt = int(newByte, 2)

        payloadSlice[count] = byteAsInt
        count += 1

    return payloadSlice


"""
Takes the image and the message as bits as the arguments and returns the rest
of the data for the image.
"""
def addRestOfImage(imageByteArray, messageAsBits):
    
    bytesToSkip = 54 + 32 + len(messageAsBits)
    
    return imageByteArray[bytesToSkip:]


"""
Finds the number of bytes to read.
Takes an image byte array as an argument and returns the number of bytes to read
in the secret image as an integer.
"""
def getSecretMessageLength(imageByteArray):
    sizeSlice = imageByteArray[54:86]
    sizeAsBinary = ""
    
    for byte in sizeSlice:
        sizeAsBinary += bin(byte)[-1]

    return int(sizeAsBinary, 2)

'''
Makes sure that user inputs in capitals or with spaces are still recognised.
'''
def sanitiseInput(inputString):
    return inputString.lower().strip()


"""
Returns the first argument in the form of a binary number the length of the second argument.
"""
def numToBinary(num, bitDepth):
    return bin(num).lstrip("0b").zfill(bitDepth)


if __name__ == "__main__":
    while True:
        run()

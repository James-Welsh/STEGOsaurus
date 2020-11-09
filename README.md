# STEGOsaurus

Hello, and welcome to stegosaurus! Within this file we have included everything
that you will need to start hiding secret strings in an image. Included within
this file you will find:

- The program (Main.py)
- Three bitmap images (TeamStego.bmp, Stego.bmp & Tiny.bmp)
- A '.png' image (nGrams.png)
- A text file (Rick.txt)
- This README

To get started with this program first run the Main.py file. You should then have
the options to either encode a message 'e', decode a message 'd' or quit 'q'. We
recommend you first encode a message. You will then be prompted to select an
image to hide the message within. The file contains two already for you to use
'Stego.bmp' and 'TeamStego.bmp'. Tiny.bmp will not give you enough characters to
store a very long string. Don't worry if you accidentally misspell the name of the
file, the program will not allow an incorrect path to be entered and will simply
prompt you to try again. If you accidentally enter a path to a file without the
'.bmp' extension the program will not execute and again you will be prompted to
try entering the file name again.

Once you have chosen the image to encode you now have the option of either typing
your message into the terminal or importing a message stored within a txt file.
If you want to try a .txt file we have provided one, 'Rick.txt', for you to use.
Finally all that's left to do is to select a name for your new image. No need to
add the .bmp extension onto the end of your file name as if you don't the program
will add it for you automatically. We will also not let you name the file the same
as the original image to prevent overwriting that. It doesn't however prevent
overwriting of other files in the directory so be careful!

Once you have a bitmap containing a secret message you can then decode the
message from that bitmap. Enter 'd' to decode and enter the name of the file into
the terminal. Again if you accidentally enter an incorrect path the program will
just prompt you to try again. You should now have received the message that your
secret message was successfully decoded and if you want that to be outputted to
the console 'v' or to a .txt file 'f'. The secret message should now be decoded
and visible.

Many thanks for using stegosaurus,

James Welsh and Donagh Marnane :)

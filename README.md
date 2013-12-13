ABPlayerHTML5-Py--nix 1.02
=====================

A HTML5 solution of comment playing on *nix.

This is another solution of the damn fact that Mac, one of the best OS in human history, does not have a reliable and nice video commit software.

Written in Python, based on ABPlayerHTML5, this is a quick way to enjoy commit(DanMu) on Mac and *nix(To-Do) like systems.

Also check https://github.com/superwbd/Mukioplayer-Py-Mac  , this is the one with flash and MukioplayerPlus.

Download
------
I will upload every version here: https://sourceforge.net/projects/abplayerhtml5pynix/

However, feel free to download here via the ZIP file. I just want to provide you a way to download all the old versions.

Also, when it comes to other *nix systems, SF would be much better than Github...

Usage
------
Download all the files, extract into one folder. Personally I do not suggest you go anywhere above ‘~’, for you would meet all kinds of privilege problems, which I suppose would drive you mad.

Make sure you have a web browser which support HTML5 and <video> as well as MP4 decode.

Make sure you use Python 2.7 (this is provided along with OSX), and run ‘python abp.py’.

After “Vid”, drag in the video file you would like to play. (Update in 1.02: Now you should can use any file thst use H.264 and AAC, mo matter it is FLV or MP4. ABPlayerHTML5-Py-*nix can convert the FLV(MKV should also works, but haven't tested yet)file to MP4, so HTML5 can read it)

For XML, drag in the XML file. Commit files from Bilibili would be OK, which had beed tested, while those from other sites are pending test. Please tell me the test result you have, this would be very helpful, and hereby I thank you in advance for your help. Enter.

For the first you run it, OSX may ask you for approving the connections. Does not matter whether you allow or not.

Now the browser would open by herself, enjoy it!

After you use it, BE SURE to input Ctrl+C in the bash window! Though I have made some improvement to enhance the security, better safe than sorry.

Things you should know
-----
Please do not include anything besides characters or numbers in your folder or filename. There ’s no guarantee that symbols would be cool.
(Update: This should be fixed in version .05. Open an issue if it does not work.)

Make sure you use Python 2.7, 3.3 won’t work for it doesn’t have some important network modules.

This software is not made for playing anything above the folder “~”. Don’t get surprised if it gives you funny results.
(Update: Now it should can play things regardless the original location.)

If somehow the player failed to load, try refreshing the page, for the programme has to copy the original file first before you can visit.

For non-MP4 file, ABPlayerHTML5-Py-*nix will try to convert it to MP4. For most of the FLV files this should be fine, and since I just remux it instead of converting the file, this step should not take very long, while it really depends on your computer and the file length, and would require more space in your hard drive. If it is not functioning properly, just convert the file to MP4 by yourself. Remember to use H.264(AVC) and AAC.

I am completely new to Python and programming, so do please help me to improve this, and I would appreciate it very much.

About me
-----
Beining, CDC of ACI-CFG, 1st year CS student of UT.

Get in touch with me via cnbeining[at]gmail.com  .

Copyleft
-----
A number of opensource codes are used in this little project, especially the main programme, ABPlayerHTML5. 
The website of ABPlayerHTML5 is https://github.com/jabbany/ABPlayerHTML5  , MIT License, author: Jim Chen.
(Copyright (c) 2013 Jim Chen (http://kanoha.org/), under the MIT license.)

The part of web server is from http://yige.org  .

A bindary of FFmpeg (http://www.ffmpeg.org/index.html), used for the video remux feature, is released under the GPL-3.0. 
(FFmpeg version 2.1.1 Copyright (C) 2000-2013 the FFmpeg developers)

This project uses MIT licence. 

Update history
-----

.02: Able to read and remux flv and other files, small change to the webpage.

.01: First version

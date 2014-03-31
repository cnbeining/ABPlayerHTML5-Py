ABPlayerHTML5-Py--nix
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

Make sure you have a web browser which can play Flash.

Make sure you use Python 2.7 (this is provided along with OSX), and run ‘python abp.py’.

After “Vid”, drag in the video file you would like to play. Since 1.02, you should can use any file with H.264 and AAC, as long as ffmpeg can convert it.

For XML, drag in the XML file. Comment files from Bilibili would be OK, which had beed tested, while those from other sites are pending test. Please tell me the test result you have, this would be very helpful, and hereby I thank you in advance for your help. If the video name and the comment filename are the same, just input " '' " in "XML", and it will get the comment by itself. Enter.

For the first you run it, OSX may ask you for approving the connections. Does not matter whether you allow or not.

Now the browser would open by herself, enjoy it!

After you use it, BE SURE to input Ctrl+C in the bash window! Though I have made some improvement to enhance the security, better safe than sorry.

Things you should know
-----
Please do not include anything besides characters or numbers in your folder or filename. There ’s no guarantee that symbols would be cool.
(Update: This should be fixed in version .05. Open an issue if it does not work.)

Only Chrome or Safari will work. Firefox or Opera on *nix cannot read MP4. No why, they just can't.

Make sure you use Python 2.7, 3.3 won’t work for it doesn’t have some important network modules.

This software is not made for playing anything above the folder “~”. Don’t get surprised if it gives you funny results.
(Update: Now it should can play things regardless the original location.)

If you don't have FFmpeg, copy the ffmpeg here to /usr/bin/, or the auto transcode will fail.

If somehow the player failed to load, try refreshing the page, for the programme has to copy the original file first before you can visit.

I am completely new to Python and programming, so do please help me to improve this, and I would appreciate it very much.

About me
-----
Beining, CDC of ACI-CFG, 1st year CS student of UT.

Get in touch with me via cnbeining[at]gmail.com  .

Copyleft
-----
A number of opensource codes are used in this little project, especially the main programme, Mukioplayer. The website of Mukioplayer is https://code.google.com/p/mukioplayer/  ,MIT License.

The part of web server is from http://xiaket.org/  , author:Xia Kai <xiaket@corp.netease.com/xiaket@gmail.com> .

This project uses MIT licence. 

Update history
-----
.05: Fix the problem that if ~/.cache does not exist, it will return a 404. Also fix the version number problem.

.04: Fix Issue #1 in a way, now Chrome and Safari are both good to play with more stable backbone.

.03：Update as the original programme updates, willing to fix the navigation problem. Chrome is having unknown problem, and is pending review. 

.02: Able to convert files by itself.

.01: First version

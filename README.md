ABPlayerHTML5-Py & ABPlayerHTML5-Py-Live
=====================

An HTML5 solution of danmaku playing.

~~This is another solution of the damn fact that Mac, one of the best OS in human history, does not have a reliable and nice video commit software.~~ After 1.5 years, there are some really good options including Biligrab, BiliDan, Danmaku2ASS, etc.

Written in Python, based on ABPlayerHTML5, this is a quick way to enjoy comment(DanMu) on Mac and *nix(To-Do) like systems.

Also check https://github.com/cnbeining/Mukioplayer-Py-Mac  , this is the one with flash and MukioplayerPlus. Probably will not have updates anymore...

Now with live mode! Supports http://live.bilibili.com !

Download
------
~~I will upload every version here: https://sourceforge.net/projects/abplayerhtml5pynix/~~

~~However, feel free to download here via the ZIP file. I just want to provide you a way to download all the old versions.~~

~~Also, when it comes to other *nix systems, SF would be much better than Github...~~

Since Sourceforge is abusing the community's trust, I will stop using SF. Feel free to grab the updates here.

Usage of normal version
------
Download all the files, extract into one folder. Personally I do not suggest you go anywhere above ‘~’, for you would meet all kinds of privilege problems, which I suppose would drive you mad.

Make sure you have a web browser which can play HTML5 videos: Opera does not ships with H.264 decoders, and so does Chromium and old versions of IE. I make no comments to browsers make in Chinese Mainland.

Make sure you use Python 2.7 (this is provided along with OSX), and run ‘python abp.py’.

After “Vid”, drag in the video file you would like to play. ~~Since 1.02, you should can use any file with H.264 and AAC, as long as ffmpeg can convert it.~~ After 1.5 years we should not have a lot of video that does not comes with H.264+AAC. Just make sure you are using one of the following format: MP4(H.264+AAC), WebM(VP9), or, Ogg. 

For XML, drag in the XML file. Danmaku files from Bilibili would be OK, which had beed tested, while ~~those from other sites are pending test~~ more supports depends on upstream updates.. Please tell me the test result you have, this would be very helpful, and hereby I thank you in advance for your help. If the video name and the comment filename are the same, just press ENTER, and it will get the comment by itself. Enter.

OSX will ask you for approving the connections. Does not matter whether you allow or not.

Now the browser would open by herself, enjoy it!

After you use it, BE SURE to input Ctrl+C in the bash window! Although I have made some improvement to enhance the security, better safe than sorry. 

Usage of Live version
------
live.py:

Simplely insert the cid of the room.

You may need to refresh the browser to make it running.

DO NOT FORGET TO PRESS CTRL+C AFTER USAGE, FOR THIS SCRIPT WILL KEEP CACHING CONTENTS UNTIL YOUR HARD DRIVE BLOWS UP! 

Things you should know
-----
~~Please do not include anything besides characters or numbers in your folder or filename. There ’s no guarantee that symbols would be cool.~~ Any filename should work as long Python can takes it.
However, since the ways that video and danmaku files are called are different between Mukioplayer-Py-Mac and this programme, some file/folder name that would work there may fail here.

Make sure you use Python 2.7, 3.3 won’t work for it doesn’t have some important network modules.

This software is not made for playing anything above the folder “~”. Don’t get surprised if it gives you funny results.
(Update: Now it should can play things regardless the original location.)

If somehow the player failed to load, try refreshing the page, for the programme has to copy the original file first before you can visit.

Looking for quick way to download videos and comments from Bilibili under OSX? Try this:http://www.cnbeining.com/?s=Biligrab , or https://github.com/cnbeining/Biligrab  .

About me
-----
Beining, CDC of ACI-CFG, CS student of UToronto.

Get in touch with me via cnbeining[at]gmail.com  , or at http://www.cnbeining.com

Copyleft
-----
A number of opensource codes are used in this little project, especially the main programme, ABPlayerHTML5. The website of ABPlayerHTML5 is https://github.com/jabbany/ABPlayerHTML5 , MIT License, used under authorization of original developer.

As the update of ver .09.9, I am using ABPlayerHTML5-bilibili-ver as wrapper for better looks. The website of ABPlayerHTML5-bilibili-ver is https://github.com/Zhuogu/ABPlayerHTML5-bilibili-ver , MIT License, used under authorization of original developer.

The part of web server is from http://xiaket.org/  , author:Xia Kai <xiaket@corp.netease.com/xiaket@gmail.com> . Used under authorization of original developer.

Special thanks to @TYPCN.

This project uses MIT licence. 

Update history
-----

Live .01: First version.

.09.91: HTTP server enhance, much quicker loadtime - now the only limit is your own browser.

.09.9: Giant update.
- Whole rewrite: merely anything left.
- Now using ABPlayerHTML5-bilibili-ver as wrapper.
- Using symlink to boost the loading speed.
- Update CCL to the latest.
- Better deal with crazy filenames.
- Now should works with any system: Not fully tested yet. So name changed.
- Remove most of the hacks in original code: no more ```os.sys```
- Remove FFMpeg: Looks useless for now. Also boost the speed.

.08.2: Fix #3, use ~ as root.

.08.1: Fix cannot read danmaku in different, due to failed to do tests.

.08: Add full screen support, pull update from upstream, make it possible to read JSON files. *NOT SUPPORTED FOR NOW* 

.07.3:  Merge the upstream update by 02:12 EDT, Jul.1.2014. Change the scale of comment speed. 
		JSON files are currently NOT supported.

.07.2:  Merge the upstream update by 01:17 EDT, May.11.2014. Change the scale of comment speed. Change the font in CSS file for better look under OSX.

.07.1: Merge the upstream update by 15:30 EDT, Apr.27.2014. Stop distributing ffmpeg binary with this programme.

.07: Use raw_input, now you do not need to input " ' "_ before files.

.06: Update from the mainstream, merge all the updates since Dec.15.2013. Also reduce the speed of comments, thanks to @yao.ot's report and pull request #5 of ABPlayerHTML5 : https://github.com/jabbany/ABPlayerHTML5/pull/5   . Redo the Readme.

.05: Fix the problem that if ~/.cache does not exist, it will return a 404. Also fix the version number problem.

.04: Fix Issue #1 in a way, now Chrome and Safari are both good to play with more stable backbone.

.03：Update as the original programme updates, willing to fix the navigation problem. Chrome is having unknown problem, and is pending review. 

.02: Able to convert files by itself.

.01: First version

---
showToc: True
TocOpen: False
draft: False
hidemeta: False
comments: False
disableHLJS: False
disableShare: False
hideSummary: False
searchHidden: True
ShowReadingTime: True
ShowBreadCrumbs: True
ShowPostNavLinks: True
ShowWordCount: True
ShowRssButtonInSectionTermList: True
UseHugoToc: True
title: Bypass Paywalls
date created: October 9th 2024, 11:47 am
date modified: January 17th 2025, 2:13 pm
---

## Introduction

This will show you how to bypass paywalls on news websites.

Here is the [list of supported websites](https://github.com/bpc-clone/bypass-paywalls-firefox-clean?tab=readme-ov-file#list-of-supported-websites) that it works with. I mainly use it for The Age and AFR.

Sometimes these extensions break or get removed, so here are the full links to where the instructions are hosted. I've just shortened these instructions to make them easier to follow:

[Chrome](https://github.com/bpc-clone/bypass-paywalls-chrome-clean)  
[Firefox](https://github.com/bpc-clone/bypass-paywalls-firefox-clean)  
[Mobile](https://gitflic.ru/project/magnolia1234/bypass-paywalls-clean-filters)

## Chrome / Edge / Brave Instructions

1. Download zip file [here](https://gitflic.ru/project/magnolia1234/bpc_uploads/blob/raw?file=bypass-paywalls-chrome-clean-master.zip)
2. Unzip so you have folder: 'bypass-paywalls-chrome-clean-master'
3. Go to Manage Extensions (may look different depending on browser) ![](/blog/images/Pasted%20image%2020241009115121.png)
4. Turn on Developer mode ![](/blog/images/Pasted%20image%2020241009115232.png)
5. Click Load unpacked ![](/blog/images/Pasted%20image%2020241009115507.png)
6. Find the unzipped folder and select that to load ![](/blog/images/Pasted%20image%2020241009115547.png)
7. Once loaded it will automatically open the plugin's setting page. I recommend turning on "Check for update rules at startup". Then just hit save. ![](/blog/images/Pasted%20image%2020241009115756.png)
8. You're done! If you go to a website like afr you'll see it's working because the extension will have a small red 'On' icon next to it. ![](/blog/images/Pasted%20image%2020241009115858.png)

## Firefox Instructions

1. Download file [here](https://gitflic.ru/project/magnolia1234/bpc_uploads/blob/raw?file=bypass_paywalls_clean-latest.xpi)
2. Go to about:addons in the URL bar. Go to Extensions, click the gear icon, and then "Install Add-on From File…" ![](/blog/images/Pasted%20image%2020241009121012.png)
3. Select the xpi file we downloaded earlier. ![](/blog/images/Pasted%20image%2020241009121105.png)
4. Firefox will ask if you want the extension to have permission, click 'Add'.
5. Once loaded it will automatically open the plugin's setting page. I recommend turning on "Check for update rules at startup". Then just hit save. ![](/blog/images/Pasted%20image%2020241009121304.png)
6. You're done! If you go to a website like afr you'll see it's working because the extension will have a small red 'On' icon next to it. ![](/blog/images/Pasted%20image%2020241009121350.png)

## iPhone Safari Instructions (Also Works on iPad and Mac)

This requires the premium version of AdGuard which has various paid plans available. There's a 7 day free trial so you can give this a go and cancel if you don't like it. At the time of writing this there's a monthly plan for \$1.50, yearly for \$8, and a lifetime plan (which I purchased) for \$20 AUD. I consider this very cheap considering how much I've saved on The Age + AFR subscriptions alone. It's also a really good ad blocker.

1. Download [AdGuard — ad blocker&privacy on the App Store](https://apps.apple.com/au/app/adguard-ad-blocker-privacy/id1047223162)
2. Open AdGuard and follow the guide to set it up in iPhone Settings > Apps > Safari > Extensions. If it asks what sites you would like to allow it on I recommend all sites.
3. Go back to AdGuard and open Settings > License to purchase AdGuard Premium or start a free trial.
4. Once purchased go to the Protection screen (second icon, shield with a tick) and turn on Safari protection and Advanced protection.
5. Open Safari protection and click Filters.
6. Enable Custom filters and open it. This is why we needed to purchase AdGuard premium, we would not have access to Custom filters without it.
7. Select Add a filter and a text box will appear. Enter the following URL:  
	<https://gitflic.ru/project/magnolia1234/bypass-paywalls-clean-filters/blob/raw?file=bpc-paywall-filter.txt>
8. Click Add.
9. Exit AdGuard
10. Download [Userscripts on the App Store](https://apps.apple.com/au/app/userscripts/id1463298887) and open it.
11. We need to activate Userscripts as a Safari extension too so head back to iPhone Settings > Apps > Safari > Extensions and turn on Userscripts. If it asks what sites you would like to allow it on I recommend all sites.
12. Go back to Userscripts and click Change Userscripts Directory.
13. I recommend going to iCloud Drive and creating a folder called Userscripts (you can make a new folder by clicking the 3 dots in the top right corner). Open the Userscripts folder you just made and click Open. What we just did was tell the Userscripts app to look inside our iCloud / Userscripts folder for any scripts we want to run on websites. This will make more sense soon.
14. Open Safari on your phone and go to:
	1. [magnolia1234/bypass-paywalls-clean-filters](https://gitflic.ru/project/magnolia1234/bypass-paywalls-clean-filters/blob?file=userscript%2Fbpc.en.user.js&branch=main)
	2. Click the small download icon ![](/blog/images/IMG_1CBFF10679D5-1.jpeg)
	3. Your phone will download the file to your phone. No we need to put this file into the Userscripts folder we created earlier.
15. Get out of Safari and go to the 'Files' app on your phone.
16. Go to the 'Browse' tab. Depending on how your phone is set up you will either find your downloads in 'On My iPhone / Downloads' or in 'iCloud Drive / Downloads'. Have a look in both these locations until you find the 'bpc.en.user.js' file we downloaded. Once you find it hold down your finger on it and select 'Move'. Now navigate to the Userscripts folder we created earlier at 'iCloud Drive / Userscripts' and then select Move.
17. Go back to Safari and let's test it out to make sure it's on. Go to afr.com.
18. Press this puzzle piece icon and select Userscripts. If you can't see Userscripts select Manage Extensions and turn it on. ![](/blog/images/IMG_8077E9B345F4-1.jpeg)
19. A little Userscripts window opens and you should see something like Bypass Paywalls Clean - en with a small JS logo next to it. Make sure this JS logo is lit up, meaning this script is turned on ![](/blog/images/IMG_C0326EBB3939-1.jpeg)
20. Phew! We're done now. Test it all out by trying to open an afr article!

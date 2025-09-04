
---
title: "ASTRA - Autonomous Stabilised Thrust Recovery Ascent"
author: "Manan Sharma (@Manan)"
description: "A basic paraffin powered rocket which goes up, falls down and lands on 4 legs."
created_at: "2025-07-14"
Total hours - 59 hrs
---

14th July, 2025 -
Doing research, I've been researching for about 5-6 hours now and i came to a conclusion - I am going to use hybrid oxidising motor to power my rocket as i can control them and make them work the way I want. I am locking in paraffin wax and n2o chargers for the fuel for now. I am gonna use whipped cream chargers as they suit the requirements here. Other than that I am right now studying how solenoid valves work and how can I effectively use them. Packing up for today - Its 4am.

hours - +4

---
15th July, 2025 -
Did a little more research and finalised everything - the structure and layout of everything including the positioning of the parts etc. now time to search for all the crucial hard to find parts and start with the cad model.

hours - +2

--

Started with Open Rocket - made a basic model of our rocket. Going to complete this tomorrow and simulate some test flights. signing off for today.
hour - +2.5
![Open Rocket](https://hc-cdn.hel1.your-objectstorage.com/s/v3/de23775a91b247666d03ca95c841cff5d8a64bec_screenshot_2025-07-16_at_1.38.09___am.png)
![Open Rocket](https://hc-cdn.hel1.your-objectstorage.com/s/v3/09037c414f543e91b96f8d16f6b7fd9bf22a2389_screenshot_2025-07-16_at_1.38.24___am.png)
hours - +2
---

29th July, 2025 -
Need to speedrun this project in the next 3 days. ran some simulations, things look good.

![Open Rocket](https://hc-cdn.hel1.your-objectstorage.com/s/v3/7d826fa916dcaf980aec910090bad755c58b76bc_screenshot_2025-07-22_at_12.32.55___am.png)
![Open Rocket](https://hc-cdn.hel1.your-objectstorage.com/s/v3/0a9340abd8f7e2090bd551a7236ef5d5b808e048_screenshot_2025-07-22_at_12.33.06___am.png)

hours - +4

---
30th and 31st July, 2025 -
Completed the cad model, with the calculations for Centre of Gravity and everything else. Decided the dimensions of the things like landing legs etc.
hours - +7

--
Also completed the research for the fuel system - the way everything will work and like the flow of the energy. Finalised the chamber design for parrafin wax and no2 chargers and all the other things. Also started working on the flight controller - researched for the parts and found the suitable things which complement each other - rn we are using - 2 lidars on either side, STM32 L052K8U6 as the MCU, MPU6050 as gyro, and BPM280 as the altimeter. Also using a RF module to make the launching system's trigger.
hours - +14

![CAD](https://hc-cdn.hel1.your-objectstorage.com/s/v3/6a278e24489b7209372f84a830f54f0c1b13f5b7_screenshot_2025-07-31_at_8.48.29___pm.png)
![CAD](https://hc-cdn.hel1.your-objectstorage.com/s/v3/05f420220b2e25e54d8cca7f1f3828cd5bdd5a63_screenshot_2025-07-31_at_8.49.23___pm.png)

--
Completed the schematics -
![CAD](https://hc-cdn.hel1.your-objectstorage.com/s/v3/f776903f97898415f5401254f62856af31d764ee_screenshot_2025-08-01_at_3.28.11___am.png)

hours - +5


---

August 1st and August 6th -
well while making this thing - i submitted it for an event but soon i realised that the pcb ive made is quite cooked, i should not use a stm as a first timer. so rn my goal is to remake this whole thing in the coming 3 days and ask for a rereview. lets see - these are the current things.

![CAD](https://hc-cdn.hel1.your-objectstorage.com/s/v3/d353d52df04e1eaece24cce61dbf0e1801a6d75c_screenshot_2025-08-07_at_6.38.21___pm.png)
![CAD](https://hc-cdn.hel1.your-objectstorage.com/s/v3/bb7f380423163cb61dbd22e2e2b1c763a285ed61_screenshot_2025-08-07_at_6.38.35___pm.png)

this pcb took around - 17 hrs

---
August 10th -
Remade some of the schematics, gonna complete all tomorrow.

![SCH](https://hc-cdn.hel1.your-objectstorage.com/s/v3/0780474ed24290801a72e58a6966364000a88099_screenshot_2025-08-11_at_2.25.21___pm.png)

hours - +4

---

August 15th -
Continued with the schematics, also had to go through a lot of things which made me go down and wanted to leave on this thing a lot of times, the thing which messed the most was the spark plug thing - the thing is that im using a 7.4V battery and a 5v buck converter to power pico and servos/lidar. But the thing is that i wasn't able to find any spark plug that could work with the 7.4V battery or the 5v buck converter thing. So i just felt like this thing isnt going anywhere as 5v or 7.4v for once is too less for something like this. So I did some more research to find if im able to find something to produce the spark working in the desired voltage, so i kinda gave up on the project as same was gonna happen with the solenoid valve, so i just slept for straight 12 hrs and woke up to do some research for the last time and surprisingly enough i found something, not a typical spark plug but a arc ignitor, i stumbled across it once before but kinda didn't look at it because it just felt too unreliable and I had spark plugs in my mind. So yeah i thought that i'd just use an arc ignitor with a power from pcb power rail and like control using gpio from pico using logic shifters or something if needed but then i realise that the only arc ignitor available here is a breakout with a button to put it up fire, so its like a plasma thing between two closely placed naked wires, so depression came in again, but then i realised that i am getting a bambu a1 mini real soon from shipwrecked so i just decided that i'd make a gear system with a servo motor controlled by the flight controller to press the button to put it up and roll back when it is not supposed to be pressed, so yeah thats it. Now i gotta figure out to use solenoid valves with the voltage limitation as im only finding 24v valves which can actually control the gas etc. and then gotta finalise the fuel system.

![SCH](/assets/SCH1.png)

hours - +7

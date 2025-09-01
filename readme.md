# ASTRA-V

heyo! Manan this side - this is my second big hardware project after my foldable 3d printer - ASTRA-V. Stands for Autonomous Stabilised Thrust Recovery Ascent Vehicle.<br>
![CAD](https://hc-cdn.hel1.your-objectstorage.com/s/v3/6a278e24489b7209372f84a830f54f0c1b13f5b7_screenshot_2025-07-31_at_8.48.29___pm.png)
![CAD](https://hc-cdn.hel1.your-objectstorage.com/s/v3/05f420220b2e25e54d8cca7f1f3828cd5bdd5a63_screenshot_2025-07-31_at_8.49.23___pm.png)
The concept is simple - Go up - attain free fall - thrust again a lil when around 3 feet from the ground - land.

Its using LiDars to calculate the height precisely and they are pretty quick, so no problems.


First iteration -
This very iteration of ASTRA-V has the following tasks - going up 15 feet, attaining a proper stable freefall and then land. Now the word *land* is the main thing, so like this is what the hardest part is - so lets discuss the whole thing step by step.

## Launch
### Trigger
We are using a RF module to trigger the launch, it is in the flight controller.
### Process
The Solenoid Valve will be kicked by the flight controller - which will open the flow of the NO2 in the Parrafin Wax Chamber(We will come to the fuel part later on), and along with the solenoid valve - the spark plug will also be kicked which will burn the fuel. *sshhhhhhhhhhiiiiiiiiuuuuuuuuu* and with that the burnt fuel gases will come out pressurized of the nozzle and *shrrrooooommmm* the rockets up - it will go up 15 feet in this iteration.


## Free fall
Pretty simple, once reached the desired height(15 feet here) the valve will be kicked to close. Thus no oxidiser - thus no thrust and no more going up. Then it will just fall down - tearing down the vigilantly through the air.

## Landing
Now this is the special sauce, the complex thing - in simple words - LiDar sensors are highly sensitive sensors which mainly work on lasers so really quick. They will be sensing the altitude and sending it to the flight computer, now as soon as the altitude or around 3feet (in this case) is reached - the computer will kick up the solenoid and spark plug once again to push enough thrust to neutralise the G force attained in the freefall. So like - the whole rocket will have a gentle bounce in the air using thrusters. Now along with the engine mechanism, one more thing kicked would be the servo motors to deploy the landing legs - they have a really wide span as you can see in the images - so it gonna land really well.


## Flight Controller
Flight controller is a custom made from scratch which uses STM32L052K8U6 as the MCU. It uses MPU-6050 as the Gyro and BMP-280 as the altimeter as its a barometer. It has pins for breakouts of all these things along with connections with landing servos, LiDar sensors, Solenoid valve and the Spark Plug.


## Fuel
It is using Paraffin wax as a fuel along with NO2 as the oxidiser. Pretty simple there is a chamber with granules of paraffin wax and a solenoid opening with NO2 chargers on the other side, I'm using whipped cream chargers for this task, they are pretty good and will come handy in this usecase.
here is the BOM -

## Why am I making this thing?
I love making unconventional things - and i just love space. I always wanted to make a rocket, and but like making something which just goes up and gets on a parachute isn't real gravy. So I decided to make this, its a bit out of the normal model rockets. Thats pretty much it.


| Name | Use case | Price Each (INR) | Units | Total Price (INR) | Total Price (USD) | Link |
|------|----------|------------------|-------|-------------------|-------------------|------|
| Carbon Fibre rods | Landing legs | ₹140 | 2 | ₹280 | 3.2$ | [Think Robotics](https://thinkrobotics.com/products/carbon-fiber-solid-tube-1-m?variant=39329659650134) |
| MG90S servo motors | Landing legs deployment | ₹429 | 4 | ₹1,720 | 20$ | [Think Robotics](https://thinkrobotics.com/products/sg5010-coreless-servo) |
| NO2 Whipped cream chargers | Oxidiser for the fuel | ₹2,800 | 1 | ₹2,800 | 32$ | [Amazon India](https://www.amazon.in/Chargers-Stainless-Laughing-Disposable-Capsules/dp/B07V6BYFWY) |
| Paraffin wax | Main fuel | ₹300 | 5 | ₹1,500 | 17.5$ | [Amazon India](https://www.amazon.in/Fully-Refined-Paraffin-Granules-White/dp/B09C4397P1) |
| Carbon Fibre tube | Main body | ₹4,000 | 1 | ₹4,000 | 46$ | [Think Robotics](https://thinkrobotics.com/products/high-quality-3k-twill-roll-wrapped-carbon-fibre-hollow-round-tube-gloss?variant=45269902721341) |
| LiDar sensor | To measure height quickly | ₹4,000 | 2 | ₹8,000 | 92$ | [Think Robotics](https://thinkrobotics.com/products/ydlidar-gs2-100-30-cm-lidar) |
| BMP280 breakout | To measure height | ₹26 | 2 | ₹52 | 0.7$ | [Think Robotics](https://thinkrobotics.com/products/ydlidar-gs2-100-30-cm-lidar) |
| AMS-1117 | converter breakout for pcb | ₹45 | 2 | ₹90 | 1.5$ | [Think Robotics](https://thinkrobotics.com/products/ydlidar-gs2-100-30-cm-lidar) |
| 4.7K ohm resistor | for pcb | ₹40| 2 | ₹80 | 1$ | [Think Robotics](https://thinkrobotics.com/products/ydlidar-gs2-100-30-cm-lidar) |
| capacitor | To measure height quickly | ₹4,000 | 2 | ₹8,000 | 92$ | [Think Robotics](https://thinkrobotics.com/products/ydlidar-gs2-100-30-cm-lidar) |
(BOM is to be changed as im remaking the pcb)
**Total Project Cost: --- **

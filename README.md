# OOP_Movement_Detection
A Movement Detection Program for Camera

# How it works

Program generates 4 separate windows.
![Screenshot from 2022-07-30 18-14-06](https://user-images.githubusercontent.com/109242797/181925789-8984d4b4-20e7-4e4a-9f52-2e4fba0d9611.png)

Each frame of video is proceed by the program to find a motion.
<ol>
<li>First window is main color window. It shows the Video in color and creates a rectangle on a place where movement is detected.</li>
<li>Second window is gray colored window which is created to proceed frame</li>
<li>Third window is Delta Frame. It shows the diffrence between actual frame and the base frame. If the area of difference exceeds a certain value the area is marked as a new object <-> motion. </li>
<li>Fourth window is a Treshold window to show a diffrence between base and actual frame and measure the area</li>
</ol>

When program starts first frame is considered as base frame. Each next frame is compared with base frame and checks the grey scale color diffrence for each pixel. If diffrence exceed certain value (defined in the program) this pixel is marked. If the pixels side by side creates an area with an area larger than the limit value motion is detected. Method inside class draw a rectangle around the area mentioned before.

# Video Editing Program

This program was created to automate the video editing process for businesses such car dealerships, realtors, or anyone else that just needs to concatenate many clips together. The program has a gui that was created using tkinter. Through this gui, you can select if you want to add an overlay image on top of every video. This overlay will automatically be stretched so that the width matches the dimensions of your video. You can also select whether or not to add music over the video. If music is added, it will be at 25% volume. You can select an intro or outro clip and those will be either added to the beginning or end of every video file. Lastly, you have the ability to select between 1080p and 4k resolution for the output video. These output videos will always be at 24fps.

When selecting what videos to concatenate together, there needs to be a specific directory structure. For example, let's say you have 5 different cars and you take 4 videos of each car. The 4 videos need to be concatenated together so that at the end, you will have 5 videos total: one for each individual car. The following directory structure is needed and you should select the top folder. In the example below, it will be "Cars". The program will output a concatenated video into the directory from which the videos were concatenated.

Cars--
  |
  |
  |--Hyundai
  |        |--video_0.mp4
  |        |--video_1.mp4
  |        |--video_2.mp4
  |        |--video_3.mp4
  |
  |--Jeep
  |     |--video_0.mp4
  |     |--video_1.mp4
  |     |--video_2.mp4
  |     |--video_3.mp4
  |
  |--Ford
  |     |--video_0.mp4
  |     |--video_1.mp4
  |     |--video_2.mp4
  |     |--video_3.mp4
  |
  |--Mazda
  |      |--video_0.mp4
  |      |--video_1.mp4
  |      |--video_2.mp4
  |      |--video_3.mp4
  |
  |--Honda
        |--video_0.mp4
        |--video_1.mp4
        |--video_2.mp4
        |--video_3.mp4
          

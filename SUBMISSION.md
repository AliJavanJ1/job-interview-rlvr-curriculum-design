# Thought process and Curriculum thinking
## Understanding the code
First that I read the whole project docs I was mainly thinking how to understand the code so I tried to read or use an LLM and summarize some parts of the code for me to understand it then after I finished reading the your own sample and taking a look at sdk.py and seed_generator.py I understood that these files alone are what I should care about.

## Basic ideas
Before I start think about the what the each task should specifically be I was thinking how I should think about this problem more generally, I mean that what is important to be exploited while I'm trying to design a curriculum and basically I end up with the following constraints:
- A complete curriculum should cover all possible tools and action available to use
- Also we should cover each section of a drawing for example we we want to add something new to a drawing or when we want to precisely delete some parts or do some transitions on already existing drawings.
- Having use a lot of edge cases inside tasks can learn the model precision
- Focusing on task that ask something implicit is better that directly pointing at the basic materials available in the Excalidraw environment. for example instead of referring to a circle with specific attributes we can put some different shapes together and create something else like a car and ask the model to do something about the car to make the model do more human like tasks
- As deterministic measurability is very important one thing that came to my mind is to put the mode to recreate or work with know mathematically measurable or programable concepts like a simple case is that there is a way to measure Convex shapes collision so we can make some nice tests only relying on that or maybe make the mode to recreate a fractal like structure that can be measured mathematically. I also know some people create beautiful drawing only relaying on certain functions displayed on a cartesian plane maybe we can ask them model do such things with basic elements and then try to use the functions to find the relative coordinates and use some proximation to evaluate it
- Another Idea was to give physical aspects to items like weight and introduce gravity and ask the model to balance something on something else
- One funny thing that came to my mind is to actually put the agent in a situation that it should solve a riddle or a problem to find out about it's task and as we have arrow and connection properties for them I was really thinking about entity relationship diagrams so we could design a simple database question and ask the model to create it's diagram and then only rely on checking the connections to grade it.
- Finally, as I didn't want to put so much time I also thought thing that I'm going to implement now should be enough simple to be developed rapidly but of course I can do much more complicated stuff I'm I'm going to work on the full time

Then I came to the point to actually design some nice simple tasks that are:
- First thing came to my mind was to try the "Draw to shape" capability cause it seems to be tricky to use specially if you want to draw an ellipse or a circle cause humans can do it easily but if you think as doesn't have any edges a computer that relies on strait point to point motions should try to estimate it with a polygon but I came to the problem that only the online version of Ecalidraw currently support draw to shape and the version that we are using locally lacks that capability but my interesting observation was that in the second try after the model made sure the such capability does not exist it instead used "Draw" capability and drawn a polygon consisting of multiple separate strait lines approximating an ellipse. on thing that I understood from this experience is that in future agent should given some way to call smooth movement motions instead of moving from point A to B in a strait line. for example thy can choose between multiple smooth function for this movements and also maybe an exit and enter angle for point A to B so this way they are able to actually draw much better.
- For the second task I wanted to do something with arrows but as I further read the current code I understood that they are not implemented by default and if want to use them I should either write a messy code or change the logic so I passed on that one but still it could be really nice.
- Then for the actual second task I was thinking about a collection of items that can represent a meaningful thing which is made up of simple shapes and many things came to my mind like grapes, apple, a car, a house, snake and even cinema camera and finally I decided to go with snake and ask the model something about the snake tongue which was meant to be made from 3 ellipses.
- For the third task I wanted to make the agent draw something that it's correctness can be measured mathematically first I thought about 3 circle that each two of them have an overlap area and they also have an area that is overlapped by all of them 3 and it came to my mind because of the chart you had in docs but then I thought let's make it even harder, so the 3rd task was to make a silver chain of circles that create a closed loop made of 10 identical circles so the constraint of being circle and same size and also creating a loop can easily measured mathematically
- Then I was thinking about something that push the agent to be very precise so I thought the eraser can be a good thing cause me my self had some problems with using it when I was trying the website and it deletes every thing you touch pretty easy so I decided to create many ellipses that overlap in a very crowded way and then ask the agent to erase the narrowest among them so should be very carful to not touch anything else
- Then finally I wanted a task than is about transitioning already available object in a very precise manner not like your original task and also not with a very obvious target so I decided to make it little bit abstract by using name for the object like ground and base using the text item and then ask the agent to balance the diamond on the base which was a very narrow rectangle.
- I had some more complicated ideas that could consume a lot of time (I also explain them a in the previous section) so I didn't want to investigate them further and some more basic ideas that could be explore for example physic based task that the model was meant to balance two objects on a lever considering mass for those objects and maybe combine it with scaling capabilities (to increase and decrease the mass relatively) but I thought the current amount should be enough for now.
# Generation method, Model capability, failure mode and Results
In this section I go through each task and explain it's special capabilities, how I built it and some changes that I get through and finally how did it perform and where did it fail
## draw-to-shape-ellipse
### Prompt
`Draw an ellipse using "Draw to shape" capability from more options menu with only one try and no further editing (don't mistake it with draw capability).
### Specific Goals and aspects of this task
- drawing a round object while the model can only draw strait lines using the "Draw to shape" capability
- actually force the model to work with "Draw to shape" capability.
### Implementation challenges
regarding the implementation challenges at first I wasn't completely sure if I can tell a shape has drawn using "Drawn to shape" or not but I found out that there is a version property for any element that seemingly shows the number of processes happen to create this item and the thing about draw to shape was that in the Exalidraw system it assumes that Items drawn using that method actually comes into existence very suddenly after the drawing has finished so their version is very low and it's actually exactly 2 and anything drawn using other methods will have a higher version number so I thought that is a good measure and I can actually implement it but then I got into the problem that the local version lacks "Draw to shape" and even later I understood that AI can suddenly jump with the cursor to it's destination and seems every thing it creates would have version number 2 cause the scaling process of it happens instantly not like how humans draw with mouse so we can say this one completely failed.
### Results
One amazing observation during testing the model on this was the Polygon that the model draw with normal Draw tool was pretty much similar to the ellipse that I asked for so I understood that this model very smart so the task should be actually very hard to reach it's limits.
## snake-tounge-color-change
### Prompt
`Change the background color of the snake's tongue to #e03131 (red).`
### Specific Goals and aspects of this task
- force the model to understand a group of elements and meaningful object (here a snake and it's tongue)
- force the model to navigate through a multilevel tools bar to find the input for custom colors and use that
- as the color says red and also provides and specific hex code which actually the value of the one of default stoke colors provided in the panel I wanted to see if the model will fall for this trap and changes the stroke color instead of the background or not
### Implementation challenges
For this task I created a snake out of putting to together ellipses and also it's tongue was a combination 3 ellipses.
Than I exported the project and use the file to do write the `generator.py` and used the same method for other tasks with predefined elements in the `seed.json` 
The challenge was as the number of items grow I couldn't track them down easily and it needed a lot of messy code to check if this ellipses is that one or not and also I couldn't write 4 asserts for each of them and I needed to use a for loop for that.
So I guessed that if I add an irrelevant meta data inside the `seed.json` Excalidraw may just ignore it and I can use it afterward to identify specify elements and that was actually true so I created a meta_label propert through the code to track the items.
Also in order to fix the looping problem as most of the elements were meant to stay the same I simply loaded the `seed.json` into my code and looped on that and used the ids to retrieve the after ward elements through a `get_element_by_id` function that I have added to `sdk.py`.
This way I easily implemented this task and used these methods for the next tasks too.
### Results and failure mode
This task got `3/10` correct and during all of it's fails it forgot to color on specific part of tongue and didn't fall for the color trap at all
Also it was completely capable of going through the tool bars extensively in all of the tries.
## precise-erase
### Prompt
`Erase the narrowest ellipse without touching other itmes using Eraser tool in Excalidraw.`
### Specific Goals and aspects of this task
- Using the eraser in very crowded spot could lead to delete wrong elements as well so this task is meant to measure the precision of the agent
- Also wen throw many element on top of each other an screen shot becomes harder to analyze for the model so finding out an ellipse among others is also another challenge
- Additionally if the agent mistakenly erased something it should try to undo the changes and redo the task and it is also one of the things that this task wants to measure.
### Implementation challenges
Implementation for this task was very straight forward and using the `meta_label` and loading `seed.json` for looping made it very easy to do.
### Results and failure mode
This task got in one run `0/10` (in a headless browser) and in the other run `2/10` (in a visible browser)
I ran it twice cause during the test runs I saw that the agent can actually solve this so I suspected there is something different about this headless mode but I'm not sure about it maybe it's because browser has a different size and in result deferent resolution so the precision task can alter between hard and easy, but I'm not sure about it.
During this task the model only failed because it chosen crowded points to do the erase and didn't tried to undo to fix the problems which supervised me. So definitely we need to learn it how to use undo in other tasks.
## create-silver-chain
### Prompt
`Using Excalidraw, create a closed chain of 10 identical circular ellipses (circles) linked together (by overlapping them) to form a closed circular chain. The ellipses stroke color should be exactly #C0C0C0 (silver).`
### Specific Goals and aspects of this task
- This task focused on creating object from scratch with some specific properties
- challenges were to keep the width and height and color equal not just internally but also among different items and to create a close loop chain which needs some calculation of how to arrange 10 circles to make it a bigger circle
### Implementation challenges
For the implementation I created a function to check overlaps between each two circle and created an adjacency list for each circle.
Then I used that to check the size of the loop and if there is actually any loop crated.
I first wanted to use an algorithm for checking overlaps between ellipses but they were not deterministic an we can say not necessary due to the circle constraint in here.
the rest of the checks for the color and size was done through a loop by comparing the width and height with an average value among them.
### Results and failure mode
This task got `8/10` which is higher than the requirement and showed how skilled the model is in creating something from scratch with specific constraints so harder similar task is necessary.
One time it failed because an outlier among ellipses and the other time because of one missing ellipse.
I also observed that my size different is missing the average size that we expect in it's log which can be added easily.
## balance-diamond-on-base
### Prompt
`Balance the diamond on the base without altering them.`
### Specific Goals and aspects of this task
- This task is mostly about precision but this time regarding a transition which makes it very similar to the original task of the project
- Additionally this task has a very short humanize prompt and that's the agent to understand the meaning
- Also I used text elements to name different elements and used their names inside prompt
### Implementation challenges
This task had a new challenge of getting text property that I added it's function as a property to the `sdk.py`
Also for checking if the diamond is actually on top of base I used some simple calculations but I forgot to report the extent of error when the diamond is not exactly in place inside the error message
### Results and failure mode
This task got `4/10` and the fails weren't because of major mistake instead it was because of minor ones and the fact that the model does not try to fix it's minor problems after the original action.
# Scale Ideas
For scaling this process we can't rely on human made tasks so instead of codding task we should code a task generator.
The first idea that came to my mind was to use real drawings from real expert users of Exaldraw and use reverse engineering so we do 1 or 2 undo at each step and ask an LLM to write a human like prompt for redoing based on two pictures of before and after and then we can create a lot of tasks then we can use a simple platform for human annotator to fast review the tasks and determine good ones, discard bad ones and put aside the ones that can be fixed with some modifications.
Additionally, We can use RLVR to train a small fast RLHF like model to determine how well the agent performed and instead of focusing on verification we can only define the task itself but I'm not quiet sure if we also these kind of projects too.
Finally, one other way to scale up in my mind is to scale up vertically instead of horizontally so we create multi step complicated tasks instead simple small ones like these which in fact can actually be very helpful cause that's how normally people expect from and agent to work.
# Final notes
I should apologize for some bad grammars and miss spellings cause I wanted to absolutely not use any AI model for this.
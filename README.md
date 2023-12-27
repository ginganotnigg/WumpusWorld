- Course: Artificial Intelligence - HCMUS  
- Contributors:
  * [21120040 - Phạm Công Bằng](https://github.com/ginganotnigg)
  * [21120045 - Bùi Hồng Đăng](https://github.com/bhdang311003)
  * [21120182 - Phan Trí Nhân](https://github.com/TreeDude03)
  * [21120413 - Bùi Thiên Bảo](https://github.com/baobui1509)
  * [20120564 - Nguyễn Hoài Sơn](https://github.com/nguyenhoaisonHCMUS)

*********

<h1 align='center'>PROJECT 2 - LOGIC (WUMPUS WORLD)</h1>

## Problem Description
The purpose of this project is to design and implement a logical search agent for a partiallyobservable environment. This will be accomplished by implementing an agent that navigates through the Wumpus World.
In summary, the Wumpus World presents key features:
- A network of interconnected 2D caves.
- Rooms that may harbor deadly pits, signaled by a perceivable breeze.
- Presence of a Wumpus in one of the rooms, detectable through a discernible stench.
- We have one arrow that we can shoot in the direction we are facing.
- A quest for a hidden pot of gold.
- Movement options: forward, backward, left, or right by 90 degrees.
The primary objectives encompass locating the gold and potentially eliminating the Wumpus to ensure success in this environment.
We will modify the Wumpus world as such:
- The world will be limited in (10 x 10) instead of (4 x 4).
    + Room (1, 1) will still be the bottom-left one
    + Room (10, 10) the top-right one.
    + First number is room position in horizontal coordinate.
    + Second number is room position in vertical coordinate.
- Agent can appear in any Room (xa, ya) and always facing to the right. This room is
the only room have the cave door.
- There may be any number of pits and gold in the world.
- There is at least one Wumpus.
- The agent carries an infinite number of arrows.
- The game will end when one of the following three conditions occurs:
    + The agent dies
    + The agent kills all of the Wumpus AND grabs all the gold
    + The agent climbs out of the cave

## User manual
There are 2 modes in our program:
- __Choose__: Run agent on a map that is represented in a file. File must be placed in maps/ folder with format is defined in the project description. User can change selected map by clicking two buttons `<` and `>`.
- __Generate__: Run agent on a random map 10x10 that is generated with custom number of pit, wumpus, gold. User can change the number of pit, wumpus and gold separately by clicking two buttons `<` and `>`.

User can click on button `Choose/Generate` to switch between 2 modes. After customization, click `Start` to launch agent.

<img src="https://github.com/ginganotnigg/WumpusWorld/assets/122675456/8e95bdce-8d0b-4c85-983e-cb0ab5a265b7" width="49%"> <img src="https://github.com/ginganotnigg/WumpusWorld/assets/122675456/3bad00ec-2d60-4225-80b0-a46431cdd0ce" width="49%">

When the game starts, agent will run automatically without stop. Below the map are 2 buttons and score text. If user wants to pause at any step, click `Pause`. User can cancel it by click `Resume`.

![Screenshot 3](https://github.com/ginganotnigg/WumpusWorld/assets/122675456/43fb929f-88ec-465d-a753-4e417edca704)

When the game ends, program will alert user the reason that ends game. User can click `Main Menu` to return to menu.

![Screenshot 4](https://github.com/ginganotnigg/WumpusWorld/assets/122675456/47d0689c-43dd-4ba6-ba0a-f01feb887e2d)

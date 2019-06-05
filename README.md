# networked_battleship
This is a networked battleship game that, instead of being turn based, is not.
Instead, it is a realistic game of battleship where each opponent has 10 ships
and can attack at any time. The win condition is being the first person to hit
the other players 10 ships.

# Setup Instructions
- Ensure Python 3 is installed on your computer
- Ensure PyGame is installed
- Make sure all four files are in the same folder on a system that supports GUIs
- Open 3 command line windows
- In the first window, type: python battleship_server.py
    - Now you have the server running.
- In the second and third windows, type: python battleship_run.py 
    - Now you have two clients running and communicating with the server. 
- Now you are ready to play real-time battleship!

# To Play
- Start by placing 10 ships in the first grid. If you finish placing your ships before you opponent, 
you will have to wait for them to do so. The last ship you set will not be white until they are set.
- Once they do, you can then click on the right grid to attack. 
- There are no taking turns like in civilized warfare, instead, it's whoever destroys the other sides first.
- Good luck!

# Backstory
You are the captain of a fleet of ships in mutiny. Your ships refuse to tell you if they
are alive or not after you give them their initial coordinates. But - you are still determined
to win this war even if it is with traitors. 
So, you still decide to use your super amazing ship blaster to attack the other side. You know if you 
are successful at an attack, because you can see the explosions. Once you have destroyed all 10 ships, 
you will be declared the winner. If the other side does so before you, you will be the loser. 
The odds are against you. Good luck. 



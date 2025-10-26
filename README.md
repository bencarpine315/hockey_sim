Not a terribly advanced or in-depth simulator but realistic and fun to toy around with.
XLSX file will eventually be hundreds (if not thousands) of players long. It is important to have it in the same working directory when testing file, otherwise
there will be no dataframe to pull anything from.
This project is a MASSIVE work in progress. I want to eventually be able to simulate entire seasons.
My knowledge of Python is rudimentiary but I think this is a cool, Monte Carlo-esque way of
applying my love of sports to coding and frankly there's no other way I wanna do it.

The engine runs on a variety of different random "dice-rolls" generated via the random library.
It does not simulate live line-changes, as that would significantly slow down the speed of simulation.
Rather, the engine simulates statistics in the aggregate, an effective and realistic manner that
avoids the mire of constant substitutions and changes of players in real-time as exists in hockey.
It utilizes player ratings, which I chose to simply make up rather than use real players and
create an objective rating system, which imposes a whole new set of challenges onto this project.
In it's current state, the code is only capable of running through one game at a time; however,
I plan to write the code such that it can simulate entire seasons, including the playoffs,
where the engine will simulate games that occur on a calendar day. Once the games on that day
have all been simulated, it will then save those stats to long-term storage (likely another xlsx
file) using player-ID's and team ID's (for separate player and team statistic storage). I will
add in a playoff engine at a later date. I will also be adding in trade logic, free agent signing,
and a player development system that will utilize the minor leagues and prospects.

At it's current state, I still plan on introducing power plays and penalty-killing, as well as
a more in-depth overtime feature (including a shoot-out feature). I don't have much of a timeline
for any of this, but it will be rolling out at some point in the coming weeks.


Thanks for reading!. 
- Ben ( 10/24/2025 )

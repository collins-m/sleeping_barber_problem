# sleeping barber problem
This is a solution to the sleeping barber problem written in python. It implements the threading module.
This solution example uses three barbers, and fifteen available seats in the waiting area.
It is run for 30 seonds by default to get an idea of what is happening, this could be run indefinitely.

The program makes use of multithreading, namely the three barbers. They simultaneously use the same customers that enter the shop at random intervals.
The haircuts represent the events that we are synchronising, the barbers represent the threads, while the cutomers - also being casted as threads for the purpose of adding them to the queue etc. - represent the "platform" that the task or event is being acted upon.
When a barber is sleeping, it represents a thread waiting for a task. When the barber is awake, it represents the thread operating on said task.

The problem is a well-known one, highlighting the advantages of multithreading, and showcases the tools used to do so.
Comments are scattered throughout the code to help the reader understand my reasoning behind each snippet of code.

This problem is dynamic, and can be used in a surprisingly large variety of implementations. One such implemetation is optimisation.
Several iterations could be held for an average day of business.
The shop owner could try to maximise profits based off the number of barbers - the business's efficiency - vs the number of customers who left without getting their hair cut - the opportunity cost.
The problem is useful for learning the principals of multithreading, and a great introduction to the topic.

import threading, time, random
from queue import Queue

CUSTOMER_SEATS = 15 # Number of available seats.
BARBERS = 3 # Number of barbers working.

EVENT = threading.Event() # Customer signals the barber to wake up.

ARRIVAL_WAIT = 1.5 # constant for arrival wait time.

def wait():
	time.sleep(ARRIVAL_WAIT * random.random()) # determines wait time upon arrival.

class Customer(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue # uses queue for new customers.

	WAIT = 0.003
	def haircut(self):
		return self.WAIT * random.randrange(500,1500,1) # Time taken for haircut.

	def trim(self):
		time_length = self.haircut()
		print("Customer haircut has started.")
		time.sleep(time_length) # In process of getting haircut.
		print("Customer haircut has finished. Haircut lasted {:.3} minutes.".format(time_length*10))
	def run(self):
		print("Customer has entered the shop.")
		if self.queue.full(): # Not always reliable.
			print("Queue is full, customer has left the shop.")
		else:
			# Wakes barber up.
			EVENT.set()
			EVENT.clear()

class Barber(threading.Thread):
	def __init__(self, queue, timer):
		threading.Thread.__init__(self)
		self.queue = queue # Uses queue to act on customers.
		self.asleep = True # Defaults to asleep.
		self.timer = timer

	def sleep_state(self): # Used to check for customers, if there are none, barber goes to sleep.
		if self.queue.empty():
			self.asleep = True
		else:
			self.asleep = False

	def run(self):
		while self.timer[0]: # To be used for 30 seconds.
			while self.queue.empty():
				EVENT.wait() # Sleeps while waiting for customer
			
			if self.asleep:
				print("Barber", self.name[-1], "is sleeping...")

			self.sleep_state() # Wakes barber up.
			print("Barber", self.name[-1], "is awake.")
			current_customer = self.queue # Calls customer for haircut.
			current_customer.get().trim() # Haircut takes place.
			current_customer.task_done() # Indicates that the formerly enqueued task is complete. 
			print("Barber", self.name[-1], "has finished cutting hair.")
			print("Barber", self.name[-1], "has gone back to sleep...")
			self.sleep_state() # Barber goes back to sleep.


def timeout(timer):
	timer[0]=False # When timer is finished.

def main():
	queue = Queue(CUSTOMER_SEATS) # Defines queue for the shop.
	timer=[True] # Initiate timer status.
	
	barbers = [] # Empty list for use later.
	for b in range(BARBERS):
		b = Barber(queue, timer) # Initialises b as a barber thread.
		b.daemon = True # Reduces hang at the end of its usage. Sets thread to low priority.
		b.start() # Barber starts haircut.
		barbers.append(b) # Barber is added to list of barbers for termination.

	t = threading.Timer(30.0, timeout, args=[timer]) # creates a 30 second timer.
	t.start() # Starts the countdown.
	while timer[0]: # While timer is in effect.
		print("There are", str(queue.qsize()), "people in the queue.")
		wait() # Initial wait upon arrival.
		c = Customer(queue) # New customer is initialised.
		c.start() # Customer enters the shop.
		queue.put(c) # Customer joins the queue.
		c.join() # Customer is done, leaves the shop.
		print("Customer has paid for their haircut and left the shop.")

	for b in barbers:
		b.join() # Barber threads are terminated.

	print("Barber shop is closed.")


if __name__ == "__main__":
	main() # Execute main function.
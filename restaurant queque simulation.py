import simpy
import random
import statistics
import numpy as np

wait_times = []

class Restaurant(object):
    def __init__(self,env, num_servers,num_cooks):
        self.env = env
        self.server = simpy.Resource(env, num_servers)
        self.scanner = simpy.Resource(env, num_cooks)

    def buy_food(self,customer):
        yield self.env.timeout(np.random.exponential(1))

    def cook_food(self,customer):
        yield self.env.timeout(random.uniform(5,7))

def go_to_eat(env,customer,restaurant):
    #Customer arrive at the restaurant
    arrival_time = env.now

    with restaurant.server.request() as request:
        yield request
        yield env.process(restaurant.buy_food(customer))

    with restaurant.scanner.request() as request:
        yield request
        yield env.process(restaurant.cook_food(customer))

    queue = env.now - arrival_time
    minutes_queue, frac_minutes = divmod(queue, 1)
    seconds_queue = frac_minutes * 60
    print(f"The customer wait time is {minutes_queue} minutes and {seconds_queue} seconds.")
    wait_times.append(env.now - arrival_time)

def run_restaurant(env, num_servers, num_cooks):
    restaurant = Restaurant(env, num_servers, num_cooks)

    for customer in range(10):
        env.process(go_to_eat(env, customer, restaurant))

    while True:
        yield env.timeout(np.random.exponential(5))  #Mean interarrival rate μ1 = 0.2 minutes)

        customer += 1
        env.process(go_to_eat(env, customer, restaurant))

def get_user_input():
    num_servers = input("Input # of cashiers: ")
    num_cooks = input("Input # of cooks: ")

    params = [num_servers, num_cooks]
    params = [int(x) for x in params]
    return params

def main():
  # Setup
  random.seed(69420)
  num_servers, num_cooks = get_user_input()

  # Run the simulation
  env = simpy.Environment()
  env.process(run_restaurant(env, num_servers, num_cooks))
  env.run(until=100)
  # View the results
  average_wait = statistics.mean(wait_times)
  minutes, frac_minutes = divmod(average_wait, 1)
  seconds = frac_minutes * 60
  print("-----------")
  print(f"\nThe average wait time is {minutes} minutes and {seconds} seconds.")

#Running Simulation:
main()

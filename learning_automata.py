import random, datetime, numpy as np, math
random.seed(datetime.datetime.now())

#algorithm that takes penalties into account - linear reward penality
def lrP(alpha, beta):
	print("Starting LRP - Linear Reward Penalty Algorithm\n\n")
	for j in range(10):
		levers = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"]
		reward_percent = [random.random() for i in range(10)]
		lever_count, reward_count  = ([0 for i in range(10)] for i in range(2))
		#probability of choosing a lever - sum equal to 1
		lever_probability = [0.1 for i in range(10)]
		optimal_decision = 0
		#randomly choose a lever and set alpha/beta values
		lever = random.randint(0, 9)
		#gets lever that is the most optimal (has the highest chance of giving us a reward)
		optimal_decision = reward_percent.index(max(reward_percent))
		i = 1
		while i <= 10000:
			# if reward = 1
			if random.random() < reward_percent[lever]:
				reward_count[lever]+=1
				#update the current lever
				lever_probability[lever] = lever_probability[lever] + alpha * (1- lever_probability[lever])
				#update other levers
				for x in range(0, len(lever_probability)):
					if x is not lever:
						lever_probability[x] = (1 - alpha) * lever_probability[x]
			#else reward = 0
			else:
				#update the other levers
				for x in range(0, len(lever_probability)):
					if x is not lever:
						lever_probability[x] = (beta/(len(levers)-1)) +  (1 - beta) * lever_probability[x]
				#update the current lever that did not give us a reward
				lever_probability[lever] = (1 - beta) * lever_probability[lever]

			lever_count[lever] += 1
			i+=1
			#choose the lever with the highest lever_probability (list of probabilities of chance to choose each arm respectively)
			lever = np.random.choice(10, p=lever_probability)

		print("Run: %d - Optimal Decision: %s with chance: %f chosen %d times. Average reward: %.2f" %  (j+1,levers[optimal_decision], reward_percent[optimal_decision], lever_count[optimal_decision], sum(reward_count)/i))

#algorithm that DOESNT take penalties into account BETA = 0 - linear reward inaction
def lrI(alpha):
	print("\n\nStarting LRI - Linear Reward Inaction Algorithm\n\n")
	for j in range(10):
		levers = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"]
		reward_percent = [random.random() for i in range(10)]
		lever_count, reward_count  = ([0 for i in range(10)] for i in range(2))
		#probability of choosing a lever - sum equal to 1
		lever_probability = [0.1 for i in range(10)]
		optimal_decision = 0
		#randomly choose a lever and set alpha/beta values
		lever = random.randint(0, 9)
		beta = 0
		#gets lever that is the most optimal (has the highest chance of giving us a reward)
		optimal_decision = reward_percent.index(max(reward_percent))
		i = 1
		while i <= 10000:
		# if reward = 1
			if random.random() < reward_percent[lever]:
				reward_count[lever]+=1
				#update the current lever
				lever_probability[lever] = lever_probability[lever] + alpha * (1- lever_probability[lever])
				#update other levers
				for x in range(0, len(lever_probability)):
					if x is not lever:
						lever_probability[x] = (1 - alpha) * lever_probability[x]
			lever_count[lever] += 1
			i+=1
			#choose the lever according to the probability distribution lever_probability
			lever = np.random.choice(10, p=lever_probability)

		print("Run: %d, Optimal Decision: %s with chance: %f chosen %d times. Average reward: %.2f" % (j+1, levers[optimal_decision], reward_percent[optimal_decision], lever_count[optimal_decision], sum(reward_count)/i))

alpha = input("Linear Reward Penalty - Enter a value for alpha (default = 0.2): ") or 0.2
beta = input("Linear Reward Penalty - Enter a value for alpha (default = 0.8): ") or 0.8
alpha2 = input("\nLinear Reward Inaction - Enter a value for alpha (default = 0.01): \n") or 0.01
lrP(alpha, beta)
lrI(alpha2)

import tensorflow as tf
import numpy as np
import random, datetime
random.seed(datetime.datetime.now())

bandits = ["q"+str(x) for x in range(1,11)]
no_of_bandits = len(bandits)

#start of neural network
tf.reset_default_graph()

#initializes the weights and sets to choose the action using argmax
weights = tf.Variable(tf.ones([no_of_bandits]))
chosen_action = tf.argmax(weights,0)

#Give reward value and action to the network to compute win or loss, train and update the network.
reward_holder = tf.placeholder(shape=[1],dtype=tf.float32)
action_holder = tf.placeholder(shape=[1],dtype=tf.int32)
responsible_weight = tf.slice(weights,action_holder,[1])
loss = -(tf.log(responsible_weight)*reward_holder)
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.002)
update = optimizer.minimize(loss)

#array to see if the agent was correct or not:
score = [0 for i in range(len(bandits))]

for iterator in range(10):
    #create % chance for bandits to return reward and initialize array to hold amount of rewards from each bandit
    reward_percent = [random.random() for x in range(no_of_bandits)]
    total_reward = np.zeros(no_of_bandits)

    #choose first action
    lever = random.randint(0, 9)
    epsilon = 0.2222
    total_episodes = 1000 #Set total number of episodes to train agent on.

    #initialize neural net
    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        i = 0
        while i < total_episodes:
            if random.random() < epsilon:
                vals = list(range(0, 10))
                vals.remove(sess.run(chosen_action))
                lever = random.choice(vals)

            #else, pick the value that has historically given the highest reward
            else:
                lever = sess.run(chosen_action)
            #pray to RNGesus that we get a reward from our lever
            reward = 0
            if random.random() < reward_percent[lever]:
                reward = 1
            else:
                reward = -1

            #update the total reward for the action we chose
            total_reward[lever] += reward
            #update our network
            _,resp,ww = sess.run([update,responsible_weight,weights], feed_dict={reward_holder:[reward],action_holder:[lever]})

            i+=1
    #if bandit with highest reward equals to bandit estimated to have highest reward, agent was correct
    if(np.argmax(reward_percent) == np.argmax(ww)):
        score[iterator] = "Correct"
    else:
        score[iterator] = "X"
print(score)

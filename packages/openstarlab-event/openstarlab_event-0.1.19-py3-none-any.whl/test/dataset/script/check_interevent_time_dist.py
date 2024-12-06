import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

train_path= "/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/csv/train.csv"
train_df = pd.read_csv(train_path)

#plot the distribution of inter-event times
plt.figure()
plt.hist(train_df[train_df["delta_T"] != 0]["delta_T"], bins=100, density=True)
plt.title("Distribution of inter-event times")
plt.xlabel("Interevent time (s)")
plt.ylabel("Density")

#save the plot
save_path= "/home/c_yeung/workspace6/python/openstarlab/Event/test/dataset/plot"
os.makedirs(save_path, exist_ok=True)
plt.savefig(os.path.join(save_path, "interevent_time_dist.png"))

#calculate the mean and standard deviation of inter-event times
mean_interevent_time = np.mean(train_df[train_df["delta_T"] != 0]["delta_T"])
std_interevent_time = np.std(train_df[train_df["delta_T"] != 0]["delta_T"])
print("Mean inter-event time: ", mean_interevent_time)
print("Standard deviation of inter-event time: ", std_interevent_time)

#take log of inter-event times and plot the distribution
plt.figure()
plt.hist(np.log(train_df[train_df["delta_T"] != 0]["delta_T"]+1e-6), bins=100, density=True)
plt.title("Distribution of log inter-event times")
plt.xlabel("Log interevent time")
plt.ylabel("Density")

#save the plot
plt.savefig(os.path.join(save_path, "log_interevent_time_dist.png"))

#calculate the mean and standard deviation of log inter-event times
mean_log_interevent_time = np.mean(np.log(train_df[train_df["delta_T"] != 0]["delta_T"]+1e-6))
std_log_interevent_time = np.std(np.log(train_df[train_df["delta_T"] != 0]["delta_T"]+1e-6))
print("Mean log inter-event time: ", mean_log_interevent_time)
print("Standard deviation of log inter-event time: ", std_log_interevent_time)


from time import sleep
from tqdm import tqdm


for i in tqdm(range(0, 100)):
        sleep(.05)

# data = [1,2,-3,-4]
# for i in range(len(data)):
#         if data[i] < 0:
#                 data[i] = 0
#         else:
#                 data[i] = 1
# print(data)

# for idx, num in enumerate(data):
#         if num < 0:
#                 data[idx] = 0
#         else:
#                 data[idx] = 1
# print(data)
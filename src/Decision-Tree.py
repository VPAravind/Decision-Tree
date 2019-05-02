import math
import pandas as pd

"""

Program that creates a decision tree on the give input file: WaitTable.csv.

"""

class Node:
    """
    Node class which stores the data frame associated with each node in the
    decision tree
    """
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_children(self, item):
        self.children.append(item)


def group_dict(as_dict):
    """
    Group the data frame with the target node.
    :param as_dict: Data frame as dictionary
    :return: grouped dictionary for calculating entropy
    """
    inner_dict = {}

    for k, v in as_dict.items():
        #getting the list of items
        item = as_dict[k]
        dict2 = {}
        target = as_dict['Wait']

        if not inner_dict or k not in inner_dict:
            inner_dict[k] = dict2

        for i in range(len(item)):

            cur = item[i]
            if not dict2 or item[i] not in dict2:
                dict2[cur] = {}
            if target[i] not in dict2[cur]:
                dict2[cur][target[i]] = []
                dict2[cur][target[i]].append(i)

            else:
                dict2[cur][target[i]].append(i)

    return inner_dict.copy()

def get_entropy(inner_dict, used):
    """
    Calculate the entropy values for every attribute in the current subset of
    data and return them as a dictionary.
    :param inner_dict:
    :param used:
    :return:
    """
    entropy_dict = {}
    for k, v in inner_dict.items():
        if k != 'Num' and k not in used:
            if not entropy_dict or k not in entropy_dict:
                entropy_dict[k] = []

            for k1, v1 in inner_dict[k].items():
                li = []
                for k2, v2 in inner_dict[k][k1].items():
                    li.append(len(v2))
                entropy_dict[k].append(list(li))

    final_entropy = {}
    for k, v in entropy_dict.items():
        if k != 'Wait':
            total = 0
            for li in v:
                sum = 0
                for val in li:
                    sum += val
                for val in li:
                    prob = val / sum
                    total -= (prob * (math.log10(prob)))

            final_entropy[k] = total
    return final_entropy


def split(df, inner_dict, used):
    """
    Return the minimum entropy value and the it's corresponding attribute
    required for the split.
    :param df:
    :param inner_dict:
    :param used:
    :return: Min entropy value
    """
    entropy_dict = get_entropy(inner_dict, used)

    return entropy_dict[min(entropy_dict, key=entropy_dict.get)], min(entropy_dict, key=entropy_dict.get)


def partition_data(df, attr):
    """
    Partition the data
    :param df:
    :param attr:
    :return: list of partitioned data frames
    """
    quest = set(df[attr])

    data_list = []

    for q in quest:
        data_list.append((attr, q, df[(df[attr] == q)]))

    return list(data_list)


def decision_tree(df, used, plist):
    """
    Recursively splits the current data frame based on entropy until entropy value
    that set of data is 0.
    :param df:
    :param used:
    :param plist:
    :return:
    """
    data_dict = df.to_dict('list')
    inner_dict = group_dict(data_dict.copy())

    entropy, attr = split(df, inner_dict, used)
    used.append(attr)

    plist.append((attr, entropy))

    if entropy == 0.0:
         return Node(df)

    cur = Node(df)

    data_list = partition_data(df, attr)

    for datas in data_list:
        node = decision_tree(datas[2], used, plist)
        cur.children.append(node)

    return cur


def traverse(node):
    """
    Traverse the tree created and print the data frames at each node.
    :param node:
    :return: None
    """
    if node:
        print(node.data)
        print('*******************')
        for child in node.children:
            traverse(child)

    return

def main():
    """
    Creates the initial data frame.
    :return:
    """
    df = pd.read_csv('WaitTable.csv')
    used = []
    plist = []
    root = decision_tree(df, used, plist)
    traverse(root)


if __name__ == '__main__':
    main()
# Utility functions go here

def get_comments_data(filename):
    f = open(filename)
    labels, timestamps, comments = list(), list(), list()
    lines = f.readlines()
    for line in lines:
        contents = line.split(",")
        if float(contents[0]) == 0.0:
            labels.append(-1)
        else:
            labels.append(1)
        timestamps.append(contents[1])
        comments.append(" ".join(contents[2:]))
    f.close()
    comments = map(lambda x: x.strip('\n').strip('"""'), comments)
    return (labels, timestamps, comments)


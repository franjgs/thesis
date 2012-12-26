import _mysql

# load the kaggle comments dataset
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

# load the depression dataset
def get_distress_data(connection):
    db = _mysql.connect(
            connection["hostname"],
            connection["database"],
            connection["username"],
            connection["password"],
    )
    db.query("select * from ratings_story")
    labels, stories = list(), list()
    results = db.store_result()
    while True:
        row = results.fetch_row()
        if not row:
            break
        else:
            labels.append(int(row[0][3]))
            stories.append(row[0][2])
    return (labels, stories)


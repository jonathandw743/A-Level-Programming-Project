import pickle

def load_obj(file_path):
    with open(file_path, r"rb") as f:
        users = pickle.load(f)
    return users

def save_obj(obj, file_path):
    with open(file_path, r"wb") as f:
        pickle.dump(obj, f)

if __name__ == "__main__":
    l1 = [1, 5, 2, 5, 3]
    print(l1, type(l1), id(l1))

    save_obj(l1, r"./afile.p")

    l2 = load_obj(r"./afile.p")
    print(l2, type(l2), id(l2))
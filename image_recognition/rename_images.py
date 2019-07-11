import os
from datetime import datetime


def main():
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    path = os.path.join(os.getcwd(), 'images/screens/1024-768/unlabeled')
    for index, filename in enumerate(os.listdir(path)):
        os.rename(os.path.join(path, filename), os.path.join(path,f'{index}-{now}.png'))


if __name__ == '__main__':
    # Calling main() function
    main()

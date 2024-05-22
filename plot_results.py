import numpy as np
import matplotlib.pyplot as plt

def plot_all_data_UR5():
    for z in np.arange(0.1, 0.5, 0.05):
        for y in np.arange(0.3, 0.65, 0.05):
            for x in np.arange(-0.1, 0.2, 0.05):
                # Load the data from the text files
                manipulability_values = np.loadtxt("data_UR5/manipulability_values_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                success_list = np.loadtxt("data_UR5/success_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                collision_list = np.loadtxt("data_UR5/collision_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")

                # Plot manipulability values
                plt.figure(figsize=(10, 5))
                plt.subplot(1, 2, 1)
                plt.plot(manipulability_values)
                plt.title("Manipulability Values (x={:.2f}, y={:.2f}, z={:.2f})".format(x, y, z))
                plt.xlabel("Index")
                plt.ylabel("Manipulability")

                # Plot success list
                plt.subplot(1, 2, 2)
                plt.plot(success_list, label="Success")
                plt.plot(collision_list, label="Collision")
                plt.title("Success and Collision (x={:.2f}, y={:.2f}, z={:.2f})".format(x, y, z))
                plt.xlabel("Index")
                plt.ylabel("Boolean")
                plt.legend()

                plt.tight_layout()
                plt.show()


def plot_all_data_UR10():
    for z in np.arange(-0.1, 0.5, 0.05):
        for y in np.arange(0.5, 0.9, 0.05):
            for x in np.arange(-0.2, 0.3, 0.05):
                # Load the data from the text files
                manipulability_values = np.loadtxt("data_UR10/manipulability_values_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                success_list = np.loadtxt("data_UR10/success_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                collision_list = np.loadtxt("data_UR10/collision_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")

                # Plot manipulability values
                plt.figure(figsize=(10, 5))
                plt.subplot(1, 2, 1)
                plt.plot(manipulability_values)
                plt.title("Manipulability Values (x={:.2f}, y={:.2f}, z={:.2f})".format(x, y, z))
                plt.xlabel("Index")
                plt.ylabel("Manipulability")

                # Plot success list
                plt.subplot(1, 2, 2)
                plt.plot(success_list, label="Success")
                plt.plot(collision_list, label="Collision")
                plt.title("Success and Collision (x={:.2f}, y={:.2f}, z={:.2f})".format(x, y, z))
                plt.xlabel("Index")
                plt.ylabel("Boolean")
                plt.legend()

                plt.tight_layout()
                plt.show()

def plot_filtered_data_UR5():
    for z in np.arange(0.1, 0.5, 0.05):
        for y in np.arange(0.3, 0.65, 0.05):
            for x in np.arange(-0.1, 0.2, 0.05):
                # Load the data from the text files
                manipulability_values = np.loadtxt("data_UR5/manipulability_values_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                success_list = np.loadtxt("data_UR5/success_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                collision_list = np.loadtxt("data_UR5/collision_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")

                # Check if there are no 0 values in success_list or no 1 values in collision_list
                if (success_list != 0).all() and (collision_list != 1).all():
                    # Plot manipulability values
                    plt.figure(figsize=(10, 5))
                    plt.subplot(1, 2, 1)
                    plt.plot(manipulability_values)
                    plt.title("Manipulability Values (x={:.2f}, y={:.2f}, z={:.2f})".format(x, y, z))
                    plt.xlabel("Index")
                    plt.ylabel("Manipulability")

                    # Plot success list
                    plt.subplot(1, 2, 2)
                    plt.plot(success_list, label="Success")
                    plt.plot(collision_list, label="Collision")
                    plt.title("Success and Collision (x={:.2f}, y={:.2f}, z={:.2f})".format(x, y, z))
                    plt.xlabel("Index")
                    plt.ylabel("Boolean")
                    plt.legend()

                    plt.tight_layout()
                    plt.show()


def plot_filtered_data_UR10():
    for z in np.arange(0.3, 0.6, 0.05):
        for y in np.arange(0.5, 1.0, 0.05):
            for x in np.arange(-0.3, 0.4, 0.05):
                # Load the data from the text files
                manipulability_values = np.loadtxt("data_UR10/manipulability_values_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                success_list = np.loadtxt("data_UR10/success_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                collision_list = np.loadtxt("data_UR10/collision_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")

                # Check if there are no 0 values in success_list or no 1 values in collision_list
                if (success_list != 0).all() and (collision_list != 1).all():
                    # Plot manipulability values
                    plt.figure(figsize=(10, 5))
                    plt.subplot(1, 2, 1)
                    plt.plot(manipulability_values)
                    plt.title("Manipulability Values (x={:.2f}, y={:.2f}, z={:.2f})".format(x, y, z))
                    plt.xlabel("Index")
                    plt.ylabel("Manipulability")

                    # Plot success list
                    plt.subplot(1, 2, 2)
                    plt.plot(success_list, label="Success")
                    plt.plot(collision_list, label="Collision")
                    plt.title("Success and Collision (x={:.2f}, y={:.2f}, z={:.2f})".format(x, y, z))
                    plt.xlabel("Index")
                    plt.ylabel("Boolean")
                    plt.legend()

                    plt.tight_layout()
                    plt.show()


def plot_filtered_data_UR10_few():
    c = 0
    for z in np.arange(0.3, 0.6, 0.05):
        for y in np.arange(0.5, 1.0, 0.05):
            for x in np.arange(-0.3, 0.4, 0.05):
                # Load the data from the text files
                manipulability_values = np.loadtxt("data_UR10/manipulability_values_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                success_list = np.loadtxt("data_UR10/success_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                collision_list = np.loadtxt("data_UR10/collision_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")

                # Check if there are no 0 values in success_list or no 1 values in collision_list
                # and there are 5 or fewer collisions
                if np.sum(collision_list) <= 5 and np.sum(success_list == 0) <= 5:
                    c += 1
                    # # Plot manipulability values
                    # plt.figure(figsize=(10, 5))
                    # plt.subplot(1, 2, 1)
                    # plt.plot(manipulability_values)
                    # plt.title("Manipulability Values (x={:.2f}, y={:.2f}, z={:.2f})".format(x, y, z))
                    # plt.xlabel("Index")
                    # plt.ylabel("Manipulability")

                    # # Plot success list
                    # plt.subplot(1, 2, 2)
                    # plt.plot(success_list, label="Success")
                    # plt.plot(collision_list, label="Collision")
                    # plt.title("Success and Collision (x={:.2f}, y={:.2f}, z={:.2f})".format(x, y, z))
                    # plt.xlabel("Index")
                    # plt.ylabel("Boolean")
                    # plt.legend()

                    # plt.tight_layout()
                    # plt.show()
    print(c)


if __name__ == "__main__":
    # plot_all_data_UR5()
    # plot_all_data_UR10()
    # plot_filtered_data_UR10()
    # plot_filtered_data_UR5()
    plot_filtered_data_UR10_few()
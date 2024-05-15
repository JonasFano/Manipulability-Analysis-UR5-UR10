import numpy as np
import matplotlib.pyplot as plt

def plot_all_data():
    for z in np.arange(0.0, 0.6, 0.1):
        for y in np.arange(0.8, 1, 0.1):
            for x in np.arange(-0.2, 0.3, 0.1):
                # Load the data from the text files
                manipulability_values = np.loadtxt("data/manipulability_values_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                success_list = np.loadtxt("data/success_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                collision_list = np.loadtxt("data/collision_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")

                # Plot manipulability values
                plt.figure(figsize=(10, 5))
                plt.subplot(1, 2, 1)
                plt.plot(manipulability_values)
                plt.title("Manipulability Values (x={:.1f}, y={:.1f}, z={:.1f})".format(x, y, z))
                plt.xlabel("Index")
                plt.ylabel("Manipulability")

                # Plot success list
                plt.subplot(1, 2, 2)
                plt.plot(success_list, label="Success")
                plt.plot(collision_list, label="Collision")
                plt.title("Success and Collision (x={:.1f}, y={:.1f}, z={:.1f})".format(x, y, z))
                plt.xlabel("Index")
                plt.ylabel("Boolean")
                plt.legend()

                plt.tight_layout()
                plt.show()

def plot_filtered_data():
    for z in np.arange(0.0, 0.6, 0.1):
        for y in np.arange(0.8, 1, 0.1):
            for x in np.arange(-0.2, 0.3, 0.1):
                # Load the data from the text files
                manipulability_values = np.loadtxt("data/manipulability_values_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                success_list = np.loadtxt("data/success_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")
                collision_list = np.loadtxt("data/collision_list_" + str(x) + "_" + str(y) + "_" + str(z) + ".txt")

                # Check if there are no 0 values in success_list or no 1 values in collision_list
                if (success_list != 0).all() and (collision_list != 1).all():
                    # Plot manipulability values
                    plt.figure(figsize=(10, 5))
                    plt.subplot(1, 2, 1)
                    plt.plot(manipulability_values)
                    plt.title("Manipulability Values (x={:.1f}, y={:.1f}, z={:.1f})".format(x, y, z))
                    plt.xlabel("Index")
                    plt.ylabel("Manipulability")

                    # Plot success list
                    plt.subplot(1, 2, 2)
                    plt.plot(success_list, label="Success")
                    plt.plot(collision_list, label="Collision")
                    plt.title("Success and Collision (x={:.1f}, y={:.1f}, z={:.1f})".format(x, y, z))
                    plt.xlabel("Index")
                    plt.ylabel("Boolean")
                    plt.legend()

                    plt.tight_layout()
                    plt.show()


if __name__ == "__main__":
    plot_all_data()
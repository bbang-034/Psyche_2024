import time

def radix_sort(data, draw_data, speed):
    max_num = max(data)
    exp = 1
    while max_num // exp > 0:
        n = len(data)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = data[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = data[i] // exp
            output[count[index % 10] - 1] = data[i]
            count[index % 10] -= 1
            i -= 1

        i = 0
        for i in range(0, len(data)):
            data[i] = output[i]
            draw_data(data, optional_color='red', digit=i)  # Visualize the sorting process
            time.sleep(speed)
        exp *= 10
        # Draw the final state of the data

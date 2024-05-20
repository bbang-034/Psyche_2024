from tkinter import *
from tkinter import ttk
from radix_sort import *
import random
import pygame
import sys
# Functions


# This function displays the array
def draw_data(current_data, digit=-1, optional_color='cyan', end=-1, digit2=999, var1=-999, var2=-999):
    canvas.delete('all')
    color = DEFAULT_COLOR
    count = 0
    C_HEIGHT = 700
    C_WIDTH = 1400
    x_width = C_WIDTH / (len(current_data))
    offset = 10
    spacing = 5
    normalized_data = [i / max(current_data) for i in current_data]
    for i, height in enumerate(normalized_data):
        # upper left
        x0 = i * x_width + offset + spacing
        y0 = C_HEIGHT - height * 680
        # bottom right
        x1 = (i + 1) * x_width + offset
        y1 = C_HEIGHT
        if count == 2:
            color = DEFAULT_COLOR
        if digit != -1 and count < 2:
            if i == digit or i == digit + 1:
                color = optional_color
                count += 1

        if algMenu.get() == 'Radix Sort':
            if i == digit or i == digit2:
                color = optional_color
            elif i <= end:
                color = '#FF6A00'
            else:
                color = DEFAULT_COLOR

        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        data_value = current_data[i]
        text_x = (x0 + x1) / 2  # Calculate the x position for text
        text_y = y0 - 10  # Adjust the y position for text placement
        canvas.create_text(text_x, text_y, text=str(data_value), fill='white', font=('Helvetica', 8))

    root.update_idletasks()


# This function is called when SORT button is pressed
def start():
    print('Sorting...')
    global data
    if not data:
        print("It's done")
        return

    # These if else statements call the function of the selected algorithm
    radix_sort(data, draw_data, speedScale.get())

    print("It's done")


# This function is called when NEW ARRAY button is pressed
def generate():

    global data
    print('Algo: ' + selected_alg.get())
    try:
        min_val = int(minEntry.get())
    except EXCEPTION:
        min_val = 10
    try:
        max_val = int(maxEntry.get())
    except EXCEPTION:
        max_val = 10
    try:
        size = int(sizeEntry.get())
    except EXCEPTION:
        size = 10
    data = []
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    if max_val == 0:
        max_val = 100
    data = []
    for _ in range(size):
        data.append(random.randrange(min_val, max_val + 1))
    draw_data(data)

def inputtext():
    # 초기화
    global data
    data.clear()
    pygame.init()

    # 화면 설정
    WIDTH, HEIGHT = 960, 75
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FONT_SIZE = 30
    font = pygame.font.Font(None, FONT_SIZE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Text Input GUI")

    # 입력 상자의 크기와 위치 설정
    input_box = pygame.Rect(10, 10, 900, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False

    # 입력한 텍스트를 저장할 변수
    input_text = ''

    # 메인 루프
    running = True
    while running:
        a=0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 마우스 클릭 시, 입력 상자가 활성화됨
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                # 키 입력 이벤트 처리
                if active:
                    if event.key == pygame.K_RETURN:
                        # 엔터 키를 누르면 입력 상자가 비활성화됨
                        words = input_text.split()
                        data.extend([int(word) for word in words])
                        draw_data(data)
                        a=1
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        # 백스페이스 키를 누르면 마지막 문자를 지움
                        input_text = input_text[:-1]
                    else:
                        # 그 외의 키 입력은 텍스트에 추가함
                        input_text += event.unicode
        if(a == 1):
            break



        # 화면 지우기
        screen.fill(WHITE)

        # 입력 상자 그리기
        pygame.draw.rect(screen, color, input_box, 2)

        # 입력한 텍스트 표시
        text_surface = font.render(input_text, True, BLACK)
        width = max(200, text_surface.get_width() + 10)
        input_box.w = width
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        # 화면 업데이트
        pygame.display.flip()

    pygame.quit()


# Global declarations
DEFAULT_COLOR = '#00FDFD'
root = Tk()
root.title('Sorting Visualiser')
root.maxsize(1920, 1080)
root.config(bg='white')

# Variables
selected_alg = StringVar()
data = []

# User Interface

# Body
UI_frame = Frame(root, width=1024, height=200, bg='white')
UI_frame.grid(row=0, column=0)
canvas = Canvas(root, width=1500, height=800, bg='black')
canvas.grid(row=1, column=0)

# Elements

# Dropdown box for algorithms
Label(UI_frame, text='Algorithm:', bg='white').grid(
    row=0, column=0, padx=0, pady=0)
algMenu = ttk.Combobox(UI_frame, textvariable=selected_alg,
                       values=['Radix sort'])
algMenu.grid(row=0, column=1, padx=5, pady=5)
algMenu.current(0)

# Delay slider
speedScale = Scale(UI_frame, from_=0.01, to=2.0, length=150, digits=2, resolution=0.02, orient=HORIZONTAL,
                   label='Delay', activebackground='#00FDFD', troughcolor='black')
speedScale.grid(row=0, column=5, padx=5, pady=5)

# Sort Button
sort_btn = PhotoImage(file=r"image/sort.png")
Button(UI_frame, command=start, image=sort_btn).grid(
    row=0, column=7, padx=5, pady=5, sticky=E)

# Size of array slider
sizeEntry = Scale(UI_frame, from_=3, to=100, length=150, resolution=1, orient=HORIZONTAL,
                  label='Size', activebackground='#00FDFD', troughcolor='black')
sizeEntry.grid(row=0, column=2, padx=5, pady=5)

# Minimum Value slider
minEntry = Scale(UI_frame, from_=0, to=1000, length=150, resolution=1, orient=HORIZONTAL,
                 label='Min Value', activebackground='#00FDFD', troughcolor='black')
minEntry.grid(row=0, column=3, padx=5, pady=5)

# Maximum Value slider
maxEntry = Scale(UI_frame, from_=0, to=1000, length=150, resolution=1, orient=HORIZONTAL,
                 label='Max Value', activebackground='#00FDFD', troughcolor='black')
maxEntry.grid(row=0, column=4, padx=5, pady=5)

# New Array Button
na_btn = PhotoImage(file=r"image/newarray.png")
Button(UI_frame, command=generate, image=na_btn).grid(
    row=0, column=6, padx=5, pady=5)

# Exit Button
exit_btn = PhotoImage(file=r"image/exit.png")
Button(UI_frame, command=root.destroy, image=exit_btn).grid(
    row=0, column=8, padx=5, pady=5)

input_btn = PhotoImage(file=r"image/input.png")
Button(UI_frame, command=inputtext, image=input_btn).grid(
    row=0, column=10, padx=5, pady=5)

root.mainloop()











# 푸바오 가지마 ㅠㅠㅠ ㅠㅠㅠ ㅠㅠ ㅠㅠㅠ ㅠㅠ
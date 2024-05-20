import pygame

# Pygame 초기 설정
pygame.init()
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 36)
NODE_SIZE = 40
NODE_GAP = 50
LINE_WIDTH = 4
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_node(self, idx, value):
        new_node = Node(value)
        if idx == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            temp = self.head
            for _ in range(idx - 1):
                if temp is None:
                    raise IndexError("Index out of range")
                temp = temp.next
            if temp is None:
                raise IndexError("Index out of range")
            new_node.next = temp.next
            temp.next = new_node

    def delete_node(self, idx):
        if self.head is None:
            raise ValueError("List is empty")
        if idx == 0:
            temp = self.head
            self.head = temp.next
            del temp
        else:
            temp = self.head
            for _ in range(idx - 1):
                if temp is None:
                    raise IndexError("Index out of range")
                temp = temp.next
            if temp is None or temp.next is None:
                raise IndexError("Index out of range")
            target = temp.next
            temp.next = target.next
            del target

    def __str__(self):
        result = []
        temp = self.head
        while temp:
            result.append(str(temp.value))
            temp = temp.next
        return " -> ".join(result)

class LinkedListVisualizer:
    def __init__(self):
        self.linked_list = LinkedList()
        self.nodes = []
        self.input_box = pygame.Rect(10, 150, 140, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.font = pygame.font.Font(None, 32)

    def insert_node(self, idx, value):
        try:
            self.linked_list.insert_node(idx, value)
        except IndexError as e:
            print("Error:", e)
        self.update_nodes()

    def delete_node(self, idx):
        try:
            self.linked_list.delete_node(idx)
        except (IndexError, ValueError) as e:
            print("Error:", e)
        self.update_nodes()


    def update_nodes(self):
        self.nodes = []
        temp = self.linked_list.head
        idx = 0
        while temp:
            self.nodes.append((temp.value, idx))
            temp = temp.next
            idx += 1

    def draw(self):
        WINDOW.fill(WHITE)
        x, y = NODE_GAP, HEIGHT // 2

        for value, idx in self.nodes:
            pygame.draw.rect(WINDOW, BLUE, (x, y, NODE_SIZE, NODE_SIZE))
            text_surface = FONT.render(str(value), True, WHITE)
            WINDOW.blit(text_surface, (x + NODE_SIZE // 2 - text_surface.get_width() // 2,
                                       y + NODE_SIZE // 2 - text_surface.get_height() // 2))
            if idx < len(self.nodes) - 1:
                pygame.draw.line(WINDOW, BLACK, (x + NODE_SIZE, y + NODE_SIZE // 2),
                                 (x + NODE_SIZE + NODE_GAP, y + NODE_SIZE // 2), LINE_WIDTH)
            x += NODE_SIZE + NODE_GAP


        if self.active:
            if self.input_mode == 'insert':
                insert_txt = FONT.render("Insert: Enter idx and value seperated by space", True, BLACK)
                WINDOW.blit(insert_txt, (30, 100))  # Adjust position as needed
            elif self.input_mode == 'delete':
                delete_txt = FONT.render("Delete: Enter idx to delete", True, BLACK)
                WINDOW.blit(delete_txt, (30, 100))  # Adjust position as needed


        # 삽입 및 삭제 키 설명 추가
        insert_text = FONT.render("Press 'keyup' to insert", True, BLACK)
        delete_text = FONT.render("Press 'keydown' to delete", True, BLACK)
        quit_text = FONT.render("Press 'q' to quit", True, BLACK)
        WINDOW.blit(insert_text, (10, 10))
        WINDOW.blit(delete_text, (10, 50))
        WINDOW.blit(quit_text, (400, 10))

        # 입력 상자 그리기
        pygame.draw.rect(WINDOW, self.color, self.input_box, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        WINDOW.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))

        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Up arrow key for insert mode
                self.input_mode = 'insert'
                self.active = True
                self.text = ''
            elif event.key == pygame.K_DOWN:  # Down arrow key for delete mode
                self.input_mode = 'delete'
                self.active = True
                self.text = ''
            elif event.key == pygame.K_q:  # 'q' key for quitting the program
                pygame.quit()
                quit()
        elif event.type == pygame.KEYUP and self.active:
            if event.key == pygame.K_RETURN:
                if self.text:
                    try:
                        if self.input_mode == 'insert':
                            idx, value = map(int, self.text.split())
                            self.insert_node(idx, value)
                        elif self.input_mode == 'delete':
                            idx = int(self.text)
                            self.delete_node(idx)
                        self.active = False
                        self.text = ''
                    except ValueError:
                        if self.input_mode == 'insert':
                            print("Invalid input format. Please enter both index and value separated by space.")
                        elif self.input_mode == 'delete':
                            print("Invalid input format. Please enter a valid index.")
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode


def main():
    linked_list_visualizer = LinkedListVisualizer()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            linked_list_visualizer.handle_event(event)

        linked_list_visualizer.draw()

    pygame.quit()

if __name__ == "__main__":
    main()

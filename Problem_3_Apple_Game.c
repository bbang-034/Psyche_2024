#include <stdio.h>
#include <stdlib.h>

#define ROWS 15
#define COLS 20
#define MAX_RECTANGLES 1000 // 최대 직사각형 개수를 설정합니다.

typedef struct {
    int left;
    int top;
    int right;
    int bottom;
} Rectangle;

void process_map(const char* input_filename, const char* output_filename) {
    FILE *file;
    int matrix[ROWS][COLS];
    int i, j;

    // 파일 열기
    file = fopen(input_filename, "r");
    if (file == NULL) {
        perror("파일 열기 실패");
        return;
    }

    // 배열 요소 읽기
    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            fscanf(file, "%d", &matrix[i][j]);
        }
    }

    // 파일 닫기
    fclose(file);

    // 직사각형 정보를 저장할 배열과 개수 초기화
    Rectangle rectangles[MAX_RECTANGLES];
    int cnt = 0;

    int sum_size = 3;
    while (sum_size <= 31) {
        for (int row_size = 1; row_size < sum_size; row_size++) {
            if (row_size > ROWS) {
                break;
            }
            int col_size = sum_size - row_size;
            if (col_size > COLS) {
                continue;
            }
            for (int I = 0; I <= ROWS - row_size; I++) {
                for (int J = 0; J <= COLS - col_size; J++) {
                    int sum = 0;
                    for (i = 0; i < row_size; i++) {
                        for (j = 0; j < col_size; j++) {
                            sum += matrix[I + i][J + j];
                        }
                    }
                    if (sum == 10) {
                        if (cnt < MAX_RECTANGLES) {
                            rectangles[cnt].left = I;
                            rectangles[cnt].top = J;
                            rectangles[cnt].right = I + row_size - 1;
                            rectangles[cnt].bottom = J + col_size - 1;
                            cnt++;
                        }
                        for (int reset_i = I; reset_i < I + row_size; reset_i++) {
                            for (int reset_j = J; reset_j < J + col_size; reset_j++) {
                                matrix[reset_i][reset_j] = 0;
                            }
                        }
                    }
                }
            }
        }
        sum_size++;
    }

    // 출력 파일 열기
    FILE *output_file = fopen(output_filename, "w");
    if (output_file == NULL) {
        perror("출력 파일 열기 실패");
        return;
    }

    // 직사각형 개수 기록
    fprintf(output_file, "총 직사각형 개수: %d\n", cnt);

    // 직사각형 정보 기록
    for (i = 0; i < cnt; i++) {
        fprintf(output_file, "%d %d %d %d\n", rectangles[i].left, rectangles[i].top, rectangles[i].right, rectangles[i].bottom);
    }

    // 출력 파일 닫기
    fclose(output_file);
}

int main() {
    for (int i = 0; i < 30; i++) {
        char input_filename[20];
        char output_filename[25];
        snprintf(input_filename, sizeof(input_filename), "map%d.txt", i);
        snprintf(output_filename, sizeof(output_filename), "ans/ans_%d.txt", i+1);
        process_map(input_filename, output_filename);
        printf("파일 '%s' 처리 완료, 결과는 '%s'에 저장되었습니다.\n", input_filename, output_filename);
    }

    return 0;
}

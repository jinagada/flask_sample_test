import math


def calculate_page(page_num, row_per_page, totalcount, block_size_param):
    """
    페이징 처리를 위한 계산
    :param page_num:
    :param row_per_page:
    :param totalcount:
    :param block_size_param:
    :return:
    """
    block_size = block_size_param
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page_num - 1) / block_size)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_start = (block_size * block_num) + 1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)
    last_page_num = math.ceil(totalcount / row_per_page)
    return block_start, block_end, last_page_num

import chess
import time

nodes = 0

def perft_driver(depth : int) -> None:
    global nodes

    if depth == 0:
        nodes += 1
        return
    for move in b.legal_moves:
        b.push(move)
        perft_driver(depth - 1)
        b.pop()

b = chess.Board()
start = time.perf_counter()
perft_driver(4)
end = time.perf_counter()
print(f"time: {end - start}s")
print(nodes)
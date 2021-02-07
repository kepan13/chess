import chess
import time

nodes = 0

ml = []

def perft_driver(depth : int) -> None:
    global nodes

    if depth == 0:
        nodes += 1
        return
    for move in b.legal_moves:
        ml.append(str(move))
        b.push(move)
        perft_driver(depth - 1)
        b.pop()

b = chess.Board()
b.set_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -")
start = time.perf_counter()
perft_driver(2)
end = time.perf_counter()
# print(f"time: {end - start}s")
# print(nodes)

for i in range(10):
    print(ml[i])
print(len(ml), len(a))
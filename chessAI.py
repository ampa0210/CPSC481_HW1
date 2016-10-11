import chess
import random
import time
from math import *
from operator import itemgetter

bKposition=[-5, 0, 0, 0, 0, 0, 0, -5,
			0, 1, 2, 2, 2, 2, 1, 0,
			0, 2, 5, 5, 5, 5, 2, 0,
			0, 2, 5, 5, 5, 5, 2, 0,
			0, 2, 5, 5, 5, 5, 2, 0,
			0, 2, 5, 5, 5, 5, 2, 0,
			0, 1, 2, 2, 2, 2, 1, 0,
			-5, 0, 0, 0, 0, 0, 0, -5]

#This function is purely for testing purposes
def randomPlayer(board):
	move = random.choice(list(board.legal_moves))
	return move.uci()
	
def computerPlayer(board):
	#Call to get which move is best
	board_copy = board
	moveList = []
	bestMoves = []
	depth = 5
	if len(board.move_stack) <= 3:
		depth -= 2
	for i in board_copy.legal_moves:
		board_copy.push(i)
		score = alphaBetaMin(board_copy, float("-inf"), float("inf"), depth)
		board_copy.pop()
		moveList.append((i, score))
	
	#Get the best score from moves
	moveList = sorted(moveList, key=itemgetter(1), reverse=True)
	bestValue = moveList[0][1]
	index = len(moveList)
	for (i, v) in enumerate(moveList):
		if v[1] != bestValue:
			index = i
			break
	print(moveList)
	time.sleep(1)
	return moveList[random.randrange(0, index)][0] #Return random best move
	
def alphaBetaMax(board, alpha, beta, depth):
	if depth == 0 or board.result() != "*":
		return evaluate(board)
	
	#Iterate through legal moves, DFS.
	for i in board.legal_moves:
		board.push(i)
		score = alphaBetaMin(board, alpha, beta, depth-1)
		board.pop()
		if score >= beta:
			return beta
		if score > alpha:
			alpha = score
	return alpha
	
def alphaBetaMin(board, alpha, beta, depth):
	if depth == 0 or board.result() != "*":
		return -evaluate(board)
		
	for i in board.legal_moves:
		board.push(i)
		score = alphaBetaMax(board, alpha, beta, depth-1)
		board.pop()
		if score <= alpha:
			return alpha
		if score < beta:
			beta = score
	return beta
	
def evaluate(board):
	wR = board.pieces(chess.ROOK, chess.WHITE)
	wN = board.pieces(chess.KNIGHT, chess.WHITE)
	wK = board.pieces(chess.KING, chess.WHITE)
	bK = board.pieces(chess.KING, chess.BLACK)
	bN = board.pieces(chess.KNIGHT, chess.BLACK)
	if board.turn == chess.WHITE:
		return heuristicX(board, wR, wN, wK, bK, bN) - heuristicY(board, wR, wN, wK, bK, bN)
	else:
		return heuristicY(board, wR, wN, wK, bK, bN) - heuristicX(board, wR, wN, wK, bK, bN)

def heuristicX(board, wR, wN, wK, bK, bN):
	score = 0
	score += 9001 if board.result() == "1-0" else 0
	if len(wR) > 0: #Check to see if white rook exists
		score += whiteDefRook(board, wR, wK)*2
		score += whiteRookAtk(board, wR, bK)
		
	score += wkMove2bk(wK, bK)*3
	score -= len(board.move_stack)
	score += len(board.attacks(list(wK)[0]))	

	score += len(wN) * 150
	score += len(wR) * 300
	
	return score

def heuristicY(board, wR, wN, wK, bK, bN):
	score = 0
	score += 9001 if board.result() == "0-1" else 0
	score += 9001 if board.is_stalemate() else 0
	score += len(bN) * 150
	score += len(board.move_stack)
	score += bKposition[list(bK)[0]]
	
	return score
	
def whiteDefRook(board, wr, wk):
	score = 0
	guard = board.attackers(chess.WHITE, list(wk)[0])
	if len(guard) > 0:
			score = 25 #King gaurding Rook
	x = abs(chess.rank_index(list(wr)[0]) - chess.rank_index(list(wk)[0]))
	y = abs(chess.file_index(list(wr)[0]) - chess.file_index(list(wk)[0]))
	return score + (10-min(x,y))
	
def whiteRookAtk(board, wr, bk):
	x = abs(chess.rank_index(list(wr)[0]) - chess.rank_index(list(bk)[0]))
	y = abs(chess.file_index(list(wr)[0]) - chess.file_index(list(bk)[0]))
	return 10-min(x,y)
	
def wkMove2bk(wk, bk):
	x = chess.rank_index(list(wk)[0]) - chess.rank_index(list(wk)[0])
	y = chess.file_index(list(bk)[0]) - chess.file_index(list(bk)[0])
	return 10 - floor((y**2 + x**2)**(1/2))
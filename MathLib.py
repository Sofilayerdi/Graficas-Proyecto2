import numpy as np
from math import pi, sin, cos, isclose

def barycentricCoords(A, B, C, P):
	#Se saca el area de los subtriangulos y del tirangulo
	#mayor usando el Shoolace Theorem, una formula que permite
	# sacar el area de un poligono de cualquier cantidad de vertices.

	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				(P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))
	
	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) -
				(A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))
	
	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) -
				(A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))
	
	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) -
				(A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))
	
	#Si el area del triangulo es 0, retornar nada para 
	# prevenir que la division sea 0
	if areaABC == 0:
		return None
	
	#Determinar las coordenadas baricentricas dividiendo el 
	# area de cada subtriangulo por el area del triangulo mayor

	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC

	#Si cada coordenada esta entre 0 a 1 y la suma de las tres
	# es igual a 1, entonces son validas
	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:
		return (u, v, w)
	else:
		return None

def barycentricCoords3D(A, B, C, P, epsilon = 1e-8):
	v0 = np.substract(B, A)
	v1 = np.substract(C, A)
	v2 = np.substract(P, A)

	d00 = np.dot(v0, v0)
	d01 = np.dot(v0, v1)
	d11 = np.dot(v1, v1)
	d20 = np.dot(v2, v0)
	d21 = np.dot(v2, v1)

	denom = d00 * d11 - d01 * d01
	if abs(denom) < epsilon:
		return None #degenerate triangle
	
	v = (d11 * d20 - d01 * d21) / denom
	w = (d00 * d21 - d01 * d20) / denom
	u = 1-v-w

	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:
		return (u, v, w)
	else:
		return None



def TranslationMatrix(x, y, z):
	
	return np.matrix([[1, 0, 0, x],
					  [0, 1, 0, y],
					  [0, 0, 1, z],
					  [0, 0, 0, 1]])



def ScaleMatrix(x, y, z):
	
	return np.matrix([[x, 0, 0, 0],
					  [0, y, 0, 0],
					  [0, 0, z, 0],
					  [0, 0, 0, 1]])



def RotationMatrix(pitch, yaw, roll):
    # Convertir a radianes
    pitch = pitch * pi / 180
    yaw = yaw * pi / 180  
    roll = roll * pi / 180
    
    # Matrices de rotación individuales
    # Pitch (X-axis rotation)
    Rx = np.array([[1, 0, 0, 0],
                   [0, cos(pitch), -sin(pitch), 0],
                   [0, sin(pitch), cos(pitch), 0],
                   [0, 0, 0, 1]])
    
    # Yaw (Y-axis rotation)
    Ry = np.array([[cos(yaw), 0, sin(yaw), 0],
                   [0, 1, 0, 0],
                   [-sin(yaw), 0, cos(yaw), 0],
                   [0, 0, 0, 1]])
    
    # Roll (Z-axis rotation)  
    Rz = np.array([[cos(roll), -sin(roll), 0, 0],
                   [sin(roll), cos(roll), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    
    # Combinar rotaciones: R = Rz * Ry * Rx
    return Rz @ Ry @ Rx

def reflectVector(normal, direction):
	# R = 2 * (N o L) * N -L
	reflect = 2 * np.dot(normal, direction)
	reflect = np.multiply(reflect, normal)
	reflect = np.subtract(reflect, direction)
	reflect = reflect / np.linalg.norm(reflect)
	return reflect
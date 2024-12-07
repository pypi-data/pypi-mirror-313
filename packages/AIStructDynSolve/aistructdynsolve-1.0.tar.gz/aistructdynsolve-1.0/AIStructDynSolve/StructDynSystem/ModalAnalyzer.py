"""
AIStructDynSolve
A framework focused on solving structural dynamics problems using artificial intelligence (AI) methods
solve the following ODE of MDOF
M*U_dotdot+C*U_dot+K*U=Pt
initial condition: U(t=0)=InitialU, and U_dot(t=0)=InitialU_dot
Author: 杜轲 duke@iem.ac.cn
Date: 2023/12/26
"""
import numpy as np
from scipy.linalg import eig

class ModalAnalyzer:
    def __new__(cls, M, K):
        """
        计算并直接返回自然频率和模态形状，而不需要额外的函数调用。

        参数:
        - M (array): 质量矩阵。
        - K (array): 刚度矩阵。

        返回:
        - mode_shapes (array): 模态形状矩阵。
        - Omega2 (array): 自然频率平方的对角矩阵。
        """
        eigvals, eigvecs = eig(K, M)
        ind = np.argsort(eigvals)
        eigenvalues = np.diag(np.real(eigvals[ind]))
        eigenvectors = np.real(eigvecs[:, ind])

        return eigenvalues, eigenvectors
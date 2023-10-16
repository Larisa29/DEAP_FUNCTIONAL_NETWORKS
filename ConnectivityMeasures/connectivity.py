import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import hilbert,coherence
from abc import ABC, abstractmethod
from configurations.config import ROOT_DIR

class ConnectivityStrategy(ABC):
    """
    Clasa abstracta ce defineste o interfata comuna pentru diferite strategii de calcul ale conectivitatii.
    """
    @abstractmethod
    def compute_connectivity(self, current_channel, next_channel, fs):
        pass

class PhaseLagIndexStrategy(ConnectivityStrategy):
    def compute_connectivity(self, current_channel, next_channel, fs):
        """
        Clasa concreta ce extinde clasa abstracta ConnectivityStrategy. Aceasta implementeaza metoda abstracta compute_connectivity() pentru
        calculul conectivitatii folosind Phase Lag Index.
        """
        # calcul Transformata Hilbert pt. serii de timp
        current_channel_complex_values = hilbert(current_channel)
        next_channel_complex_values = hilbert(next_channel)
        # calcul unghi in radiani pt. nr. complexe obtinute anterior
        phase1 = np.angle(current_channel_complex_values)
        phase2 = np.angle(next_channel_complex_values)
        # calcul diferenta de faza
        phase_difference = phase1 - phase2
        # calcul PLI
        pli = np.abs(np.mean(np.sign(np.sin(phase_difference))))
        return pli

class WeightedPhaseLagIndexStrategy(ConnectivityStrategy):
    def compute_connectivity(self, current_channel, next_channel, fs):
        """
        Clasa concreta ce extinde clasa abstracta ConnectivityStrategy. Aceasta implementeaza metoda abstracta compute_connectivity() pentru
        calculul conectivitatii folosind Weighted Phase Lag Index.
        """
        # calcul Transformata Hilbert pt. serii de timp
        current_channel_analytic = hilbert(current_channel)
        next_channel_analytic = hilbert(next_channel)
        # calcul unghi in radiani pt. nr. complexe obtinute anterior
        current_channel_phase = np.angle(current_channel_analytic)
        next_channel_phase = np.angle(next_channel_analytic)
        # calcul diferenta de faza
        phase_difference = current_channel_phase - next_channel_phase
        # calcul wPLI
        wpli = np.abs(np.mean(np.sin(phase_difference))) / np.mean(np.abs(np.sin(phase_difference)))
        return wpli

class CoherenceStrategy(ConnectivityStrategy):
    def compute_connectivity(self, current_channel, next_channel, fs):
        """
        Clasa concreta ce extinde clasa abstracta ConnectivityStrategy. Aceasta implementeaza metoda abstracta compute_connectivity() pentru
        calculul conectivitatii folosind coerenta.
        """
        # calcul coerenta intre doua semnale, unde variabila f va pastra frecventele, si variabila coh valorile coerentelor
        f, coh = signal.coherence(current_channel, next_channel, fs)
        mean_coherence = coh.mean()

        return mean_coherence


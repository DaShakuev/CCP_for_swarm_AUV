import control as ctrl

class YawControl:
    def __init__(self, K1 = 0.08, K_omega = 0.5, Kc = 1, T = 0.15, xi = 0.707):
        self.K_Omega = K1 * K_omega * Kc
        self.T = T
        self.xi = xi
        self.transfer_function = self.create_transfer_function()
        
    def create_transfer_function(self):
        # Определите числитель и знаменатель передаточной функции
        numerator = [self.K_Omega]
        denominator = [self.T**2, 2*self.T*self.xi, 1, 0]
        # Создайте передаточную функцию
        Wp = ctrl.TransferFunction(numerator, denominator)
        # Создайте передаточную функцию замкнутой системы
        Wcl = ctrl.feedback(Wp, 1)
        return Wcl
    
    def get_response(self, error, time_span):
        _, response = ctrl.forced_response(self.transfer_function, T=time_span, U=error)
        return response[-1]  # Возвращаем последнее значение отклика

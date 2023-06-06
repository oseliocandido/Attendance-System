class User:
    def __init__(self, numero_identificacao, complete_name, date_nascimento, date_admissao, role, telephone_number, observation):
        self.numero_identificacao = numero_identificacao
        self.complete_name = complete_name
        self.date_nascimento = date_nascimento
        self.date_admissao = date_admissao
        self.role = role
        self.telephone_number = telephone_number
        self.observation = observation
        self.status = 'Ativo'


class UserDTO:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from functools import wraps
import copy

# ================= EXCEÇÕES =================
class SaldoInsuficienteError(Exception):
    pass

class LimiteExcedidoError(Exception):
    pass

class ContaNaoEncontradaError(Exception):
    pass

class OperacaoInvalidaError(Exception):
    pass


# ================= INTERFACE =================
class Tributavel(ABC):
    @abstractmethod
    def calcular_imposto(self):
        pass


# ================= DECORADORES =================
def auditoria(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} executado em {datetime.now()}")
        return func(*args, **kwargs)
    return wrapper


def transacao_atomica(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        backup_contas = copy.deepcopy(self.contas)
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.contas = backup_contas
            print("[ROLLBACK] Operação revertida")
            raise e
    return wrapper


def limite_diario(quantidade):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "_operacoes_diarias"):
                self._operacoes_diarias = {}

            hoje = datetime.now().date()
            self._operacoes_diarias.setdefault(hoje, 0)

            if self._operacoes_diarias[hoje] >= quantidade:
                raise LimiteExcedidoError("Limite diário excedido")

            resultado = func(self, *args, **kwargs)
            self._operacoes_diarias[hoje] += 1
            return resultado
        return wrapper
    return decorator


# ================= CONTA ABSTRATA =================
class Conta(ABC):
    def __init__(self, cliente, saldo=0):
        if saldo < 0:
            raise OperacaoInvalidaError("Saldo inicial inválido")

        self.__saldo = saldo
        self.cliente = cliente
        self._historico = []
        self._operacoes_diarias = {}

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, valor):
        if not isinstance(valor, (int, float)):
            raise OperacaoInvalidaError("Saldo inválido")
        self.__saldo = valor

    def registrar(self, descricao):
        self._historico.append((datetime.now(), descricao))

    def historico_90_dias(self):
        limite = datetime.now() - timedelta(days=90)
        return [h for h in self._historico if h[0] >= limite]

    @abstractmethod
    def sacar(self, valor):
        pass

    @abstractmethod
    def depositar(self, valor):
        pass

    def __add__(self, other):
        if not isinstance(other, Conta):
            raise OperacaoInvalidaError("Somente contas podem ser somadas")
        return self.saldo + other.saldo


# ================= CONTA CORRENTE =================
class ContaCorrente(Conta):
    LIMITE_NEGATIVO = -1000

    def __init__(self, cliente, saldo=0):
        super().__init__(cliente, saldo)
        if not hasattr(self, "_operacoes_diarias"):
            self._operacoes_diarias = {}

    @limite_diario(3)
    def sacar(self, valor):
        if valor <= 0:
            raise OperacaoInvalidaError("Valor inválido")

        if self.saldo - valor < self.LIMITE_NEGATIVO:
            raise SaldoInsuficienteError("Limite negativo atingido")

        self.saldo -= valor
        self.registrar(f"Saque R$ {valor}")

        if valor > 1000:
            print("[EMAIL] Saque elevado detectado")
        if self.saldo < 0:
            print("[SMS] Saldo negativo")

    def depositar(self, valor):
        if valor <= 0:
            raise OperacaoInvalidaError("Valor inválido")

        self.saldo += valor
        self.registrar(f"Depósito R$ {valor}")

    def cobrar_manutencao(self):
        self.saldo -= 15
        self.registrar("Taxa de manutenção")


# ================= CONTA CORRENTE ESPECIAL =================
class ContaCorrenteEspecial(ContaCorrente, Tributavel):
    LIMITE_NEGATIVO = -5000

    def depositar(self, valor):
        if valor <= 0:
            raise OperacaoInvalidaError("Valor inválido")

        cashback = valor * 0.005
        self.saldo += valor + cashback
        self.registrar(f"Depósito R$ {valor} + Cashback R$ {cashback:.2f}")

    def calcular_imposto(self):
        return self.saldo * 0.0038


# ================= CONTA POUPANÇA =================
class ContaPoupanca(Conta):
    def __init__(self, cliente, saldo=0):
        super().__init__(cliente, saldo)
        self._saques_mes = 0

    def sacar(self, valor):
        if valor <= 0:
            raise OperacaoInvalidaError("Valor inválido")

        taxa = 2 if self._saques_mes >= 1 else 0

        if self.saldo < valor + taxa:
            raise SaldoInsuficienteError("Saldo insuficiente")

        self.saldo -= valor + taxa
        self._saques_mes += 1
        self.registrar(f"Saque R$ {valor} Taxa R$ {taxa}")

    def depositar(self, valor):
        if valor <= 0:
            raise OperacaoInvalidaError("Valor inválido")

        self.saldo += valor
        self.registrar(f"Depósito R$ {valor}")

    def render(self):
        self.saldo *= 1.005
        self.registrar("Rendimento mensal")


# ================= CONTA POUPANÇA PREMIUM =================
class ContaPoupancaPremium(ContaPoupanca, Tributavel):
    def render(self):
        self.saldo *= 1.008 if self.saldo > 10000 else 1.005
        self.registrar("Rendimento premium")

    def sacar(self, valor):
        if valor <= 0:
            raise OperacaoInvalidaError("Valor inválido")

        if self.saldo < valor:
            raise SaldoInsuficienteError("Saldo insuficiente")

        self.saldo -= valor
        self.registrar(f"Saque R$ {valor} (Isento)")

    def calcular_imposto(self):
        return self.saldo * 0.0038


# ================= BANCO =================
class OrionBank:
    def __init__(self):
        self._id_conta = 1
        self.contas = {}
        self.transacoes_dia = []

    @auditoria
    def criar_conta(self, tipo, cliente, saldo=0):
        mapa = {
            "corrente": ContaCorrente,
            "especial": ContaCorrenteEspecial,
            "poupanca": ContaPoupanca,
            "premium": ContaPoupancaPremium
        }

        if tipo not in mapa:
            raise OperacaoInvalidaError("Tipo de conta inválido")

        conta = mapa[tipo](cliente, saldo)
        self.contas[self._id_conta] = conta
        self._id_conta += 1
        return self._id_conta - 1

    @auditoria
    def fechar_conta(self, id_conta):
        if id_conta not in self.contas:
            raise ContaNaoEncontradaError("Conta não encontrada")
        del self.contas[id_conta]

    @auditoria
    @transacao_atomica
    def transferir(self, origem, destino, valor):
        if origem not in self.contas or destino not in self.contas:
            raise ContaNaoEncontradaError("Conta não encontrada")

        if valor <= 0:
            raise OperacaoInvalidaError("Valor inválido")

        self.contas[origem].sacar(valor)
        self.contas[destino].depositar(valor)
        self.transacoes_dia.append((origem, destino, valor))

    def calcular_patrimonio_total(self):
        return sum(conta.saldo for conta in self.contas.values())

    def gerar_relatorio_mensal(self):
        print("\n=== RELATÓRIO MENSAL ===")
        for idc, conta in self.contas.items():
            print(f"Conta {idc} | Cliente: {conta.cliente} | Saldo: R$ {conta.saldo:.2f}")


# ================= TESTE =================
if __name__ == "__main__":
    banco = OrionBank()

    c1 = banco.criar_conta("corrente", "João", 1000)
    c2 = banco.criar_conta("especial", "Maria", 6000)
    c3 = banco.criar_conta("premium", "Carlos", 15000)

    banco.transferir(c2, c1, 500)
    banco.contas[c3].render()

    print("\nPatrimônio total:", banco.calcular_patrimonio_total())
    banco.gerar_relatorio_mensal()
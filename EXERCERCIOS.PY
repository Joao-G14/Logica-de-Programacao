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


# ================= INTERFACE DE MENU =================
def limpar_tela():
    print("\n" * 2)


def exibir_menu():
    print("\n" + "=" * 50)
    print("          🏦 ORION BANK - SISTEMA BANCÁRIO")
    print("=" * 50)
    print("\n[1] Criar Nova Conta")
    print("[2] Depositar")
    print("[3] Sacar")
    print("[4] Transferir")
    print("[5] Consultar Saldo")
    print("[6] Aplicar Rendimento (Poupança)")
    print("[7] Cobrar Manutenção (Conta Corrente)")
    print("[8] Ver Histórico (90 dias)")
    print("[9] Calcular Imposto")
    print("[10] Relatório Mensal")
    print("[11] Patrimônio Total")
    print("[12] Fechar Conta")
    print("[0] Sair")
    print("=" * 50)


def criar_conta_menu(banco):
    print("\n--- CRIAR NOVA CONTA ---")
    print("Tipos disponíveis:")
    print("  1. Corrente")
    print("  2. Especial (Corrente com cashback)")
    print("  3. Poupança")
    print("  4. Premium (Poupança com maior rendimento)")

    tipo_map = {"1": "corrente", "2": "especial", "3": "poupanca", "4": "premium"}
    tipo_escolha = input("\nEscolha o tipo (1-4): ").strip()

    if tipo_escolha not in tipo_map:
        print("❌ Tipo inválido!")
        return

    cliente = input("Nome do cliente: ").strip()
    if not cliente:
        print("❌ Nome inválido!")
        return

    try:
        saldo = float(input("Saldo inicial (0 para nenhum): ").strip() or "0")
        id_conta = banco.criar_conta(tipo_map[tipo_escolha], cliente, saldo)
        print(f"✅ Conta #{id_conta} criada com sucesso para {cliente}!")
    except Exception as e:
        print(f"❌ Erro: {e}")


def depositar_menu(banco):
    print("\n--- DEPOSITAR ---")
    try:
        id_conta = int(input("ID da conta: ").strip())
        if id_conta not in banco.contas:
            print("❌ Conta não encontrada!")
            return

        valor = float(input("Valor a depositar: R$ ").strip())
        banco.contas[id_conta].depositar(valor)
        print(f"✅ Depósito realizado! Novo saldo: R$ {banco.contas[id_conta].saldo:.2f}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def sacar_menu(banco):
    print("\n--- SACAR ---")
    try:
        id_conta = int(input("ID da conta: ").strip())
        if id_conta not in banco.contas:
            print("❌ Conta não encontrada!")
            return

        valor = float(input("Valor a sacar: R$ ").strip())
        banco.contas[id_conta].sacar(valor)
        print(f"✅ Saque realizado! Novo saldo: R$ {banco.contas[id_conta].saldo:.2f}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def transferir_menu(banco):
    print("\n--- TRANSFERIR ---")
    try:
        origem = int(input("ID da conta origem: ").strip())
        destino = int(input("ID da conta destino: ").strip())
        valor = float(input("Valor a transferir: R$ ").strip())

        banco.transferir(origem, destino, valor)
        print(f"✅ Transferência realizada com sucesso!")
        print(f"   Origem: R$ {banco.contas[origem].saldo:.2f}")
        print(f"   Destino: R$ {banco.contas[destino].saldo:.2f}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def consultar_saldo_menu(banco):
    print("\n--- CONSULTAR SALDO ---")
    try:
        id_conta = int(input("ID da conta: ").strip())
        if id_conta not in banco.contas:
            print("❌ Conta não encontrada!")
            return

        conta = banco.contas[id_conta]
        print(f"\n📊 Conta #{id_conta}")
        print(f"   Cliente: {conta.cliente}")
        print(f"   Tipo: {type(conta).__name__}")
        print(f"   Saldo: R$ {conta.saldo:.2f}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def aplicar_rendimento_menu(banco):
    print("\n--- APLICAR RENDIMENTO ---")
    try:
        id_conta = int(input("ID da conta poupança: ").strip())
        if id_conta not in banco.contas:
            print("❌ Conta não encontrada!")
            return

        conta = banco.contas[id_conta]
        if not isinstance(conta, ContaPoupanca):
            print("❌ Apenas contas poupança podem receber rendimento!")
            return

        saldo_anterior = conta.saldo
        conta.render()
        print(f"✅ Rendimento aplicado!")
        print(f"   Saldo anterior: R$ {saldo_anterior:.2f}")
        print(f"   Novo saldo: R$ {conta.saldo:.2f}")
        print(f"   Rendimento: R$ {conta.saldo - saldo_anterior:.2f}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def cobrar_manutencao_menu(banco):
    print("\n--- COBRAR MANUTENÇÃO ---")
    try:
        id_conta = int(input("ID da conta corrente: ").strip())
        if id_conta not in banco.contas:
            print("❌ Conta não encontrada!")
            return

        conta = banco.contas[id_conta]
        if not isinstance(conta, ContaCorrente):
            print("❌ Apenas contas correntes têm taxa de manutenção!")
            return

        saldo_anterior = conta.saldo
        conta.cobrar_manutencao()
        print(f"✅ Taxa cobrada! Novo saldo: R$ {conta.saldo:.2f}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def ver_historico_menu(banco):
    print("\n--- HISTÓRICO (90 DIAS) ---")
    try:
        id_conta = int(input("ID da conta: ").strip())
        if id_conta not in banco.contas:
            print("❌ Conta não encontrada!")
            return

        historico = banco.contas[id_conta].historico_90_dias()
        if not historico:
            print("ℹ️  Nenhuma transação nos últimos 90 dias.")
            return

        print(f"\n📋 Histórico da conta #{id_conta}:")
        for data, descricao in historico:
            print(f"   {data.strftime('%d/%m/%Y %H:%M:%S')} - {descricao}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def calcular_imposto_menu(banco):
    print("\n--- CALCULAR IMPOSTO ---")
    try:
        id_conta = int(input("ID da conta: ").strip())
        if id_conta not in banco.contas:
            print("❌ Conta não encontrada!")
            return

        conta = banco.contas[id_conta]
        if not isinstance(conta, Tributavel):
            print("❌ Esta conta não é tributável!")
            return

        imposto = conta.calcular_imposto()
        print(f"💰 Imposto a pagar: R$ {imposto:.2f}")
    except Exception as e:
        print(f"❌ Erro: {e}")


def fechar_conta_menu(banco):
    print("\n--- FECHAR CONTA ---")
    try:
        id_conta = int(input("ID da conta a fechar: ").strip())
        confirmacao = input(f"⚠️  Confirma o fechamento da conta #{id_conta}? (s/n): ").strip().lower()

        if confirmacao == 's':
            banco.fechar_conta(id_conta)
            print("✅ Conta fechada com sucesso!")
        else:
            print("ℹ️  Operação cancelada.")
    except Exception as e:
        print(f"❌ Erro: {e}")


# ================= MAIN =================
if __name__ == "__main__":
    banco = OrionBank()

    # Criar algumas contas de exemplo
    print("🔧 Inicializando sistema com contas de exemplo...")
    banco.criar_conta("corrente", "João Silva", 1000)
    banco.criar_conta("especial", "Maria Santos", 6000)
    banco.criar_conta("premium", "Carlos Oliveira", 15000)
    print("✅ Sistema pronto!\n")

    while True:
        exibir_menu()

        try:
            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "0":
                print("\n👋 Obrigado por usar o Orion Bank!")
                break
            elif opcao == "1":
                criar_conta_menu(banco)
            elif opcao == "2":
                depositar_menu(banco)
            elif opcao == "3":
                sacar_menu(banco)
            elif opcao == "4":
                transferir_menu(banco)
            elif opcao == "5":
                consultar_saldo_menu(banco)
            elif opcao == "6":
                aplicar_rendimento_menu(banco)
            elif opcao == "7":
                cobrar_manutencao_menu(banco)
            elif opcao == "8":
                ver_historico_menu(banco)
            elif opcao == "9":
                calcular_imposto_menu(banco)
            elif opcao == "10":
                banco.gerar_relatorio_mensal()
            elif opcao == "11":
                print(f"\n💵 Patrimônio Total do Banco: R$ {banco.calcular_patrimonio_total():.2f}")
            elif opcao == "12":
                fechar_conta_menu(banco)
            else:
                print("❌ Opção inválida! Escolha entre 0 e 12.")

            input("\n⏎ Pressione ENTER para continuar...")

        except KeyboardInterrupt:
            print("\n\n👋 Encerrando sistema...")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            input("\n⏎ Pressione ENTER para continuar...")
from PyQt5 import uic, QtWidgets
import sqlite3
from message_box import message_box_error_string, message_box_error_numeric, message_box_error_max_limit

banco = sqlite3.connect('crud.db')
cursor = banco.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS gerenciamento (id	INTEGER NOT NULL,nome	TEXT,status	TEXT,quantidade	'
               'REAL,data_inicial	TEXT,data_final	TEXT,PRIMARY KEY("id" AUTOINCREMENT))')
banco.commit()


def mostra_bd():
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM gerenciamento")
    dados_lidos = cursor.fetchall()

    principal.tableWidget.setRowCount(len(dados_lidos))
    principal.tableWidget.setColumnCount(6)
    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            principal.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def inserir_dados():
    # Salva os dados em variáveis
    nome = inserir.line_nome.text()
    quantidade = inserir.line_quantidade.text()

    # VERIFICAÇÃO
    if not nome.isalpha() or len(nome) > 15:
        message_box_error_string()
        return

    if inserir.check_status.isChecked():
        status = 'Ativo'
    else:
        status = 'Inativo'

    if not quantidade.isnumeric():
        message_box_error_numeric()
        return

    if int(quantidade) > 365:
        message_box_error_max_limit(365)
        return

    # Calcula a data da inscrição e a data final do plano convert para o padrão Brasileiro.
    from datetime import date, timedelta
    data_inicial = date.today()
    data_final = data_inicial + timedelta(int(quantidade))
    data_final_padrao = data_final.strftime("%d/%m/%Y")
    data_inicial_padrao = data_inicial.strftime("%d/%m/%Y")

    cursor = banco.cursor()
    comando_sql = 'INSERT INTO gerenciamento (nome, status, quantidade, data_inicial, data_final) ' \
                  'VALUES (?, ?, ?, ?, ?)'
    dados = (nome, status, str(quantidade), str(data_inicial_padrao), str(data_final_padrao),)
    cursor.execute(comando_sql, dados)
    banco.commit()
    inserir.close()
    mostra_bd()


def alterar_dados():
    global data_de_hoje_padrao_br, data_final_padrao_br
    pk = alterar.id_aluno.text()
    nome = alterar.nome_aluno.text()
    quantidade = alterar.quantidade_dias.text()

    if quantidade != '':
        from datetime import date, timedelta
        data_de_hoje = date.today()
        data_final = data_de_hoje + timedelta(int(quantidade))

        data_de_hoje_padrao_br = data_de_hoje.strftime("%d/%m/%Y")
        data_final_padrao_br = data_final.strftime("%d/%m/%Y")

    if alterar.check_status.isChecked():
        status = 'Ativo'

    else:
        status = 'Inativo'

    if pk != '' and nome != '':
        if pk.isnumeric() and nome.isalpha():
            if len(nome) < 15:
                cursor = banco.cursor()
                cursor.execute('update gerenciamento set nome=?, status=? where id=?', (nome, status, pk,))
                banco.commit()
                alterar.close()
            else:
                message_box_error_max_limit(15)
                return

        else:
            if not pk.isnumeric():
                message_box_error_numeric()
                return
            if not nome.isalpha():
                message_box_error_string()
                return

    if pk != '' and quantidade != '':
        if pk.isnumeric() and quantidade.isnumeric():
            cursor = banco.cursor()
            cursor.execute(
                'update gerenciamento set quantidade=?, status=?, data_inicial=?, data_final=? where id=?',
                (quantidade, status,
                 data_de_hoje_padrao_br,
                 data_final_padrao_br, pk,))
            banco.commit()
            alterar.close()

        else:
            if not pk.isnumeric():
                message_box_error_numeric()
                return

            if not quantidade.isnumeric():
                message_box_error_numeric()
                return

    if pk != '' and nome != '' and quantidade != '':
        if pk.isnumeric() and nome.isalpha() and quantidade.isnumeric():
            cursor = banco.cursor()
            cursor.execute(
                'update gerenciamento set nome=?, quantidade=?, status=?, data_inicial=?, data_final=? where id=?',
                (nome, quantidade,
                 status,
                 data_de_hoje_padrao_br,
                 data_final_padrao_br, pk,))
            banco.commit()
            alterar.close()
        else:
            if not pk.isnumeric():
                message_box_error_numeric()
                return

            if not nome.isalpha():
                message_box_error_string()
                return

            if not quantidade.isnumeric():
                message_box_error_numeric()
                return
    mostra_bd()


def excluir_dados():
    excluir_id = excluir.line_delete.text()
    if not excluir_id.isnumeric():
        return

    try:
        cursor = banco.cursor()
        cursor.execute(f'DELETE FROM gerenciamento where id = {excluir_id}')
        banco.commit()

    except:
        print('Digite apenas NÚMEROS')

    finally:
        mostra_bd()


def resultados():
    # Checagem
    if tela_resultado.filtrar_id.isChecked():
        pesquisa = tela_resultado.line_pesquisa.text()
        if not pesquisa.isnumeric():
            message_box_error_numeric()

    if tela_resultado.filtrar_nome.isChecked():
        pesquisa = tela_resultado.line_pesquisa.text()
        if not pesquisa.isalpha():
            message_box_error_string()

    if tela_resultado.filtrar_status.isChecked():
        pesquisa = tela_resultado.line_pesquisa.text()
        if not pesquisa.isalpha():
            message_box_error_string()

    if tela_resultado.filtrar_id.isChecked():
        pesquisa = tela_resultado.line_pesquisa.text()
        cursor = banco.cursor()
        comando_sql = 'SELECT * FROM gerenciamento WHERE id=?'
        cursor.execute(comando_sql, (pesquisa,))
        dados_lidos = cursor.fetchall()

        tela_resultado.tableWidget.setRowCount(len(dados_lidos))
        tela_resultado.tableWidget.setColumnCount(6)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 6):
                tela_resultado.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    if tela_resultado.filtrar_nome.isChecked():
        pesquisa = tela_resultado.line_pesquisa.text()
        cursor = banco.cursor()
        comando_sql = 'SELECT * FROM gerenciamento WHERE nome LIKE ?'
        cursor.execute(comando_sql, ("%" + pesquisa + '%',))
        dados_lidos = cursor.fetchall()

        tela_resultado.tableWidget.setRowCount(len(dados_lidos))
        tela_resultado.tableWidget.setColumnCount(6)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 6):
                tela_resultado.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    if tela_resultado.filtrar_status.isChecked():
        pesquisa = tela_resultado.line_pesquisa.text()
        cursor = banco.cursor()
        comando_sql = 'SELECT * FROM gerenciamento WHERE status LIKE ?'
        cursor.execute(comando_sql, (pesquisa + '%',))
        dados_lidos = cursor.fetchall()

        tela_resultado.tableWidget.setRowCount(len(dados_lidos))
        tela_resultado.tableWidget.setColumnCount(6)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 6):
                tela_resultado.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    if tela_resultado.filtrar_status.isChecked():
        pesquisa = tela_resultado.line_pesquisa.text()
        cursor = banco.cursor()
        comando_sql = 'SELECT * FROM gerenciamento WHERE status LIKE ?'
        cursor.execute(comando_sql, (pesquisa + '%',))
        dados_lidos = cursor.fetchall()

        tela_resultado.tableWidget.setRowCount(len(dados_lidos))
        tela_resultado.tableWidget.setColumnCount(6)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 6):
                tela_resultado.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    if tela_resultado.filtrar_qtda.isChecked():
        pesquisa = tela_resultado.line_pesquisa.text()
        cursor = banco.cursor()
        comando_sql = 'SELECT * FROM gerenciamento WHERE quantidade=?'
        cursor.execute(comando_sql, (pesquisa,))
        dados_lidos = cursor.fetchall()

        tela_resultado.tableWidget.setRowCount(len(dados_lidos))
        tela_resultado.tableWidget.setColumnCount(6)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 6):
                tela_resultado.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


# Inicializando o App
app = QtWidgets.QApplication([])

# Importando os Designs
principal = uic.loadUi("principal.ui")
inserir = uic.loadUi('inserir_dados.ui')
excluir = uic.loadUi('excluir_dados.ui')
alterar = uic.loadUi('alterar_dados.ui')
tela_resultado = uic.loadUi('tela_resultados.ui')

# Mostra o Banco de dados ao Abrir o Programa.
mostra_bd()

# Ligando os botões as telas
principal.btn_inserir.clicked.connect(inserir.show)
principal.btn_alterar.clicked.connect(alterar.show)
principal.btn_excluir.clicked.connect(excluir.show)
principal.btn_pesquisar.clicked.connect(tela_resultado.show)

# Botão da tela de Inserir
inserir.btn_inserir.clicked.connect(inserir_dados)
alterar.btn_alterar.clicked.connect(alterar_dados)
excluir.btn_delete.clicked.connect(excluir_dados)
tela_resultado.btn_pesquisa.clicked.connect(resultados)

principal.show()
app.exec()

import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    input_tipo = ft.TextField(label="Tipo", width=375)
    input_marca = ft.TextField(label="Marca", width=375)
    input_anno = ft.TextField(label="Anno acquisto", width=375)
    txt_valore = ft.TextField(value="0", width=75, disabled=True,
                              text_align=ft.TextAlign.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
        def diminuisci_valore(e):
            # Decrementa il contatore di 1 euro, senza scendere sotto lo 0
            v = int(txt_valore.value)
            if v > 0:
                v = v - 1
            txt_valore.value = v
            txt_valore.update()

        def aumenta_valore(e):
            # Incrementa il contatore di 1 euro
            v = int(txt_valore.value)
            v = v + 1
            txt_valore.value = v
            txt_valore.update()

        def conferma_strumento(e):
            # Legge tipo e marca togliendo gli spazi a inizio/fine
            tipo = input_tipo.value.strip()
            marca = input_marca.value.strip()

            # Controllo campi obbligatori: se uno è vuoto mostra l'alert ed esce
            # (il return evita di svuotare i campi, così l'utente non perde quanto scritto)
            if tipo == "" or marca == "":
                alert.show_alert("❌ Errore: inserisci tipo e marca.")
                return

            try:
                anno = int(input_anno.value)  # int() solleva ValueError se il testo non è un intero
            except ValueError:
                alert.show_alert("❌ Errore: inserisci un valore numerico valido per l'anno.")
                return

            # Aggiunge lo strumento al deposito (il codice S<n> è generato dal deposito)
            deposito.aggiungi_strumento(tipo, marca, anno, float(txt_valore.value))

            # Svuota i campi e azzera il contatore per il prossimo inserimento
    input_tipo.value = ""
    input_marca.value = ""
    input_anno.value = ""
    txt_valore.value = "0"

    # Ricostruisce la lista (ordinata per marca) e aggiorna la pagina
    aggiorna_lista_strumenti()
    page.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    pulsante_meno = ft.IconButton(icon=ft.Icons.REMOVE, icon_color=ft.Colors.RED,
                                  on_click=diminuisci_valore)
    pulsante_piu = ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN,
                                 on_click=aumenta_valore)
    pulsante_aggiungi = ft.Button("Aggiungi strumento", on_click=conferma_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text("Aggiungi nuovo strumento", size=20),
        # Riga con i tre campi (tipo, marca, anno) e il contatore del valore (- valore +)
        ft.Row(controls=[input_tipo, input_marca, input_anno,
                         pulsante_meno, txt_valore, pulsante_piu],
               spacing=40,
               alignment=ft.MainAxisAlignment.CENTER),
        # Pulsante di conferma, centrato sotto la riga
        ft.Row(controls=[pulsante_aggiungi],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)

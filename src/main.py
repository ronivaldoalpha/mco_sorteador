import flet as ft
from random import choice
import asyncio

@ft.component
def App():
    count, set_count = ft.use_state(0)
    sorteados, set_sorteados = ft.use_state([])
    max_range, set_max_range = ft.use_state(100)
    bt_roleta_ativo, set_bt_roleta_ativo = ft.use_state(True)

    numeros_sorteio = list(range(1, max_range+1))

    async def roleta(e):
        set_bt_roleta_ativo(False)
        for _ in range(20):
            valor = choice(numeros_sorteio)
            set_count(valor)
            await asyncio.sleep(0.1)
        while valor in sorteados:
            valor = choice(numeros_sorteio)
        set_count(valor)
        set_sorteados(sorteados + [valor])
        numeros_sorteio.remove(valor)
        set_bt_roleta_ativo(True)

    def reset(e):
        set_count(0)
        set_sorteados([])
        numeros_sorteio = list(range(1, max_range+1))

    def salvar_iniciar(e):
        valor = 0 if e.control.value == "" else int(e.control.value)
        set_max_range(valor)
        reset(e)

    return ft.Container(
        alignment=ft.Alignment.CENTER,
        expand=True,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Row(
                        wrap=True,
                        controls=[
                        ft.Text(value=f"{sorteado:02d} .", size=50) for sorteado in sorteados
                        ]
                    ),
            ),
                ft.Divider(color=ft.Colors.AMBER_400),
                ft.Row(
                    margin=ft.Margin.all(20),
                    alignment=ft.MainAxisAlignment.END, 
                    controls=[
                        ft.TextField(
                            label="Máximo: ",
                            width=100,
                            max_length=3,
                            value=str(max_range),
                            keyboard_type=ft.KeyboardType.NUMBER,
                            on_submit=salvar_iniciar
                        ),
                    ]
                ),
                ft.Text(value=f"{count:02d}", size=150, color=ft.Colors.AMBER_400),
                ft.Button("Roleta", on_click=roleta, disabled=not bt_roleta_ativo),
                ft.Button("Reset", on_click=reset),
            ]
        )
    )

ft.run(lambda page: page.render(App))

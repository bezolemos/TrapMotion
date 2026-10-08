"""TrapMotion — interface gráfica do Projeto 15.

Entrada de parâmetros (Tkinter), interpretação dos resultados e gráficos (Matplotlib).
Toda a física fica isolada em simulacao.py.
"""

import math
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from simulacao import calcular_constante_torsional, executar_simulacao


class TrapMotionApp(tk.Tk):
    """Janela principal: os widgets ficam separados da lógica de simulação."""

    def __init__(self):
        super().__init__()
        self.title("TrapMotion | Simulador de carrinho de ratoeira")
        self.geometry("1380x820")
        self.minsize(1040, 640)

        self.campos = {}
        self.conhece_constante = tk.StringVar(value="sim")
        self.ultimo_resultado = None
        self.canvas_grafico = None
        self.toolbar_grafico = None

        self._configurar_estilo()
        self._construir_interface()
        self._preencher_exemplo()
        self._atualizar_campos_mola()

    def _configurar_estilo(self):
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("TFrame", background="#F3F6FA")
        estilo.configure("TLabelframe", background="#F3F6FA")
        estilo.configure("TLabelframe.Label", background="#F3F6FA", font=("Segoe UI", 10, "bold"))
        estilo.configure("TLabel", background="#F3F6FA", font=("Segoe UI", 10))
        estilo.configure("TButton", font=("Segoe UI", 10, "bold"), padding=7)
        estilo.configure("TEntry", padding=4)
        estilo.configure("TRadiobutton", background="#F3F6FA", font=("Segoe UI", 10))
        estilo.configure("TNotebook", background="#F3F6FA")
        estilo.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=(16, 8))

    def _construir_interface(self):
        # Área superior com o nome e a explicação do programa.
        topo = ttk.Frame(self, padding=(18, 10))
        topo.pack(fill="x")
        ttk.Label(topo, text="TrapMotion", font=("Segoe UI", 21, "bold")).pack(anchor="w")
        ttk.Label(
            topo,
            text="Projeto 15  •  Simulação física de carrinhos movidos a ratoeira  •  V11",
        ).pack(anchor="w")

        corpo = ttk.Frame(self, padding=(12, 4, 12, 12))
        corpo.pack(fill="both", expand=True)
        corpo.columnconfigure(0, weight=0)
        corpo.columnconfigure(1, weight=1)
        corpo.rowconfigure(0, weight=1)

        # Esquerda: formulário rolável para funcionar também em telas menores.
        esquerda = ttk.Frame(corpo, width=390)
        esquerda.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        esquerda.grid_propagate(False)
        esquerda.rowconfigure(0, weight=1)
        esquerda.columnconfigure(0, weight=1)

        scroll = tk.Canvas(esquerda, bg="#F3F6FA", highlightthickness=0, width=375)
        barra = ttk.Scrollbar(esquerda, orient="vertical", command=scroll.yview)
        scroll.configure(yscrollcommand=barra.set)
        scroll.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        form = ttk.Frame(scroll, padding=(4, 4, 12, 8))
        janela_form = scroll.create_window((0, 0), window=form, anchor="nw")
        form.bind("<Configure>", lambda _e: scroll.configure(scrollregion=scroll.bbox("all")))
        scroll.bind("<Configure>", lambda e: scroll.itemconfigure(janela_form, width=e.width))
        # No Windows, a roda do mouse é recebida como incrementos de 120.
        scroll.bind("<MouseWheel>", lambda e: scroll.yview_scroll(-int(e.delta / 120), "units"))
        form.bind("<MouseWheel>", lambda e: scroll.yview_scroll(-int(e.delta / 120), "units"))

        geometria = ttk.LabelFrame(form, text="1. Geometria e objetivo", padding=10)
        geometria.pack(fill="x", pady=(0, 9))
        self._adicionar_campo(geometria, 0, "Diâmetro da roda (cm)", "roda")
        self._adicionar_campo(geometria, 1, "Diâmetro do eixo (cm)", "eixo")
        self._adicionar_campo(geometria, 2, "Comprimento da corda (cm)", "corda")
        self._adicionar_campo(geometria, 3, "Comprimento da haste (cm)", "haste")
        self._adicionar_campo(geometria, 4, "Massa total do carrinho (g)", "massa")
        self._adicionar_campo(geometria, 5, "Meta de distância (m)", "meta")

        mola = ttk.LabelFrame(form, text="2. Mola da ratoeira", padding=10)
        mola.pack(fill="x", pady=(0, 9))
        ttk.Label(mola, text="Você conhece a constante torsional?").pack(anchor="w")
        radios = ttk.Frame(mola)
        radios.pack(anchor="w", pady=4)
        ttk.Radiobutton(
            radios, text="Sim", value="sim", variable=self.conhece_constante,
            command=self._atualizar_campos_mola,
        ).pack(side="left", padx=(0, 16))
        ttk.Radiobutton(
            radios, text="Não (estimar por medição)", value="nao",
            variable=self.conhece_constante, command=self._atualizar_campos_mola,
        ).pack(side="left")

        # O container reserva a posição dos campos dinâmicos antes dos ângulos.
        self.opcoes_mola = ttk.Frame(mola)
        self.opcoes_mola.pack(fill="x")
        self.frame_sabe = ttk.Frame(self.opcoes_mola)
        self.frame_nao_sabe = ttk.Frame(self.opcoes_mola)
        self._adicionar_campo(self.frame_sabe, 0, "Constante k (N·m/rad)", "constante")
        self._adicionar_campo(self.frame_nao_sabe, 0, "Força perpendicular medida (N)", "forca")
        self._adicionar_campo(self.frame_nao_sabe, 1, "Ângulo medido (graus)", "angulo_medicao")
        ttk.Label(
            self.frame_nao_sabe,
            text="A medição deve usar a haste e ângulo relativo à posição relaxada.",
            wraplength=330,
        ).pack(anchor="w", pady=3)

        ttk.Separator(mola, orient="horizontal").pack(fill="x", pady=7)
        ttk.Label(mola, text="Ângulos da simulação", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        angulos = ttk.Frame(mola)
        angulos.pack(fill="x")
        self._adicionar_campo(angulos, 0, "Ângulo inicial da mola (°)", "angulo_inicial")
        self._adicionar_campo(angulos, 1, "Ângulo atual / partida (°)", "angulo_atual")

        parametros = ttk.LabelFrame(form, text="3. Hipóteses adotadas", padding=10)
        parametros.pack(fill="x", pady=(0, 9))
        ttk.Label(
            parametros,
            text="Atrito estático μ = 0,60  |  Rolamento Crr = 0,02\n"
                 "Gravidade = 9,81 m/s²  |  Passo = 0,005 s\n"
                 "Limite = 60 s. Valores ilustrativos, não medidos.",
            wraplength=335,
        ).pack(anchor="w")

        ttk.Label(form, text="Os valores iniciais são apenas um exemplo de teste.",
                  wraplength=335).pack(anchor="w", pady=4)
        # O botão fica FIXO fora da área rolável para nunca desaparecer na tela.
        ttk.Button(esquerda, text="SIMULAR CARRINHO", command=self.simular).grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(8, 0), ipady=5)

        # Direita: três abas evitam sobrecarga de textos na tela.
        direita = ttk.Frame(corpo)
        direita.grid(row=0, column=1, sticky="nsew")
        direita.rowconfigure(0, weight=1)
        direita.columnconfigure(0, weight=1)
        self.abas = ttk.Notebook(direita)
        self.abas.grid(row=0, column=0, sticky="nsew")

        self.aba_resumo = ttk.Frame(self.abas, padding=16)
        self.aba_detalhes = ttk.Frame(self.abas, padding=10)
        self.aba_graficos = ttk.Frame(self.abas, padding=4)
        self.abas.add(self.aba_resumo, text="Resumo e recomendações")
        self.abas.add(self.aba_detalhes, text="Detalhes físicos")
        self.abas.add(self.aba_graficos, text="Gráficos")

        self.status = tk.Label(
            self.aba_resumo, text="Preencha os parâmetros e clique em SIMULAR CARRINHO.",
            font=("Segoe UI", 15, "bold"), bg="#F3F6FA", fg="#1C3552",
            anchor="w", justify="left", wraplength=750,
        )
        self.status.pack(fill="x", pady=(3, 15))
        self.resumo_texto = scrolledtext.ScrolledText(
            self.aba_resumo, font=("Consolas", 11), bg="white", fg="#18283B",
            relief="flat", padx=16, pady=14, wrap="word", state="disabled",
        )
        self.resumo_texto.pack(fill="both", expand=True)

        self.detalhes_texto = scrolledtext.ScrolledText(
            self.aba_detalhes, font=("Consolas", 10),
            bg="white", fg="#18283B", wrap="word", state="disabled",
        )
        self.detalhes_texto.pack(fill="both", expand=True)

        self.area_graficos = ttk.Frame(self.aba_graficos)
        self.area_graficos.pack(fill="both", expand=True)
        ttk.Label(self.area_graficos, text="Os gráficos serão exibidos depois da primeira simulação.").pack(
            anchor="center", pady=24)

    def _adicionar_campo(self, parent, linha, rotulo, chave):
        """Cria um Label/Entry e guarda o Entry pelo nome 'chave'."""
        linha_frame = ttk.Frame(parent)
        linha_frame.pack(fill="x", pady=3)
        ttk.Label(linha_frame, text=rotulo).pack(side="left", fill="x", expand=True)
        entrada = ttk.Entry(linha_frame, width=11)
        entrada.pack(side="right", padx=(5, 1))
        self.campos[chave] = entrada

    def _preencher_exemplo(self):
        """Dados para demonstração (não representam medição experimental)."""
        exemplos = {
            "roda": "10", "eixo": "1", "corda": "100", "haste": "15",
            "massa": "200", "meta": "10", "constante": "0.2",
            "forca": "2.0944", "angulo_medicao": "90",
            "angulo_inicial": "90", "angulo_atual": "90",
        }
        for chave, valor in exemplos.items():
            self.campos[chave].insert(0, valor)

    def _atualizar_campos_mola(self):
        """Mostra um campo para k conhecido OU dois para k medido."""
        self.frame_sabe.pack_forget()
        self.frame_nao_sabe.pack_forget()
        if self.conhece_constante.get() == "sim":
            # O posicionamento simples pelo pack não altera os valores digitados.
            self.frame_sabe.pack(fill="x", pady=4)
        else:
            self.frame_nao_sabe.pack(fill="x", pady=4)

    def _ler_numero(self, chave, descricao):
        """Aceita 2.5 ou 2,5, mas rejeita campos vazios com mensagem amigável."""
        texto = self.campos[chave].get().strip().replace(",", ".")
        if not texto:
            raise ValueError(f"Preencha o campo: {descricao}.")
        try:
            return float(texto)
        except ValueError as exc:
            raise ValueError(f"Digite um número válido em: {descricao}.") from exc

    def simular(self):
        """O botão lê os Entries, chama o motor físico e mostra a resposta."""
        try:
            roda = self._ler_numero("roda", "Diâmetro da roda")
            eixo = self._ler_numero("eixo", "Diâmetro do eixo")
            corda = self._ler_numero("corda", "Comprimento da corda")
            haste = self._ler_numero("haste", "Comprimento da haste")
            massa = self._ler_numero("massa", "Massa")
            meta = self._ler_numero("meta", "Distância da meta")
            angulo_inicial = self._ler_numero("angulo_inicial", "Ângulo inicial")
            angulo_atual = self._ler_numero("angulo_atual", "Ângulo atual")

            if self.conhece_constante.get() == "sim":
                k = self._ler_numero("constante", "Constante torsional")
            else:
                forca = self._ler_numero("forca", "Força medida")
                angulo_medido = self._ler_numero("angulo_medicao", "Ângulo medido")
                k = calcular_constante_torsional(forca, haste, angulo_medido)

            # Uma só chamada substitui toda a física que ficava na interface.
            resultado = executar_simulacao(
                roda, eixo, corda, haste, massa, meta, k,
                angulo_inicial, angulo_atual,
                coeficiente_atrito_estatico=0.6,
                coeficiente_resistencia_rolamento=0.02,
            )
        except (ValueError, ZeroDivisionError, OverflowError) as erro:
            messagebox.showerror("Confira os dados", str(erro), parent=self)
            return
        except Exception as erro:
            messagebox.showerror("Falha inesperada", str(erro), parent=self)
            raise  # Preserva traceback para depuração no terminal.

        self.ultimo_resultado = resultado
        self._mostrar_resultados(resultado)
        self._atualizar_graficos(resultado)
        self.abas.select(self.aba_resumo)

    @staticmethod
    def _formatar(valor, casas=3):
        return f"{valor:.{casas}f}".replace(".", ",")

    def _alterar_texto(self, widget, conteudo):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", conteudo)
        widget.configure(state="disabled")

    def _mostrar_resultados(self, dados):
        mov, meta = dados["movimento"], dados["meta"]
        f = self._formatar
        if meta["resultado"] == "meta_atingida":
            status, cor = "META ATINGIDA", "#187347"
        elif meta["resultado"] == "resultado_inconclusivo":
            status, cor = "SIMULAÇÃO INCONCLUSIVA (60 s)", "#9A6A10"
        else:
            status, cor = "META NÃO ATINGIDA", "#A13E34"
        self.status.configure(text=status, fg=cor)

        linhas = [
            "RESULTADOS PRINCIPAIS",
            "─" * 56,
            f"Distância final simulada     {f(mov['distancia_total_m'])} m",
            f"Meta desejada                {f(meta['distancia_meta_m'])} m",
            f"Percentual da meta           {f(meta['porcentagem'], 1)} %",
            f"Tempo total de movimento     {f(mov['tempo_total_s'])} s",
            f"Velocidade máxima            {f(mov['velocidade_maxima_m_s'])} m/s",
            f"Velocidade final             {f(mov['velocidade_final_m_s'])} m/s",
            f"Fim da impulsão              {f(mov['tempo_fim_impulsao'])} s",
            f"Distância impulsionada       {f(mov['distancia_fase_impulsionada_m'])} m",
            f"Distância na fase livre      {f(mov['distancia_fase_livre_m'])} m",
            f"Constante torsional          {f(dados['parametros']['constante_torsional_mola'], 5)} N·m/rad",
        ]
        if meta["tempo_meta_atingida_s"] is not None:
            linhas.append(
                f"Instante em que atingiu meta {f(meta['tempo_meta_atingida_s'])} s")
        linhas.extend(["", "DIAGNÓSTICOS", "─" * 56])
        linhas.extend(f"• {texto}" for texto in dados["diagnosticos"])
        if not dados["diagnosticos"]:
            linhas.append("• Nenhuma limitação específica identificada nos testes do modelo.")
        linhas.extend(["", "RECOMENDAÇÕES", "─" * 56])
        linhas.extend(f"• {texto}" for texto in dados["recomendacoes"])
        if not dados["recomendacoes"]:
            linhas.append("• Não há ajustes obrigatórios para a meta informada.")
        linhas.extend(["", "OBSERVAÇÃO", "─" * 56, dados["limitacoes"]])
        self._alterar_texto(self.resumo_texto, "\n".join(linhas))
        self._alterar_texto(self.detalhes_texto, self._texto_detalhes(dados))

    def _texto_detalhes(self, dados):
        """Mostra as grandezas V1–V9 com unidade e interpretação básica."""
        f = self._formatar
        g = dados["geometria"]
        m = dados["mola"]
        a = dados["aceleracao"]
        r = dados["resistencia"]
        ad = dados["aderencia"]
        mov = dados["movimento"]
        meta = dados["meta"]
        linhas = [
            "TRAPMOTION — DETALHES DA SIMULAÇÃO", "=" * 62,
            "", "V1 — GEOMETRIA",
            f"Raio da roda:                 {f(g['raio_roda_m'], 5)} m",
            f"Raio do eixo:                 {f(g['raio_eixo_m'], 5)} m",
            f"Circunferência da roda:       {f(g['circunferencia_roda_m'])} m",
            f"Circunferência do eixo:       {f(g['circunferencia_eixo_m'])} m",
            f"Rotações geométricas:         {f(g['rotacoes'])}",
            f"Alcance geométrico ideal:    {f(g['distancia_teorica_m'])} m",
            "Nota: o alcance geométrico não considera todas as perdas.",
            "", "V2 — MOLA E TRANSMISSÃO",
            f"Torque inicial:               {f(m['torque_inicial'])} N·m",
            f"Torque no ângulo atual:       {f(m['torque_atual'])} N·m",
            f"Energia inicial:              {f(m['energia_inicial'])} J",
            f"Energia no ângulo atual:      {f(m['energia_atual'])} J",
            f"Energia já liberada:          {f(m['energia_liberada'])} J",
            f"Tensão inicial da corda:      {f(m['tensao_inicial_corda'])} N",
            f"Tensão no ângulo atual:       {f(m['tensao_atual_corda'])} N",
            f"Torque inicial no eixo:       {f(m['torque_inicial_eixo'])} N·m",
            f"Força de tração inicial:      {f(m['forca_tracao_inicial'])} N",
            f"Força tração no ângulo atual: {f(m['forca_tracao_atual'])} N",
            "", "V3 — ACELERAÇÃO IDEAL",
            f"Massa total:                  {f(a['massa_total_carrinho_kg'])} kg",
            f"Aceleração ideal inicial:    {f(a['aceleracao_inicial'])} m/s²",
            f"Aceleração ideal atual:      {f(a['aceleracao_atual'])} m/s²",
            "", "V4 — RESISTÊNCIA AO ROLAMENTO",
            f"Peso e força normal:         {f(r['forca_normal'])} N",
            f"Resistência ao rolamento:    {f(r['forca_resistencia_rolamento'])} N",
            f"Força resultante inicial:    {f(r['forca_resultante_inicial'])} N",
            f"Força resultante atual:      {f(r['forca_resultante_atual'])} N",
            f"Aceleração c/ resistência:   {f(r['aceleracao_resistencia_inicial'])} m/s²",
            "", "V5 — ADERÊNCIA",
            f"Coeficiente estático (μ):    {f(ad['coeficiente'], 2)}",
            f"Aderência máxima:            {f(ad['forca_maxima'])} N",
            f"Tração útil inicial:         {f(ad['forca_tracao_util_inicial'])} N",
            f"Tração útil atual:           {f(ad['forca_tracao_util_atual'])} N",
            f"Aceleração inicial c/ μ:     {f(ad['aceleracao_inicial'])} m/s²",
            "", "V6–V7 — MOVIMENTO",
            f"Fim da fase impulsionada:    {f(mov['tempo_fim_impulsao'])} s",
            f"Velocidade ao fim da fase:   {f(mov['velocidade_fim_impulsao'])} m/s",
            f"Distância impulsionada:      {f(mov['distancia_fase_impulsionada_m'])} m",
            f"Distância na fase livre:     {f(mov['distancia_fase_livre_m'])} m",
            f"Distância total:             {f(mov['distancia_total_m'])} m",
            f"Ângulo final:                {f(mov['angulo_final_graus'])}°",
            f"Corda desenrolada:           {f(mov['corda_desenrolada_m'])} m",
            f"Motivo fim impulsão:         {mov['motivo_fim_impulsao']}",
            f"Motivo fim simulação:        {mov['motivo_encerramento']}",
            "", "V8 — META",
            f"Meta:                        {f(meta['distancia_meta_m'])} m",
            f"Resultado:                   {meta['resultado']}",
            f"Percentual atingido:         {f(meta['porcentagem'], 1)} %",
            "", "V9 — DIAGNÓSTICOS E RECOMENDAÇÕES",
        ]
        linhas.extend(f"Diagnóstico: {x}" for x in dados["diagnosticos"])
        linhas.extend(f"Recomendação: {x}" for x in dados["recomendacoes"])
        if dados["ajustes_geometricos"]:
            aj = dados["ajustes_geometricos"]
            linhas.extend([
                "", "ALTERNATIVAS GEOMÉTRICAS ISOLADAS",
                f"Aumentar roda em:            {f(aj['aumento_roda_cm'])} cm",
                f"Aumentar corda em:           {f(aj['aumento_corda_cm'])} cm",
                f"Reduzir eixo em:             {f(aj['reducao_eixo_cm'])} cm",
                "Atenção: estimativas geométricas, não garantia de alcance real.",
            ])
        linhas.extend(["", "LIMITAÇÕES DO MODELO", dados["limitacoes"]])
        return "\n".join(linhas)

    def _atualizar_graficos(self, dados):
        """V10: quatro curvas numa figura 2×2, incorporadas ao Tkinter."""
        if self.toolbar_grafico is not None:
            self.toolbar_grafico.destroy()
            self.toolbar_grafico = None
        if self.canvas_grafico is not None:
            self.canvas_grafico.get_tk_widget().destroy()
            self.canvas_grafico = None
        for widget in self.area_graficos.winfo_children():
            widget.destroy()

        h = dados["historicos"]
        t = h["tempo"]
        angulos_graus = [math.degrees(angulo) for angulo in h["angulo_rad"]]
        meta = dados["meta"]
        tempo_impulsao = dados["movimento"]["tempo_fim_impulsao"]
        fig = Figure(figsize=(9.1, 5.8), dpi=100)
        eixos = fig.subplots(2, 2)

        # Mesma organização da V10: posição, velocidade, aceleração e mola.
        dados_plot = [
            (eixos[0, 0], h["posicao"], "Posição × tempo", "Posição (m)"),
            (eixos[0, 1], h["velocidade"], "Velocidade × tempo", "Velocidade (m/s)"),
            (eixos[1, 0], h["aceleracao"], "Aceleração × tempo", "Aceleração (m/s²)"),
            (eixos[1, 1], angulos_graus, "Ângulo da mola × tempo", "Ângulo (°)"),
        ]
        for ax, valores, titulo, eixo_y in dados_plot:
            ax.plot(t, valores, linewidth=1.8)
            # Com um ponto, plot sozinho não desenha uma linha visível.
            if len(t) == 1:
                ax.scatter(t, valores, s=50, zorder=3)
            ax.set_title(titulo, fontsize=10)
            ax.set_xlabel("Tempo (s)", fontsize=9)
            ax.set_ylabel(eixo_y, fontsize=9)
            ax.grid(True, alpha=0.35)
            ax.tick_params(labelsize=8)

        eixos[0, 0].axhline(meta["distancia_meta_m"], linestyle="--", label="Meta")
        if meta["tempo_meta_atingida_s"] is not None:
            eixos[0, 0].axvline(meta["tempo_meta_atingida_s"], linestyle=":", label="Meta atingida")
        for ax in (eixos[0, 1], eixos[1, 0], eixos[1, 1]):
            ax.axvline(tempo_impulsao, linestyle="--", label="Fim da impulsão")
        for ax in eixos.flat:
            if ax.get_legend_handles_labels()[1]:
                ax.legend(fontsize=8, loc="best")
        fig.tight_layout(pad=2.0)

        self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.area_graficos)
        self.canvas_grafico.draw()
        widget_grafico = self.canvas_grafico.get_tk_widget()
        widget_grafico.pack(side="top", fill="both", expand=True)
        self.toolbar_grafico = NavigationToolbar2Tk(
            self.canvas_grafico, self.area_graficos, pack_toolbar=False)
        self.toolbar_grafico.update()
        self.toolbar_grafico.pack(side="bottom", fill="x")


def iniciar_interface():
    """Chamada a partir do arquivo de entrada simulador.py."""
    app = TrapMotionApp()
    app.mainloop()


if __name__ == "__main__":
    iniciar_interface()

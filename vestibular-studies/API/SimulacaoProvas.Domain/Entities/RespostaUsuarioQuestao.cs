using System;

namespace SimulacaoProvas.Domain.Entities
{
    public class RespostaUsuarioQuestao
    {
    public int Id { get; set; }
    public int UsuarioId { get; set; }
    public int QuestaoId { get; set; }
    public required string OpcaoSelecionada { get; set; }
    public bool EstaCorreta { get; set; }
    public DateTime RespondidoEm { get; set; }
    public Usuario? Usuario { get; set; }
    public Questao? Questao { get; set; }
    }
}

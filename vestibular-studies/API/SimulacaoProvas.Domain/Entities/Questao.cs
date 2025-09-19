using System;
using System;
using System.Collections.Generic;

namespace SimulacaoProvas.Domain.Entities
{
    public class Questao
    {
    public int Id { get; set; } 
    public int MateriaId { get; set; }
    public required string Enunciado { get; set; }
    public required string OpcoesJson { get; set; }
    public required string OpcaoCorreta { get; set; }
    public string? Explicacao { get; set; }
    public DateTime CriadoEm { get; set; }
    public Materia? Materia { get; set; }
    public ICollection<RespostaUsuarioQuestao> Respostas { get; set; } = new List<RespostaUsuarioQuestao>();
    }
}

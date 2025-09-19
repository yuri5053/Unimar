using System;
using System.Collections.Generic;

namespace SimulacaoProvas.Domain.Entities
{
    public class Usuario
    {
    public int Id { get; set; } 
    public required string Email { get; set; }
    public required string Nome { get; set; }
    public string? Foto { get; set; }
    public required string ProvedorAutenticacao { get; set; }
    public required string SenhaHash { get; set; }
    public DateTime CriadoEm { get; set; }
    public ICollection<RespostaUsuarioQuestao> Respostas { get; set; } = new List<RespostaUsuarioQuestao>();
    }
}
